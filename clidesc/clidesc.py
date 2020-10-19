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

"""clidesc implementation."""

import re
from argparse import ArgumentParser
import importlib

try:
    import yaml
except ImportError:
    pass


class Object:  # pylint: disable=too-few-public-methods
    """Used to add attributes on demand."""


class CLIDesc:
    """Framework for CLI application creation."""

    @classmethod
    def from_file(cls, filename):
        """Load the CLI configuration from a YAML or JSON file."""
        with open(filename, "r") as cli_description:
            return cls(yaml.safe_load(cli_description.read()))

    def __init__(self, cli_description):
        """Initialize framework with the provided description."""
        self.__description = cli_description
        program = cli_description["program"]
        description = cli_description["description"]
        self.__argparse = ArgumentParser(prog=program, description=description)
        if "version" in cli_description:
            self.__argparse.add_argument(
                "--version",
                action="version",
                help="display program version",
                version=f"%(prog)s {cli_description['version']}",
            )

        self.configuration = Object()
        self.__non_parameters = []
        self.__output = {}
        self.__commands = {}
        self.__add_group(None, self.__argparse, program, cli_description)

    def __add_group(self, subparser, parser, command, cmd_description):
        handler = cmd_description.get("handler")
        if handler:
            self.__commands[f"{command}"] = handler
            self.__output[handler] = cmd_description.get("output")

        for argument in cmd_description.get("arguments", []):
            self.__add_argument(parser, argument)

        sub_commands = cmd_description.get("sub_commands", {})

        if sub_commands:
            sub_parser_args = {}
            for item in ["title", "description"]:
                if item in sub_commands:
                    sub_parser_args[item] = sub_commands[item]
            if "group_name" in sub_commands:
                sub_parser_args["metavar"] = sub_commands["group_name"]
            subparser = parser.add_subparsers(
                dest="_cli_command", **sub_parser_args
            )
            for cmd_group in sub_commands.get("commands"):
                new_parser = subparser.add_parser(
                    cmd_group["name"], help=cmd_group["description"]
                )
                self.__add_group(
                    subparser, new_parser, cmd_group["name"], cmd_group
                )

    def run(self, argv=None):
        """Execute the CLI application."""
        options = self.__argparse.parse_args(argv)
        args = vars(options)
        self.configuration = Object()
        for cfg in self.__non_parameters:
            if cfg in args:
                setattr(self.configuration, cfg, args[cfg])
                del args[cfg]

        if hasattr(options, "_cli_command"):
            # pylint: disable=protected-access
            method_name = options._cli_command
            del args["_cli_command"]
        else:
            method_name = self.__description["program"]
        if not method_name:
            raise Exception("Method name not defined.")
        if method_name not in self.__commands:
            raise Exception(f"Invalid command: {method_name}.")

        method_name = self.__commands[method_name]
        output = self.__output[method_name]

        # execute function
        *module, function = method_name.split(".")
        mod = importlib.import_module(".".join(module))
        handler = getattr(mod, function)
        result = handler(**args)
        if output:
            if isinstance(result, dict):
                if isinstance(output, dict):
                    print(output["format"].format(**result))
                if isinstance(output, str):
                    print(output.format(**result))
                else:
                    self.display(result)
            else:
                self.display(result)
        return result

    def __add_argument(self, parser, argument):
        default = argument.get("default")
        arg_type = {
            "count": (int, "count", 0),
            "int": (int, "store"),
            "integer": (int, "store"),
            "str": (str, "store"),
            "string": (str, "store"),
            "float": (float, "store"),
            "boolean": (bool, "store_true" if default else "store_false"),
        }
        extra_args = {}

        description = argument["description"]
        required = argument.get("required", False)
        optional = argument.get("optional")

        datatype, action, *type_default = (
            arg_type.get(argument["type"], (str, "store"))
            if "type" in argument
            else (str, "store", None)
        )

        extra_args["action"] = action
        if type_default:
            extra_args["default"] = datatype(*type_default)
        if default is not None:
            extra_args["default"] = datatype(default)

        if optional:
            names = [f"--{argument['name']}"]
            if "abbrev" in argument:
                names.append(f"-{argument['abbrev']}")
            extra_args["required"] = required
        else:
            if "abbrev" in argument:
                raise Exception("Cannot use `abbrev` without `optional: yes`.")
            if argument.get("type", "string") not in ["bool", "boolean"]:
                if not required:
                    extra_args["nargs"] = "?"
            extra_args["type"] = datatype
            names = [argument["name"]]

        if "nargs" in argument:
            extra_args["nargs"] = argument["nargs"]

        if argument.get("configuration"):
            self.__non_parameters.append(
                names[0][re.search(r"[^-]", names[0]).start() :]
            )

        parser.add_argument(*names, help=description, **extra_args)

    @classmethod
    def display(cls, data, level=0):
        """Display the result of the API command."""
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    print("%s%s:" % (" " * (4 * level), key))
                    cls.display(value, level + 1)
                elif isinstance(value, list):
                    print("%s%s:" % (" " * (4 * level), key))
                    for item in value:
                        print("%s- %s" % (" " * 4 * (level + 1), item))
                else:
                    print("%s%s: %s" % (" " * (4 * level), key, value))
        elif isinstance(data, list):
            for entry in data:
                cls.display(entry, level)
                print("---")
        else:
            print(repr(data))
