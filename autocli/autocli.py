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

from argparse import ArgumentParser
import importlib


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

        for argument in cli_description.get("arguments", []):
            self.__add_argument(self.__argparse, argument)

    def run(self, argv=None):
        """Execute the CLI application."""
        options = self.__argparse.parse_args(argv)
        args = vars(options)

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
        # pylint: disable=no-self-use
        flag = "flag" in argument
        if flag:
            if "name" in argument:
                raise Exception("Only one of `name` or `flag` can be used.")
        else:
            if "abbrev" in argument:
                raise Exception("Cannot use `abbrev` with `name`.")
        names = [
            argument[i] for i in ["flag", "abbrev", "name"] if i in argument
        ]
        description = argument["description"]
        required = argument.get("required", False)

        extra_args = {}
        if flag:
            extra_args["required"] = required
        else:
            if not required:
                extra_args["nargs"] = "?"
        parser.add_argument(*names, help=description, **extra_args)
