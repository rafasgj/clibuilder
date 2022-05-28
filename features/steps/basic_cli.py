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

"""Basic CLI test steps."""

import re
import sys
import io
from unittest.mock import MagicMock, patch, mock_open, PropertyMock
import yaml

# pylint: disable=import-error, no-name-in-module
from behave import given, when, then
from behave_shared import text_compare_error_message

# pylint: enable=import-error, no-name-in-module


from clidesc import CLIDesc


def __run_application(context, params=None):
    try:
        context.cli.run(params)
    except SystemExit as sysexit:
        context.exit_code = sysexit.code
        context.exception = None
    except Exception as exception:  # pylint: disable=broad-except
        context.exception = exception
        context.exit_code = float("NaN")
    else:
        context.exception = None
        context.exit_code = 0


def __compare_output(expected, observed):
    """Compare expected text output with observed text."""
    expected = expected.strip()
    observed = observed.strip()
    assert observed == expected, text_compare_error_message(expected, observed)


def __regex_match_output(expected, observed):
    exp_regex = re.compile(re.escape(expected.strip()))
    observed = observed.strip()
    assert exp_regex.search(observed) is not None, text_compare_error_message(
        expected, observed
    )


def __patch_function(context, func_name, impl):
    *module, function = func_name.split(".")
    context.mock_fun = MagicMock(**{function: MagicMock(side_effect=impl)})
    sys.modules[".".join(module)] = context.mock_fun


@given("the CLI description")
def _given_cli_description(context):
    """Create clidesc from YAML/JSON text data."""
    context.cli_description = yaml.safe_load(context.text)
    context.cli = CLIDesc(context.cli_description)


@given('a function "{func}" that prints "{strfmt}"')
def _given_a_function_with_one_arg_that_prints(context, func, strfmt):
    def side_effect(**kwargs):
        print(strfmt.format(**kwargs))

    __patch_function(context, func, side_effect)


@when("the application is executed without parameters")
def _when_run_application_without_parameters(context):
    __run_application(context, None)


@then("the output is")
def _then_output_is(context):
    __compare_output(context.text, context.stdout.getvalue())
    context.stdout = io.StringIO()


@then("the output contains")
def _then_output_matches(context):
    stdout = context.stdout.getvalue()
    for expected in context.text.split("\n"):
        __regex_match_output(expected, stdout)
    context.stdout = io.StringIO()


@then("the error output is")
def _then_error_output_is(context):
    __compare_output(context.text, context.stderr.getvalue())
    context.stderr = io.StringIO()


@then("the exit code is not zero")
def _then_exit_code_is_not_zero(context):
    assert context.exit_code != 0


@then("the exit code is {exit_code:d}")
def _then_exit_code_is(context, exit_code):
    assert (
        context.exit_code == exit_code
    ), f"exit_code: {context.exit_code:d} / {exit_code:d}"


@when("the application is executed with [{param_list}]")
def _when_run_application_with_param(context, param_list):
    params = [p.strip() for p in param_list.split(",")]
    __run_application(context, params)


@then('the CLI configuration has attribute "{attribute}" with value {value}')
def _then_cli_configuration_has_attribute(context, attribute, value):
    assert hasattr(context.cli.configuration, attribute)
    assert str(getattr(context.cli.configuration, attribute)) == value


@given('a function "{func}"')
def _given_a_function(context, func):
    def side_effect(**kwargs):
        return kwargs

    __patch_function(context, func, side_effect)


@given('the the CLI description from the file "{filename}"')
def _given_cli_as_file(context, filename):
    try:
        with patch("builtins.open", mock_open(read_data=context.text)):
            context.cli = CLIDesc.from_file(filename)
    except Exception as error:  # pylint: disable=broad-except
        context.exception = error
    else:
        context.exception = None


@given('the module "{module}" has attribute "{attr}" with value "{value}"')
def _given_module_attribute(context, module, attr, value):
    context.mock_attr = MagicMock()
    attribute = PropertyMock(return_value=value)
    setattr(type(context.mock_attr), attr, attribute)
    sys.modules[module] = context.mock_attr


@given('a function that returns "{value}" of type {value_type} named "{func}"')
def _given_function_returning_builtin(context, func, value_type, value):
    def side_effect(*_args, **_kwargs):
        types = {
            "string": str,
            "str": str,
            "integer": int,
            "int": int,
            "boolean": bool,
            "bool": bool,
            "float": float,
        }
        return types[value_type](value)

    __patch_function(context, func, side_effect)


@given('a function returning nothing, named "{func}"')
def _given_function_return_none(context, func):
    def side_effect(**_):
        return None

    __patch_function(context, func, side_effect)


@then("the output is empty")
def _then_output_is_empty(context):
    __compare_output("", context.stdout.getvalue())
    context.stdout = io.StringIO()


@given('a function "{func}", returning')
def _given_function_with_return_table(context, func):
    def create_list(data):
        return [v.strip() for v in data.split(",")]

    def side_effect(**_):
        output = {}
        for row in data_table:
            types = {
                "string": str,
                "str": str,
                "list": create_list,
            }
            rfield, rtype, rvalue = [field.strip() for field in row]
            output[rfield] = types[rtype](rvalue.strip())
        return output

    data_table = context.table
    __patch_function(context, func, side_effect)


@then("no exception is raised")
def _then_no_exception(context):
    assert context.exception is None, f"Exception: {context.exception}"
