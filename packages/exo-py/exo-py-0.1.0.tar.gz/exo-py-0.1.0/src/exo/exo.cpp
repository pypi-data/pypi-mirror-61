/* ============================================================================
 * Copyright (c) 2020 Jared Duffey - All Rights Reserved
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

#include "exo/exo.hpp"

#include <cmath>
#include <map>
#include <numeric>
#include <utility>

namespace
{
using cache_map = std::map<size_t, std::vector<std::pair<size_t, size_t>>>;

void generate_pairs(cache_map& cache, size_t k)
{
  for(size_t i = 1; i < k; i++)
  {
    for(size_t j = 1; j < k; j++)
    {
      if(i + j != k)
      {
        continue;
      }

      cache[k].emplace_back(i, j);
    }
  }
}

double dnk_dt(nonstd::span<const double> data, cache_map& cache, double A, size_t k)
{
  if(!(cache.count(k) > 0))
  {
    generate_pairs(cache, k);
  }

  double increase = 0.0;

  const auto& pairs = cache[k];

  for(const auto& [i, j] : pairs)
  {
    increase += data[i - 1] * data[j - 1];
  }

  increase *= 0.5 * A;

  double decrease = 0.0;

  if(data[k - 1] != 0.0)
  {
    decrease += std::accumulate(data.cbegin(), data.cend(), 0.0);
    decrease *= A * data[k - 1];
  }

  return increase - decrease;
}

double dnk_dt(nonstd::span<const double> data, cache_map& cache, exo::matrix_span<const double> A, size_t k)
{
  if(!(cache.count(k) > 0))
  {
    generate_pairs(cache, k);
  }

  double increase = 0.0;

  const auto& pairs = cache[k];

  for(const auto& [i, j] : pairs)
  {
    increase += data[i - 1] * data[j - 1] * A(i - 1, j - 1);
  }

  increase *= 0.5;

  double decrease = 0.0;

  if(data[k - 1] != 0.0)
  {
    for(size_t i = 0; i < data.size(); i++)
    {
      decrease += A(i, k - 1) * data[i];
    }
    decrease *= data[k - 1];
  }

  return increase - decrease;
}

void step(nonstd::span<const double> data, nonstd::span<double> output, cache_map& cache, double A, double dt)
{
  for(size_t i = 0; i < data.size(); i++)
  {
    output[i] = (dnk_dt(data, cache, A, i + 1) * dt) + data[i];
  }
}

void step(nonstd::span<const double> data, nonstd::span<double> output, cache_map& cache, exo::matrix_span<const double> A,
          double dt)
{
  for(size_t i = 0; i < data.size(); i++)
  {
    output[i] = (dnk_dt(data, cache, A, i + 1) * dt) + data[i];
  }
}
} // namespace

namespace exo
{
std::vector<double> compute_nk(nonstd::span<const double> steps, double A, size_t k_max, double initial)
{
  std::vector<double> nk(steps.size() * k_max, 0.0);

  cache_map cache;

  nk[0] = initial;

  for(size_t i = 1; i < steps.size(); i++)
  {
    size_t row_data = (i - 1) * k_max;
    size_t row_ouput = i * k_max;
    nonstd::span<const double> data(nk.data() + row_data, k_max);
    nonstd::span<double> output(nk.data() + row_ouput, k_max);
    double dt = steps[i] - steps[i - 1];
    step(data, output, cache, A, dt);
  }

  return nk;
}

std::vector<double> compute_nk(nonstd::span<const double> steps, matrix_span<const double> A, double initial)
{
  size_t k_max = A.rows();
  std::vector<double> nk(steps.size() * k_max, 0.0);

  cache_map cache;

  nk[0] = initial;

  for(size_t i = 1; i < steps.size(); i++)
  {
    size_t row_data = (i - 1) * k_max;
    size_t row_ouput = i * k_max;
    nonstd::span<const double> data(nk.data() + row_data, k_max);
    nonstd::span<double> output(nk.data() + row_ouput, k_max);
    double dt = steps[i] - steps[i - 1];
    step(data, output, cache, A, dt);
  }

  return nk;
}
} // namespace exo
