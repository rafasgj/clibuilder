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

"""clidesc example: application with a colored formated output."""

import yaml

from clidesc import CLIDesc

__CLI_CONFIGURATION = """
---
program: output
description: Auto-formatting colored output.
version: 1.0
handler: output.fancy_greet
output:
  format: "{WHITE}Hello, {BG_RED}{someone}{BG_BLACK}!"
arguments:
  - name: someone
    required: true
    description: Someone to greet, in color.
"""


def fancy_greet(someone):
    """Greet someone, with color."""
    return {"someone": someone}


if __name__ == "__main__":
    CLIDesc(yaml.safe_load(__CLI_CONFIGURATION)).run()
