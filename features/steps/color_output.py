# This file is part of clidesc
#
# Copyright (C) 2021 Rafael Guterres Jeffman
#
# f/π is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

"""ANSI color output CLI test steps."""

import io

# pylint: disable=import-error, no-name-in-module
from behave import then
from behave_shared import text_compare_error_message

# pylint: enable=import-error, no-name-in-module


from clidesc import CLIDesc


@then("the color output is equivalent to")
def _then_color_output_is(context):
    # pylint: disable=protected-access
    expected = context.text.format(**CLIDesc._ansi_color_theme(True))
    # pylint: enable=protected-access
    observed = context.stdout.getvalue()
    msg = text_compare_error_message(expected, observed)
    expected = expected.strip().split("\n")
    observed = observed.strip().split("\n")
    context.stdout = io.StringIO()

    for exp in expected:
        for obs in observed:
            if obs.startswith(exp):
                break
        else:
            raise AssertionError(msg)
