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

"""Test to verify correctness of attributes in handlers."""

import yaml

from clidesc import CLIDesc


def test_attr_value_none():
    """Test if an attribute recieves None (NoneType) value."""
    description = """
---
program: test_for_none
description: Test an optional attribute.
version: 1.0
handler: conftest.simple_handler
arguments:
- name: fields
  abbrev: -f
  description: retrieve only this fields.
  optional: yes
  nargs: '*'
"""
    cli = CLIDesc(yaml.safe_load(description))
    result = cli.run([])
    assert result["fields"] is None, "Expected fields to be of NoneType."
