// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#ifndef ARROW_STL_H
#define ARROW_STL_H

#include <algorithm>
#include <cstddef>
#include <memory>
#include <sstream>
#include <string>
#include <tuple>
#include <type_traits>
#include <utility>
#include <vector>

#include "arrow/builder.h"
#include "arrow/compute/api.h"
#include "arrow/memory_pool.h"
#include "arrow/status.h"
#include "arrow/table.h"
#include "arrow/type.h"
#include "arrow/type_traits.h"
#include "arrow/util/checked_cast.h"
#include "arrow/util/macros.h"

namespace arrow {

class Schema;

namespace stl {

namespace internal {

template <typename T, typename = void>
struct is_optional_like : public std::false_type {};

template <typename T, typename = void>
struct is_dereferencable : public std::false_type {};

template <typename T>
struct is_dereferencable<T, arrow::internal::void_t<decltype(*std::declval<T>())>>
    : public std::true_type {};

template <typename T>
struct is_optional_like<
    T, typename std::enable_if<
           std::is_constructible<bool, T>::value && is_dereferencable<T>::value &&
           !std::is_array<typename std::remove_reference<T>::type>::value>::type>
    : public std::true_type {};

template <size_t N, typename Tuple>
using BareTupleElement =
    typename std::decay<typename std::tuple_element<N, Tuple>::type>::type;

}  // namespace internal

template <typename T, typename R = void>
using enable_if_optional_like =
    typename std::enable_if<internal::is_optional_like<T>::value, R>::type;

/// Traits meta class to map standard C/C++ types to equivalent Arrow types.
template <typename T, typename Enable = void>
struct ConversionTraits {};

/// Returns builder type for given standard C/C++ type.
template <typename CType>
using CBuilderType =
    typename TypeTraits<typename ConversionTraits<CType>::ArrowType>::BuilderType;

/// Default implementation of AppendListValues.
///
/// This function can be specialized by user to take advantage of appending
/// contiguous ranges while appending. This default implementation will call
/// ConversionTraits<ValueCType>::AppendRow() for each value in the range.
template <typename ValueCType, typename Range>
Status AppendListValues(CBuilderType<ValueCType>& value_builder, Range&& cell_range) {
  for (auto const& value : cell_range) {
    ARROW_RETURN_NOT_OK(ConversionTraits<ValueCType>::AppendRow(value_builder, value));
  }
  return Status::OK();
}

#define ARROW_STL_CONVERSION(CType_, ArrowType_)                                    \
  template <>                                                                       \
  struct ConversionTraits<CType_> : public CTypeTraits<CType_> {                    \
    static Status AppendRow(typename TypeTraits<ArrowType_>::BuilderType& builder,  \
                            CType_ cell) {                                          \
      return builder.Append(cell);                                                  \
    }                                                                               \
    static CType_ GetEntry(const typename TypeTraits<ArrowType_>::ArrayType& array, \
                           size_t j) {                                              \
      return array.Value(j);                                                        \
    }                                                                               \
  };                                                                                \
                                                                                    \
  template <>                                                                       \
  Status AppendListValues<CType_, const std::vector<CType_>&>(                      \
      typename TypeTraits<ArrowType_>::BuilderType & value_builder,                 \
      const std::vector<CType_>& cell_range) {                                      \
    return value_builder.AppendValues(cell_range);                                  \
  }

ARROW_STL_CONVERSION(bool, BooleanType)
ARROW_STL_CONVERSION(int8_t, Int8Type)
ARROW_STL_CONVERSION(int16_t, Int16Type)
ARROW_STL_CONVERSION(int32_t, Int32Type)
ARROW_STL_CONVERSION(int64_t, Int64Type)
ARROW_STL_CONVERSION(uint8_t, UInt8Type)
ARROW_STL_CONVERSION(uint16_t, UInt16Type)
ARROW_STL_CONVERSION(uint32_t, UInt32Type)
ARROW_STL_CONVERSION(uint64_t, UInt64Type)
ARROW_STL_CONVERSION(float, FloatType)
ARROW_STL_CONVERSION(double, DoubleType)

template <>
struct ConversionTraits<std::string> : public CTypeTraits<std::string> {
  static Status AppendRow(StringBuilder& builder, const std::string& cell) {
    return builder.Append(cell);
  }
  static std::string GetEntry(const StringArray& array, size_t j) {
    return array.GetString(j);
  }
};

/// Append cell range elements as a single value to the list builder.
///
/// Cell range will be added to child builder using AppendListValues<ValueCType>()
/// if provided. AppendListValues<ValueCType>() has a default implementation, but
/// it can be specialized by users.
template <typename ValueCType, typename ListBuilderType, typename Range>
Status AppendCellRange(ListBuilderType& builder, Range&& cell_range) {
  constexpr bool is_list_builder = std::is_same<ListBuilderType, ListBuilder>::value;
  constexpr bool is_large_list_builder =
      std::is_same<ListBuilderType, LargeListBuilder>::value;
  static_assert(
      is_list_builder || is_large_list_builder,
      "Builder type must be either ListBuilder or LargeListBuilder for appending "
      "multiple rows.");

  using ChildBuilderType = CBuilderType<ValueCType>;
  ARROW_RETURN_NOT_OK(builder.Append());
  auto& value_builder =
      ::arrow::internal::checked_cast<ChildBuilderType&>(*builder.value_builder());

  // XXX: Remove appended value before returning if status isn't OK?
  return AppendListValues<ValueCType>(value_builder, std::forward<Range>(cell_range));
}

template <typename ValueCType>
struct ConversionTraits<std::vector<ValueCType>>
    : public CTypeTraits<std::vector<ValueCType>> {
  static Status AppendRow(ListBuilder& builder, const std::vector<ValueCType>& cell) {
    return AppendCellRange<ValueCType>(builder, cell);
  }

  static std::vector<ValueCType> GetEntry(const ListArray& array, size_t j) {
    using ElementArrayType =
        typename TypeTraits<typename ConversionTraits<ValueCType>::ArrowType>::ArrayType;

    const ElementArrayType& value_array =
        ::arrow::internal::checked_cast<const ElementArrayType&>(*array.values());

    std::vector<ValueCType> vec(array.value_length(j));
    for (int64_t i = 0; i < array.value_length(j); i++) {
      vec[i] =
          ConversionTraits<ValueCType>::GetEntry(value_array, array.value_offset(j) + i);
    }
    return vec;
  }
};

template <typename Optional>
struct ConversionTraits<Optional, enable_if_optional_like<Optional>>
    : public CTypeTraits<typename std::decay<decltype(*std::declval<Optional>())>::type> {
  using OptionalInnerType =
      typename std::decay<decltype(*std::declval<Optional>())>::type;
  using typename CTypeTraits<OptionalInnerType>::ArrowType;
  using CTypeTraits<OptionalInnerType>::type_singleton;

  static Status AppendRow(typename TypeTraits<ArrowType>::BuilderType& builder,
                          const Optional& cell) {
    if (cell) {
      return ConversionTraits<OptionalInnerType>::AppendRow(builder, *cell);
    } else {
      return builder.AppendNull();
    }
  }
};

/// Build an arrow::Schema based upon the types defined in a std::tuple-like structure.
///
/// While the type information is available at compile-time, we still need to add the
/// column names at runtime, thus these methods are not constexpr.
template <typename Tuple, std::size_t N = std::tuple_size<Tuple>::value>
struct SchemaFromTuple {
  using Element = internal::BareTupleElement<N - 1, Tuple>;

