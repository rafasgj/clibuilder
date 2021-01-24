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

Scenario: Simple string output.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output: yes
        """
        And a function that returns "a string" of type string named "greeting.hello"
    When the application is executed without parameters
    Then the output is
        """
        a string
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

Scenario: Output of a list of values, enumerating items.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
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
    Then the output is
        """
        someone:
            1. John
            2. Jack
            3. Jill
        """

Scenario: Output of a list of values, enumerating items, starting with 0.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          someone:
            enumerate: 0
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
            0. John
            1. Jack
            2. Jill
        """

Scenario: Output of a list of values, explicitly disabling enumeration.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          someone:
            enumerate: False
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

Scenario: Output of a list of values, with member formatting.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          someone: "{_index}: {_item}"
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
        1: John
        2: Jack
        3: Jill
        """

Scenario: Output of a list of values, with member formatting, and no key.
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
            format: "{_index}: {_item}"
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
        1: John
        2: Jack
        3: Jill
        """

Scenario: Output of a list of values, with no key.
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
        - John
        - Jack
        - Jill
        """

Scenario: Output of a numbered list of values, starting with 0, less padding.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          padding: 2
          someone:
            enumerate: 0
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
          0. John
          1. Jack
          2. Jill
        """

Scenario: Output of a numbered list of values, starting with 0, no padding.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output:
          padding: no
          someone:
            enumerate: 0
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
        0. John
        1. Jack
        2. Jill
        """

Scenario: Output of a handler that returns `None`.
    Given the CLI description
        """
        ---
        program: greeting
        description: A greeting application.
        version: 1.0
        handler: greeting.hello
        output: yes
        """
        And a function returning nothing, named "greeting.hello"
    When the application is executed without parameters
    Then the output is empty
