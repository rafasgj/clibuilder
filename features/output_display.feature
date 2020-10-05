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

@stdout @stderr
Feature: Automatic output of command handlers.

Scenario: Simple formatted output.
Given the CLI description
    """
    ---
    program: greeting
    description: A greeting application.
    version: 1.0
    handler: greeting.hello
    output: >
      Hello, {someone}!
    arguments:
      - name: someone
        description: Someone to greet.
        required: yes
    """
    And a function "greeting.hello"
When the application is executed with [World]
Then the output is
    """
    Hello, World!
    """

Scenario: Simple unformatted output.
Given the CLI description
    """
    ---
    program: greeting
    description: A greeting application.
    version: 1.0
    handler: greeting.hello
    output: yes
    arguments:
      - name: someone
        description: Someone to greet.
        required: yes
    """
    And a function "greeting.hello"
When the application is executed with [John]
Then the output is
    """
    someone: John
    """

Scenario: Output of a list of values.
Given the CLI description
    """
    ---
    program: greeting
    description: A greeting application.
    version: 1.0
    handler: greeting.hello
    output: yes
    arguments:
      - name: someone
        description: Someone to greet.
        required: yes
        nargs: +
    """
    And a function "greeting.hello"
When the application is executed with [John, Jack, Jill]
Then the output is
    """
    someone:
        - John
        - Jack
        - Jill
    """