  // Implementations that take a vector-like object for the column names.

  /// Recursively build a vector of arrow::Field from the defined types.
  ///
  /// In most cases MakeSchema is the better entrypoint for the Schema creation.
  static std::vector<std::shared_ptr<Field>> MakeSchemaRecursion(
      const std::vector<std::string>& names) {
    std::vector<std::shared_ptr<Field>> ret =
        SchemaFromTuple<Tuple, N - 1>::MakeSchemaRecursion(names);
    auto type = ConversionTraits<Element>::type_singleton();
    ret.push_back(field(names[N - 1], type, internal::is_optional_like<Element>::value));
    return ret;
  }

  /// Build a Schema from the types of the tuple-like structure passed in as template
  /// parameter assign the column names at runtime.
  ///
  /// An example usage of this API can look like the following:
  ///
  /// \code{.cpp}
  /// using TupleType = std::tuple<int, std::vector<std::string>>;
  /// std::shared_ptr<Schema> schema =
  ///   SchemaFromTuple<TupleType>::MakeSchema({"int_column", "list_of_strings_column"});
  /// \endcode
  static std::shared_ptr<Schema> MakeSchema(const std::vector<std::string>& names) {
    return std::make_shared<Schema>(MakeSchemaRecursion(names));
  }

  // Implementations that take a tuple-like object for the column names.

