/* ============================================================================
 * Copyright (c) 2020 Jared Duffey - All Rights Reserved
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

#include "pybind11/pybind11.h"

#include "pybind11/numpy.h"
#include "pybind11/stl.h"

#include "exo/exo.hpp"

namespace
{
namespace py = pybind11;
using py_arrayd = py::array_t<double, py::array::c_style | py::array::forcecast>;

template <typename Container, typename = std::enable_if_t<std::is_rvalue_reference_v<Container&&>>>
py::array_t<typename Container::value_type> py_array_move(Container&& data, const py::array::ShapeContainer& shape)
{
  Container* ptr = new Container(std::move(data));
  auto capsule = py::capsule(ptr, [](void* p) { delete reinterpret_cast<Container*>(p); });
  return std::move(py::array(shape, ptr->data(), capsule));
}

auto py_compute_nk_approx(py_arrayd steps, double A, size_t k_max, double initial)
{
  if(k_max == 0)
  {
    throw std::invalid_argument("k_max must be non-zero");
  }

  if(steps.size() == 0)
  {
    throw std::invalid_argument("steps must be non-empty");
  }

  std::vector<double> nk = exo::compute_nk(steps, A, k_max, initial);
  std::vector<ssize_t> shape{steps.size(), static_cast<ssize_t>(k_max)};
  return py_array_move(std::move(nk), std::move(shape));
}

auto py_compute_nk(py_arrayd steps, py_arrayd A, double initial)
{
  ssize_t ndim = A.ndim();
  if(ndim != 2)
  {
    throw std::invalid_argument("A must be 2D");
  }

  if(A.shape(0) != A.shape(1))
  {
    throw std::invalid_argument("A must be N x N");
  }

  size_t k_max = static_cast<size_t>(A.shape(0));

  if(k_max == 0)
  {
    throw std::invalid_argument("A must be non-empty");
  }

  if(steps.size() == 0)
  {
    throw std::invalid_argument("steps must be non-empty");
  }

  exo::matrix_span<const double> matrix(A, k_max);

  std::vector<double> nk = exo::compute_nk(steps, matrix, initial);
  std::vector<ssize_t> shape{steps.size(), static_cast<ssize_t>(k_max)};
  return py_array_move(std::move(nk), std::move(shape));
}
} // namespace

PYBIND11_MODULE(exopy, m)
{
  using namespace pybind11::literals;
  m.doc() = "exopy";

  m.def("compute_nk", &py_compute_nk,
        "Models the growth of planetesimals in a disk using the Smoluchowski coagulation equation. "
        "Returns a 2D array with each row representing all nk for that time step.",
        "steps"_a, "A"_a, "initial"_a);

  m.def("compute_nk_approx", &py_compute_nk_approx,
        "Models the growth of planetesimals in a disk using the Smoluchowski coagulation equation. "
        "Assumes all collision terms are the same constant A. Returns a 2D array with each row "
        "representing all nk for that time step.",
        "steps"_a, "A"_a, "k_max"_a, "initial"_a);
}
