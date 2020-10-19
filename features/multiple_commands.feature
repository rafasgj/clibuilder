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

@stdout @stderr
Feature: Allow definition of multiple commands.

Scenario: Multiple command help.
Given the CLI description
    """
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
          handler: multi.abc
          arguments:
          - name: some_arg
            description: Some argument.
        - name: xyz
          description: Second command.
          handler: multi.xyz
          arguments:
          - name: another_arg
            description: Another argument.
    """
When the application is executed with [--help]
Then the output is
    """
    usage: multi [-h] [--version] Sub commands ...

    A multi-command application.

    optional arguments:
      -h, --help    show this help message and exit
      --version     display program version

    Commands:
      Application sub-commands

      Sub commands
        abc         First command.
        xyz         Second command.
    """

Scenario: Multiple command, sub-command help.
Given the CLI description
    """
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
          handler: multi.abc
          arguments:
          - name: some_arg
            description: Some argument.
        - name: xyz
          description: Second command.
          handler: multi.xyz
          arguments:
          - name: another_arg
            description: Another argument.
    """
When the application is executed with [abc, --help]
Then the output is
    """
    usage: multi abc [-h] [some_arg]

    positional arguments:
      some_arg    Some argument.

    optional arguments:
      -h, --help  show this help message and exit
    """

Scenario: Multiple command, second sub-command help.
Given the CLI description
    """
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
          handler: multi.abc
          arguments:
          - name: some_arg
            description: Some argument.
        - name: xyz
          description: Second command.
          handler: multi.xyz
          arguments:
          - name: another_arg
            description: Another argument.
    """
When the application is executed with [xyz, --help]
Then the output is
    """
    usage: multi xyz [-h] [another_arg]

    positional arguments:
      another_arg  Another argument.

    optional arguments:
      -h, --help   show this help message and exit
    """

Scenario: Multiple command, first handler.
Given the CLI description
    """
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
          handler: multi.abc
          output: yes
          arguments:
          - name: some_arg
            description: Some argument.
        - name: xyz
          description: Second command.
          handler: multi.xyz
          output: yes
          arguments:
          - name: another_arg
            description: Another argument.
    """
    And a function "multi.abc"
When the application is executed with [abc, value]
Then the output is
    """
    some_arg: value
    """

Scenario: Multiple command, second handler.
Given the CLI description
    """
    ---
    program: multi
    description: A multi-command application.
    version: 1.0
    output: yes
    sub_commands:
      title: Commands
      description: Application sub-commands
      group_name: Sub commands
      commands:
        - name: abc
          description: First command.
          handler: multi.abc
          output: yes
          arguments:
          - name: some_arg
            description: Some argument.
        - name: xyz
          description: Second command.
          handler: multi.xyz
          output: yes
          arguments:
          - name: another_arg
            description: Another argument.
    """
    And a function "multi.xyz"
When the application is executed with [xyz, value]
Then the output is
    """
    another_arg: value
    """

Scenario: Multiple command levels.
Given the CLI description
    """
    ---
    program: multi
    description: A multi-command application.
    version: 1.0
    output: yes
    sub_commands:
      title: Commands
      description: Application sub-commands
      group_name: Sub commands
      commands:
        - name: abc
          description: First command.
          sub_commands:
              title: Inner commands
              description: Application inner-commands
              group_name: inner commands
              commands:
              - name: xyz
                description: Second command.
                handler: multi.xyz
                output: yes
                arguments:
                - name: another_arg
                  description: Another argument.
    """
    And a function "multi.xyz"
When the application is executed with [abc, xyz, value]
Then the output is
    """
    another_arg: value
    """
