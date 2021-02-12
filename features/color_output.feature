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

@stdout @stderr
Feature: Automatic ANSI color terminal output.

Scenario: Simple colorized output.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          someone:
            no_key: yes
            format: "Hello, {WHITE}{someone}{RESET}!"
        arguments:
          - name: someone
            description: Someone to greet.
            required: yes
        """
        And a function "greeting.hello"
    When the application is executed with [World]
    Then the color output is equivalent to
        """
        Hello, {WHITE}World{RESET}!
        """

Scenario: Output of a list of values, enumerating items, global default colored.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          colorize: yes
          someone:
            enumerate: yes
        arguments:
          - name: someone
            description: Someone to greet.
            required: yes
            nargs: +
        """
        And a function "greeting.hello"
    When the application is executed with [John, Jack, Jill]
    Then no exception is raised
        And the color output is equivalent to
            """
            someone:
                {WHITE}1.{RESET} John
                {WHITE}2.{RESET} Jack
                {WHITE}3.{RESET} Jill
            """


Scenario: Output of a list of values, enumerating items, attribute default colored.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          someone:
            colorize: yes
            enumerate: yes
        arguments:
          - name: someone
            description: Someone to greet.
            required: yes
            nargs: +
        """
        And a function "greeting.hello"
    When the application is executed with [John, Jack, Jill]
    Then no exception is raised
        And the color output is equivalent to
            """
            someone:
                {WHITE}1.{RESET} John
                {WHITE}2.{RESET} Jack
                {WHITE}3.{RESET} Jill
            """
