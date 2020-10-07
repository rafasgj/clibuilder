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

"""autocli example: Application with multiple commands."""

import yaml

from autocli.autocli import AutoCLI

__CLI_CONFIGURATION = """
---
program: multi
description: A multi-command application.
version: 1.0
sub_commands:
  title: Commands
  description: Application sub-commands
  group_name: Sub commands
  commands:
    - name: abc
      description: First command.
      handler: multicommand.abc
      arguments:
      - name: some_arg
        description: Some argument.
    - name: xyz
      description: Second command.
      handler: multicommand.xyz
      arguments:
      - name: another_arg
        description: Another argument.
"""


def abc(some_arg):
    """Greet someone."""
    print(f"ABC: {some_arg}")


def xyz(another_arg):
    """Greet someone."""
    print(f"XYZ: {another_arg}")


if __name__ == "__main__":
    cli = AutoCLI(yaml.safe_load(__CLI_CONFIGURATION))
    cli.run()