  /// Recursively build a vector of arrow::Field from the defined types.
  ///
  /// In most cases MakeSchema is the better entrypoint for the Schema creation.
  template <typename NamesTuple>
  static std::vector<std::shared_ptr<Field>> MakeSchemaRecursionT(
      const NamesTuple& names) {
    using std::get;

    std::vector<std::shared_ptr<Field>> ret =
        SchemaFromTuple<Tuple, N - 1>::MakeSchemaRecursionT(names);
    std::shared_ptr<DataType> type = ConversionTraits<Element>::type_singleton();
    ret.push_back(
        field(get<N - 1>(names), type, internal::is_optional_like<Element>::value));
    return ret;
  }

  /// Build a Schema from the types of the tuple-like structure passed in as template
  /// parameter assign the column names at runtime.
  ///
  /// An example usage of this API can look like the following:
  ///
  /// \code{.cpp}
  /// using TupleType = std::tuple<int, std::vector<std::string>>;
  /// std::shared_ptr<Schema> schema =
  ///   SchemaFromTuple<TupleType>::MakeSchema({"int_column", "list_of_strings_column"});
  /// \endcode
  template <typename NamesTuple>
  static std::shared_ptr<Schema> MakeSchema(const NamesTuple& names) {
    return std::make_shared<Schema>(MakeSchemaRecursionT<NamesTuple>(names));
  }
};

template <typename Tuple>
struct SchemaFromTuple<Tuple, 0> {
  static std::vector<std::shared_ptr<Field>> MakeSchemaRecursion(
      const std::vector<std::string>& names) {
    std::vector<std::shared_ptr<Field>> ret;
    ret.reserve(names.size());
    return ret;
  }

