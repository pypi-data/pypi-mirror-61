/* ============================================================================
 * Copyright (c) 2020 Jared Duffey - All Rights Reserved
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

#pragma once

#include "nonstd/span.hpp"

namespace exo
{
template <class T>
class matrix_span
{
public:
  matrix_span(nonstd::span<T> span, size_t rows, size_t cols)
  : span_(span)
  , rows_(rows)
  , cols_(cols)
  {
    if(rows * cols != span.size())
    {
      throw std::invalid_argument("rows * cols must equal span.size()");
    }
  }

  matrix_span(nonstd::span<T> span, size_t n)
  : matrix_span(span, n, n)
  {
  }

  T& operator()(size_t i, size_t j)
  {
    return span_[i * rows_ + j];
  }

  const T& operator()(size_t i, size_t j) const
  {
    return span_[i * rows_ + j];
  }

  inline size_t rows() const
  {
    return rows_;
  }

  inline size_t cols() const
  {
    return cols_;
  }

private:
  nonstd::span<T> span_;
  size_t rows_ = 0;
  size_t cols_ = 0;
};
} // namespace exo
