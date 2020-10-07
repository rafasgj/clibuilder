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

"""autocli example: Greeting application."""

import os

from autocli import AutoCLI


def hello(someone):
    """Greet someone."""
    print(f"Hello, {someone}!")


if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__))
    cli = AutoCLI.from_file(os.path.join(path, "from_file.yml"))
    cli.run()
