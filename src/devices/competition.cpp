/**
 * \file devices/competition.cpp
 *
 * Contains competition control functions.
 *
 * \copyright Copyright (c) 2017-2024, Purdue University ACM SIGBots.
 * All rights reserved.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/.
 */

#include "kapi.h"

namespace pros {
namespace competition {
using namespace pros::c;
std::uint8_t get_status(void) {
	return competition_get_status();
}

std::uint8_t is_autonomous(void) {
	return competition_is_autonomous();
}

std::uint8_t is_connected(void) {
	return competition_is_connected();
}

std::uint8_t is_disabled(void) {
	return competition_is_disabled();
}

std::uint8_t is_field_control(void) {
	return competition_is_field();
}

std::uint8_t is_competition_switch(void) {
	return competition_is_switch();
}

}  // namespace competition
}  // namespace pros