  template <typename NamesTuple>
  static std::vector<std::shared_ptr<Field>> MakeSchemaRecursionT(
      const NamesTuple& names) {
    std::vector<std::shared_ptr<Field>> ret;
    ret.reserve(std::tuple_size<NamesTuple>::value);
    return ret;
  }
};

namespace internal {

template <typename Tuple, std::size_t N = std::tuple_size<Tuple>::value>
struct CreateBuildersRecursive {
  static Status Make(MemoryPool* pool,
                     std::vector<std::unique_ptr<ArrayBuilder>>* builders) {
    using Element = BareTupleElement<N - 1, Tuple>;
    std::shared_ptr<DataType> type = ConversionTraits<Element>::type_singleton();
    ARROW_RETURN_NOT_OK(MakeBuilder(pool, type, &builders->at(N - 1)));

    return CreateBuildersRecursive<Tuple, N - 1>::Make(pool, builders);
  }
};

template <typename Tuple>
struct CreateBuildersRecursive<Tuple, 0> {
  static Status Make(MemoryPool*, std::vector<std::unique_ptr<ArrayBuilder>>*) {
    return Status::OK();
  }
};

template <typename Tuple, std::size_t N = std::tuple_size<Tuple>::value>
struct RowIterator {
  static Status Append(const std::vector<std::unique_ptr<ArrayBuilder>>& builders,
                       const Tuple& row) {
    using std::get;
    using Element = BareTupleElement<N - 1, Tuple>;
    using BuilderType =
        typename TypeTraits<typename ConversionTraits<Element>::ArrowType>::BuilderType;

    BuilderType& builder =
        ::arrow::internal::checked_cast<BuilderType&>(*builders[N - 1]);
    ARROW_RETURN_NOT_OK(ConversionTraits<Element>::AppendRow(builder, get<N - 1>(row)));

    return RowIterator<Tuple, N - 1>::Append(builders, row);
  }
};

template <typename Tuple>
struct RowIterator<Tuple, 0> {
  static Status Append(const std::vector<std::unique_ptr<ArrayBuilder>>& builders,
                       const Tuple& row) {
    return Status::OK();
  }
};

template <typename Tuple, std::size_t N = std::tuple_size<Tuple>::value>
struct EnsureColumnTypes {
  static Status Cast(const Table& table, std::shared_ptr<Table>* table_owner,
                     const compute::CastOptions& cast_options,
                     compute::FunctionContext* ctx,
                     std::reference_wrapper<const ::arrow::Table>* result) {
    using Element = BareTupleElement<N - 1, Tuple>;
    std::shared_ptr<DataType> expected_type = ConversionTraits<Element>::type_singleton();

    if (!table.schema()->field(N - 1)->type()->Equals(*expected_type)) {
      compute::Datum casted;
      ARROW_RETURN_NOT_OK(compute::Cast(ctx, compute::Datum(table.column(N - 1)),
                                        expected_type, cast_options, &casted));
      auto new_field = table.schema()->field(N - 1)->WithType(expected_type);
      ARROW_RETURN_NOT_OK(
          table.SetColumn(N - 1, new_field, casted.chunked_array(), table_owner));
      *result = **table_owner;
    }

    return EnsureColumnTypes<Tuple, N - 1>::Cast(result->get(), table_owner, cast_options,
                                                 ctx, result);
  }
};

template <typename Tuple>
struct EnsureColumnTypes<Tuple, 0> {
  static Status Cast(const Table& table, std::shared_ptr<Table>* table_ownder,
                     const compute::CastOptions& cast_options,
                     compute::FunctionContext* ctx,
                     std::reference_wrapper<const ::arrow::Table>* result) {
    return Status::OK();
  }
};

template <typename Range, typename Tuple, std::size_t N = std::tuple_size<Tuple>::value>
struct TupleSetter {
  static void Fill(const Table& table, Range* rows) {
    using std::get;
    using Element = typename std::tuple_element<N - 1, Tuple>::type;
    using ArrayType =
        typename TypeTraits<typename ConversionTraits<Element>::ArrowType>::ArrayType;

    auto iter = rows->begin();
    const ChunkedArray& chunked_array = *table.column(N - 1);
    for (int i = 0; i < chunked_array.num_chunks(); i++) {
      const ArrayType& array =
          ::arrow::internal::checked_cast<const ArrayType&>(*chunked_array.chunk(i));
      for (int64_t j = 0; j < array.length(); j++) {
        get<N - 1>(*iter++) = ConversionTraits<Element>::GetEntry(array, j);
      }
    }

    return TupleSetter<Range, Tuple, N - 1>::Fill(table, rows);
  }
};

template <typename Range, typename Tuple>
struct TupleSetter<Range, Tuple, 0> {
  static void Fill(const Table& table, Range* rows) {}
};

}  // namespace internal

template <typename Range>
Status TableFromTupleRange(MemoryPool* pool, Range&& rows,
                           const std::vector<std::string>& names,
                           std::shared_ptr<Table>* table) {
  using row_type = typename std::iterator_traits<decltype(std::begin(rows))>::value_type;
  constexpr std::size_t n_columns = std::tuple_size<row_type>::value;

  std::shared_ptr<Schema> schema = SchemaFromTuple<row_type>::MakeSchema(names);

  std::vector<std::unique_ptr<ArrayBuilder>> builders(n_columns);
  ARROW_RETURN_NOT_OK(internal::CreateBuildersRecursive<row_type>::Make(pool, &builders));

  for (auto const& row : rows) {
    ARROW_RETURN_NOT_OK(internal::RowIterator<row_type>::Append(builders, row));
  }

  std::vector<std::shared_ptr<Array>> arrays;
  for (auto const& builder : builders) {
    std::shared_ptr<Array> array;
    ARROW_RETURN_NOT_OK(builder->Finish(&array));
    arrays.emplace_back(array);
  }

  *table = Table::Make(schema, arrays);

  return Status::OK();
}

template <typename Range>
Status TupleRangeFromTable(const Table& table, const compute::CastOptions& cast_options,
                           compute::FunctionContext* ctx, Range* rows) {
  using row_type = typename std::decay<decltype(*std::begin(*rows))>::type;
  constexpr std::size_t n_columns = std::tuple_size<row_type>::value;

  if (table.schema()->num_fields() != n_columns) {
    std::stringstream ss;
    ss << "Number of columns in the table does not match the width of the target: ";
    ss << table.schema()->num_fields() << " != " << n_columns;
    return Status::Invalid(ss.str());
  }

  // TODO: Use std::size with C++17
  if (rows->size() != static_cast<size_t>(table.num_rows())) {
    std::stringstream ss;
    ss << "Number of rows in the table does not match the size of the target: ";
    ss << table.num_rows() << " != " << rows->size();
    return Status::Invalid(ss.str());
  }

  // Check that all columns have the correct type, otherwise cast them.
  std::shared_ptr<Table> table_owner;
  std::reference_wrapper<const ::arrow::Table> current_table(table);

  ARROW_RETURN_NOT_OK(internal::EnsureColumnTypes<row_type>::Cast(
      table, &table_owner, cast_options, ctx, &current_table));

  internal::TupleSetter<Range, row_type>::Fill(current_table.get(), rows);

  return Status::OK();
}

/// \brief A STL allocator delegating allocations to a Arrow MemoryPool
template <class T>
class allocator {
 public:
  using value_type = T;
  using pointer = T*;
  using const_pointer = const T*;
  using reference = T&;
  using const_reference = const T&;
  using size_type = std::size_t;
  using difference_type = std::ptrdiff_t;

