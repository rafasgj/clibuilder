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

"""autocli implementation."""

import re
from argparse import ArgumentParser
import importlib


class Object:  # pylint: disable=too-few-public-methods
    """Used to add attributes on demand."""


class AutoCLI:
    """Framework for CLI application creation."""

    # pylint: disable=too-few-public-methods

    def __init__(self, cli_description):
        """Initialize framework with the provided description."""
        self.__description = cli_description
        self.__program = cli_description["program"]
        description = cli_description["description"]
        self.__version = str(cli_description.get("version"))
        self.__argparse = ArgumentParser(
            prog=self.__program, description=description
        )
        if self.__version:
            self.__argparse.add_argument(
                "--version",
                action="version",
                help="display program version",
                version=f"%(prog)s {self.__version}",
            )
        self.__commands = {f"{self.__program}": cli_description.get("handler")}
        self.configuration = Object()
        self.__non_parameters = []

        for argument in cli_description.get("arguments", []):
            self.__add_argument(self.__argparse, argument)

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
            del args[method_name]
        else:
            method_name = self.__program
        if not method_name:
            raise Exception("Method name not defined.")
        if method_name not in self.__commands:
            raise Exception(f"Invalid command: {method_name}.")

        method_name = self.__commands[method_name]

        # execute function
        *module, function = method_name.split(".")
        mod = importlib.import_module(".".join(module))
        handler = getattr(mod, function)
        handler(**args)

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

        type_default = None
        if "type" in argument:
            datatype, action, *type_default = arg_type.get(
                argument["type"], (str, "store")
            )
        else:
            action = "store"
            datatype = str

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

        if argument.get("configuration"):
            self.__non_parameters.append(
                names[0][re.search(r"[^-]", names[0]).start() :]
            )

        parser.add_argument(*names, help=description, **extra_args)
