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

"""autocli example: application with a formated output."""

import yaml

from autocli import AutoCLI

__CLI_CONFIGURATION = """
---
program: output
description: Auto-formatting output.
version: 1.0
handler: output.hello
output:
  format: "Hello, {someone}"
arguments:
  - name: someone
    description: Someone to greet.
    required: true
"""


def hello(someone):
    """Greet someone."""
    return {"someone": someone}


if __name__ == "__main__":
    cli = AutoCLI(yaml.safe_load(__CLI_CONFIGURATION))
    cli.run()