  template <class U>
  struct rebind {
    using other = allocator<U>;
  };

  /// \brief Construct an allocator from the default MemoryPool
  allocator() noexcept : pool_(default_memory_pool()) {}
  /// \brief Construct an allocator from the given MemoryPool
  explicit allocator(MemoryPool* pool) noexcept : pool_(pool) {}

  template <class U>
  allocator(const allocator<U>& rhs) noexcept : pool_(rhs.pool_) {}

  ~allocator() { pool_ = NULLPTR; }

  pointer address(reference r) const noexcept { return std::addressof(r); }

  const_pointer address(const_reference r) const noexcept { return std::addressof(r); }

  pointer allocate(size_type n, const void* /*hint*/ = NULLPTR) {
    uint8_t* data;
    Status s = pool_->Allocate(n * sizeof(T), &data);
    if (!s.ok()) throw std::bad_alloc();
    return reinterpret_cast<pointer>(data);
  }

  void deallocate(pointer p, size_type n) {
    pool_->Free(reinterpret_cast<uint8_t*>(p), n * sizeof(T));
  }

  size_type size_max() const noexcept { return size_type(-1) / sizeof(T); }

  template <class U, class... Args>
  void construct(U* p, Args&&... args) {
    new (reinterpret_cast<void*>(p)) U(std::forward<Args>(args)...);
  }

  template <class U>
  void destroy(U* p) {
    p->~U();
  }

  MemoryPool* pool() const noexcept { return pool_; }

 private:
  MemoryPool* pool_;
};

/// \brief A MemoryPool implementation delegating allocations to a STL allocator
///
/// Note that STL allocators don't provide a resizing operation, and therefore
/// any buffer resizes will do a full reallocation and copy.
template <typename Allocator = std::allocator<uint8_t>>
class STLMemoryPool : public MemoryPool {
 public:
  /// \brief Construct a memory pool from the given allocator
  explicit STLMemoryPool(const Allocator& alloc) : alloc_(alloc) {}

  Status Allocate(int64_t size, uint8_t** out) override {
    try {
      *out = alloc_.allocate(size);
    } catch (std::bad_alloc& e) {
      return Status::OutOfMemory(e.what());
    }
    stats_.UpdateAllocatedBytes(size);
    return Status::OK();
  }

  Status Reallocate(int64_t old_size, int64_t new_size, uint8_t** ptr) override {
    uint8_t* old_ptr = *ptr;
    try {
      *ptr = alloc_.allocate(new_size);
    } catch (std::bad_alloc& e) {
      return Status::OutOfMemory(e.what());
    }
    memcpy(*ptr, old_ptr, std::min(old_size, new_size));
    alloc_.deallocate(old_ptr, old_size);
    stats_.UpdateAllocatedBytes(new_size - old_size);
    return Status::OK();
  }

  void Free(uint8_t* buffer, int64_t size) override {
    alloc_.deallocate(buffer, size);
    stats_.UpdateAllocatedBytes(-size);
  }

  int64_t bytes_allocated() const override { return stats_.bytes_allocated(); }

  int64_t max_memory() const override { return stats_.max_memory(); }

  std::string backend_name() const override { return "stl"; }

 private:
  Allocator alloc_;
  arrow::internal::MemoryPoolStats stats_;
};

template <class T1, class T2>
bool operator==(const allocator<T1>& lhs, const allocator<T2>& rhs) noexcept {
  return lhs.pool() == rhs.pool();
}

template <class T1, class T2>
bool operator!=(const allocator<T1>& lhs, const allocator<T2>& rhs) noexcept {
  return !(lhs == rhs);
}

}  // namespace stl

}  // namespace arrow

#endif  // ARROW_STL_H
