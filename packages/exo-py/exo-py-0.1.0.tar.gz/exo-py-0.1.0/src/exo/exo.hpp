/* ============================================================================
 * Copyright (c) 2020 Jared Duffey - All Rights Reserved
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 * ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ */

#pragma once

#include <vector>

#include "nonstd/span.hpp"

#include "exo/matrix_span.hpp"

namespace exo
{
/**
 * Models the growth of planetesimals in a disk using the Smoluchowski coagulation equation.
 * Returns a 2D array with each row representing all nk for that time step.
 *
 * @param steps span of steps
 * @param A span of 2D matrix of collision terms (k x k)
 * @param initial initial value of nk[0][0]
 * @return 2D array of nk
 */
std::vector<double> compute_nk(nonstd::span<const double> steps, matrix_span<const double> A, double initial);

/**
 * Models the growth of planetesimals in a disk using the Smoluchowski coagulation equation.
 * This overload assumes all collision terms are the same constant A.
 * Returns a 2D array with each row representing all nk for that time step.
 *
 * @param steps span of steps
 * @param A collision term
 * @param k_max number of nk to compute
 * @param initial initial value of nk[0][0]
 * @return 2D array of nk
 */
std::vector<double> compute_nk(nonstd::span<const double> steps, double A, size_t k_max, double initial);
} // namespace exo
