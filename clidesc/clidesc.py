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

import sys
import re
import itertools
from argparse import ArgumentParser
import importlib
import traceback

try:
    import yaml
except ImportError:  # pragma: no cover
    pass

# pylint: disable=too-many-instance-attributes


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
            version = cli_description["version"]
            if isinstance(version, dict):
                *module, attr = version["attribute"].split(".")
                module = ".".join(module) if module else "builtins"
                imp_mod = importlib.import_module(module)
                if not hasattr(imp_mod, attr):
                    raise ValueError(
                        f"Module `{module}` has no attribute `{attr}`"
                    )
                version = getattr(imp_mod, attr)
            self.__argparse.add_argument(
                "--version",
                action="version",
                help="display program version",
                version=f"%(prog)s {version}",
            )

        self.configuration = Object()
        self.__non_parameters = []
        self.__output = {}
        self.__commands = {}
        self.output_stream = sys.stdout
        self.exit_code = 0
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

        method_name = self.__commands[self.__get_method_name_from(args)]
        output = self.__output[method_name]

        # execute function
        *module, function = method_name.split(".")
        mod = importlib.import_module(".".join(module))
        handler = getattr(mod, function)
        try:
            result = handler(**args)
        except Exception as exc:  # pylint: disable=broad-except
            if "exceptions" in self.__description:
                self.__process_exception(exc, self.__description["exceptions"])
            raise exc from None
        else:
            if output:
                if isinstance(output, bool):
                    output = {}
                self.__display(result, level=0, format_cfg=output)
            return result
        return None

    def __get_method_name_from(self, args):
        method_name = args.get("_cli_command", self.__description["program"])
        if "_cli_command" in args:
            del args["_cli_command"]
        if not method_name:
            raise Exception("Method name not defined.")
        if method_name not in self.__commands:
            raise Exception(f"Invalid command: {method_name}.")
        return method_name

    def __process_exception(self, exc, exceptions):
        """Process exception to provide user defined behavior."""
        exc_names = [n.__name__ for n in type(exc).mro()]
        exceptions = self.__description["exceptions"]
        candidates = [
            y
            for x, y in itertools.product(exc_names, exceptions)
            if y["class"] == x
        ]
        if not candidates:
            raise exc from None
        exception = candidates[0]
        exit_code = exception.get("exit_code", 0)
        action = exception.get("action", "abort" if exit_code else "raise")
        if action == "raise":
            raise exc from None
        # if not raising, program will end.
        error_msg = exception.get("message", "ERROR: {exception}")
        print(error_msg.format(exception=exc), file=self.output_stream)
        if action == "traceback":
            traceback.print_tb(exc.__traceback__)
        sys.exit(exit_code if "exit_code" in exception else 1)

    def __add_argument(self, parser, argument):
        default = argument.get("default")
        store_selector = {
            True: "store_false",
            False: "store_true",
        }
        arg_type = {
            "count": (int, "count"),
            "int": (int, "store"),
            "integer": (int, "store"),
            "str": (str, "store"),
            "string": (str, "store"),
            "float": (float, "store"),
            "boolean": (bool, store_selector[bool(default)]),
            "bool": (bool, store_selector[bool(default)]),
        }
        extra_args = {}

        description = argument["description"]
        required = argument.get("required", False)
        optional = argument.get("optional")

        datatype, action = arg_type.get(argument.get("type", "str"))

        extra_args["action"] = action
        if default or action == "count":
            extra_args["default"] = datatype(default) if default else 0

        if optional:
            names = [f"--{argument['name']}"]
            if "abbrev" in argument:
                names.append(f"-{argument['abbrev']}")
            extra_args["required"] = required
        else:
            if "abbrev" in argument:
                raise Exception("Cannot use `abbrev` without `optional: yes`.")
            if (
                argument.get("type", "string") not in ["bool", "boolean"]
                and not required
            ):
                extra_args["nargs"] = "?"
            names = [argument["name"]]

        if argument.get("type") not in ["count", "bool", "boolean"]:
            extra_args["type"] = datatype

        if "nargs" in argument:
            extra_args["nargs"] = argument["nargs"]
        if "choices" in argument:
            extra_args["choices"] = argument["choices"]

        if argument.get("configuration"):
            self.__non_parameters.append(
                names[0][re.search(r"[^-]", names[0]).start() :]
            )

        parser.add_argument(*names, help=description, **extra_args)

    def __display(self, data, level, format_cfg, parent=None):
        """Display the result of the API command."""
        if not isinstance(format_cfg, (str, dict)):
            raise TypeError("Invalid format type: %s" % type(format).__name__)

        display_opts = self.__get_display_opts(level, format_cfg, parent)
        if isinstance(format_cfg, str):
            print(
                format_cfg.format(**data, **display_opts),
                file=self.output_stream,
            )
        else:
            if isinstance(data, (str, int)):
                print(data, file=self.output_stream)
            elif isinstance(data, list):
                self.__display_list(data, display_opts, parent or "")
            else:
                for _key, _value in data.items():
                    _parent = parent.split(".") if parent else []
                    element = ".".join(_parent + [_key])
                    disp_key, fmt = self.__get_display_key(format_cfg, _key)
                    if isinstance(_value, (list, set, dict, tuple)):
                        inc = 0
                        if disp_key:
                            print(
                                f"{display_opts['_pad']}{disp_key}",
                                file=self.output_stream,
                            )
                            inc = 1
                        self.__display(_value, level + inc, format_cfg, element)
                    else:
                        print(disp_key, end=" ", file=self.output_stream)
                        if fmt:
                            keys = {_key: _value}
                            keys.update(display_opts)
                            print(fmt.format(**keys), file=self.output_stream)
                        else:
                            print(_value, file=self.output_stream)

    @staticmethod
    def __get_display_key(format_cfg, key):
        fmt = format_cfg.get("format")
        inner = None
        if key in format_cfg:
            inner = format_cfg[key]
            if isinstance(inner, dict):
                if "format" in inner:
                    fmt = inner["format"]
                if inner.get("no_key", False):
                    return "", fmt
        if format_cfg.get("no_key", False):
            return "", fmt
        return f"{key}:", fmt

    def __display_list(self, data, display_opts, parent):
        for _index, _item in enumerate(data):
            inc = 1
            _fmt = (
                "{_pad}{theme.list}-{theme.RESET} "
                "{theme.list_item}{_item}{theme.RESET}"
            )
            if "__enumerate" in display_opts:
                _inc = display_opts["__enumerate"]
                if isinstance(_inc, bool):
                    do_fmt = _inc
                elif isinstance(_inc, int):
                    do_fmt = True
                    inc = _inc
                else:
                    raise TypeError(
                        "Invalid type for 'enumerate': %s" % type(_inc).__name__
                    )
                if do_fmt:
                    _fmt = (
                        "{_pad}{theme.list}{_index}.{theme.RESET} "
                        "{theme.list_item}{_item}{theme.RESET}"
                    )
            disp_fmt = display_opts.get("__format")
            _fmt = disp_fmt if disp_fmt else _fmt
            _key = parent.split(".")[-1] if parent else ""
            text = _fmt.format(
                **display_opts,
                _index=_index + inc,
                _item=_item,
                _key=_key,
                _value=_item,
                _parent=parent,
            )
            print(text, file=self.output_stream)

    @staticmethod
    def __get_display_opts(level, format_cfg, parent):
        # get formatting options
        if isinstance(format_cfg, str):
            _fmt = {"format": format_cfg}
        else:
            _fmt = format_cfg
        _pad_size = _fmt.get("padding", 4)
        colorize = _fmt.get("colorize", False)
        if parent:
            for _elem in parent.split("."):
                if _elem in _fmt:
                    _fmt = _fmt[_elem]
                    if "colorize" in _fmt:
                        colorize = _fmt["colorize"]
                else:
                    break
            if isinstance(_fmt, str):
                _fmt = {"format": _fmt}
        display_opts = {
            "_pad": (" " * (_pad_size * level)) if _pad_size else "",
            "__format": _fmt.get("format"),
            "__no_key": _fmt.get("no_key", False),
        }
        display_opts.update(CLIDesc._ansi_color_theme(colorize))
        if "enumerate" in _fmt:
            display_opts["__enumerate"] = _fmt["enumerate"]
        return display_opts

    @staticmethod
    def _ansi_color_theme(colorize):
        colors = {
            "RESET": "\033[0m",
            "FG_RESET": "\033[39m",
            "BG_RESET": "\033[49m",
            "BLACK": "\033[30m",
            "DARK_GRAY": "\033[90m",
            "GRAY": "\033[37m",
            "WHITE": "\033[97m",
            "DARK_RED": "\033[31m",
            "DARK_GREEN": "\033[32m",
            "ORANGE": "\033[33m",
            "DARK_BLUE": "\033[34m",
            "DARK_MAGENTA": "\033[35m",
            "DARK_CYAN": "\033[36m",
            "RED": "\033[91m",
            "GREEN": "\033[92m",
            "YELLOW": "\033[93m",
            "BLUE": "\033[94m",
            "MAGENTA": "\033[95m",
            "CYAN": "\033[96m",
            "BG_BLACK": "\033[40m",
            "BG_DARK_GRAY": "\033[100m",
            "BG_GRAY": "\033[47m",
            "BG_WHITE": "\033[107m",
            "BG_DARK_RED": "\033[41m",
            "BG_DARK_GREEN": "\033[42m",
            "BG_ORANGE": "\033[43m",
            "BG_DARK_BLUE": "\033[44m",
            "BG_DARK_MAGENTA": "\033[45m",
            "BG_DARK_CYAN": "\033[46m",
            "BG_RED": "\033[101m",
            "BG_GREEN": "\033[102m",
            "BG_YELLOW": "\033[103m",
            "BG_BLUE": "\033[104m",
            "BG_CYAN": "\033[106m",
            "BG_MAGENTA": "\033[105m",
        }
        theme = {k: "" for k in ["RESET", "list", "list_item"]}
        if colorize:
            theme = {
                "RESET": "{RESET}",
                "list": "{WHITE}",
                "list_item": "",
            }
        colors["theme"] = type(
            "Theme",
            (object,),
            {k: v.format(**colors) for k, v in theme.items()},
        )
        return colors
