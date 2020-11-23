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
Feature: Use defined types for attributes.

Scenario: Attribute with integer type.
    Given the CLI description
        """
        ---
        program: multi
        description: A multi-command application.
        version: 1.0
        handler: attrtype.check
        output: yes
        arguments:
        - name: argument
          description: Some integer argument.
          type: int
          optional: yes
        """
        And a function "attrtype.check"
    When the application is executed with [--argument, 2]
    Then the output is
        """
        argument: 2
        """
    When the application is executed with [--argument, 3.1415]
    Then the error output is
    """
    usage: multi [-h] [--version] [--argument ARGUMENT]
    multi: error: argument --argument: invalid int value: '3.1415'
    """

Scenario: Attribute with boolean type.
    Given the CLI description
        """
        ---
        program: multi
        description: A multi-command application.
        version: 1.0
        handler: attrtype.check
        output: yes
        arguments:
        - name: argument
          description: Some integer argument.
          type: bool
          optional: yes
        """
        And a function "attrtype.check"
    When the application is executed with [--argument]
    Then the output is
        """
        argument: True
        """
    When the application is executed with [--argument, 2]
    Then the error output is
        """
        usage: multi [-h] [--version] [--argument]
        multi: error: unrecognized arguments: 2
        """

Scenario: Attribute with float type.
    Given the CLI description
        """
        ---
        program: multi
        description: A multi-command application.
        version: 1.0
        handler: attrtype.check
        output: yes
        arguments:
        - name: argument
          description: Some integer argument.
          type: float
          optional: yes
        """
        And a function "attrtype.check"
    When the application is executed with [--argument, 3.1415]
    Then the output is
        """
        argument: 3.1415
        """
    When the application is executed with [--argument, a string]
    Then the error output is
    """
    usage: multi [-h] [--version] [--argument ARGUMENT]
    multi: error: argument --argument: invalid float value: 'a string'
    """
