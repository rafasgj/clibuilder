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

"""Common test functions and classes."""


def text_compare_error_message(expected, observed):
    """Create an error message for text comparision."""
    return (
        f"Output mismatch: size = {len(expected)} / "
        + f"{len(observed)}\n---\n{expected}\n===\n{observed}\n---\n"
    )
