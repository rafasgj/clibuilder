# This file is part of clidesc
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

"""Steps to test exception handling."""

import sys
from importlib import import_module
from unittest.mock import MagicMock

from behave import given, then


@given('a function named "{fun_name}" raises {exception}, with message "{msg}"')
def _given_function_raises_exception(context, exception, msg, fun_name):
    def get_class(cls):
        *module, kls = cls.split(".")
        mod = import_module(".".join(module or ["builtins"]))
        return getattr(mod, kls)

    def side_effect(**kwargs):
        raise get_class(exception)(msg)

    *module, function = fun_name.split(".")
    context.mock_fun = MagicMock(
        **{function: MagicMock(side_effect=side_effect)}
    )
    sys.modules[".".join(module)] = context.mock_fun


@then("exception {exception} is raised")
def _then_exception_raised(context, exception):
    assert type(context.exception).__name__ == exception, "Exception mismatch."
