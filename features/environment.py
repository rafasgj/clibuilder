# This file is part of autocli
#
# Copyright (C) 2020 Rafael Guterres Jeffman
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

"""Prepare test environment for behave."""

import sys
import io


def before_tag(context, tag):
    """Configure enviroment before tags."""
    if tag == "stdout":
        context.real_stdout = sys.stdout
        context.stdout = io.StringIO()
        sys.stdout = context.stdout
    if tag == "stderr":
        context.real_stderr = sys.stderr
        context.stderr = io.StringIO()
        sys.stderr = context.stderr


def after_tag(context, tag):
    """Cleanup enviroment after tags."""
    if tag == "stdout":
        sys.stdout = context.real_stdout
    if tag == "stderr":
        sys.stderr = context.real_stderr


def before_scenario(context, scenario):
    """Set scenario output capture."""
    if "stdout" in scenario.tags or "stdout" in scenario.feature.tags:
        context.stdout = io.StringIO()
        sys.stdout = context.stdout
    if "stderr" in scenario.tags or "stderr" in scenario.feature.tags:
        context.stderr = io.StringIO()
        sys.stderr = context.stderr
