clidesc
=======

`clidesc` is a CLI interface framework that can be used to build simple,
yet functional, command line interfaces with minimal client code.

The goal is to create a framework to build the command line interface only
using configuration files (YAML or JSON format), and minimizing the need to
write code for it.


Usage
-----

To create a simple "Greeting" application, the CLI definition file, should
look like:

```yaml
---
program: greeting
description: A greeting application.
version: 1.0
handler: greeting.hello
arguments:
  - name: someone
    description: Someone to greet.
    type: string
    required: true
```

And the application code would be:

```python
# Contents of greeting.py

from clidesc import CLIDesc

def hello(someone):
    print(f"Hello, {someone}!")

if __name__ == "__main__":
    cli = CLIDesc.from_file("greeting.yml")
    cli.run()
```

With this configuration, the application will have options to display its
version (--version), help instructions (-h or --help), and a required
positional argument. If run with `--help`, the output is:

```
usage: greeting [-h] [--version] someone

A greeting application.

positional arguments:
  someone     Someone to greet.

optional arguments:
  -h, --help  show this help message and exit
  --version   display program version
```

If the application does not receive the required argument, an error is
displayed. For example, the output for running `greeting` is:

```
usage: greeting [-h] [--version] someone
greeting: error: the following arguments are required: someone
```

When running an application with one parameter, `greeting World`, the output
would be:

```
Hello, World!
```

You may also use `clidesc` to automatically format the output returned by
the handler methods. Use the `output` attribute along with the handler
method to configure the output format.

The next example configures the output format, with a formatting string,
that follows Python's formatting rules.

```yaml
---
program: output
description: Auto-formatting output.
version: 1.0
handler: output.hello
output:
  format: "Hello, {someone}"
arguments:
  - name: someone
    description: Someone to greet.
    required: true
```

And the code for this application would be:

```python
# contents of output.py.

from clidesc import CLIDesc


def hello(someone):
    """Greet someone."""
    return {"someone": someone}


if __name__ == "__main__":
    cli = CLIDesc.from_file('output.yaml'))
    cli.run()
```

Applications with multiple commands and command groups (like `git`) are
supported through `sub_commands`. Each `command` in `sub_command` can have
its own `sub_command`, creating a command hierarchy (deep hierarchies are
not recommended).

The configuration for such application would be:

```yaml
---
program: multi
description: A multi-command application.
version: 1.0
sub_commands:
  title: Commands
  description: Application sub-commands
  group_name: Sub commands
  commands:
    - name: abc
      description: First command.
      handler: multi.abc
      arguments:
      - name: some_arg
        description: Some argument.
    - name: xyz
      description: Second command.
      handler: multi.xyz
      arguments:
      - name: another_arg
        description: Another argument.
```

And the client code:

```python
# contents of multi.py

from clidesc import CLIDesc

def abc(some_arg):
    """Greet someone."""
    print(f"ABC: {some_arg}")


def xyz(another_arg):
    """Greet someone."""
    print(f"XYZ: {another_arg}")


if __name__ == "__main__":
    cli = CLIDesc.from_file("multi.yml")
    cli.run()
```


Output Formatting
-----------------

> Note: The output formatting is still a "preview" and might change in the
near future. Documentation and testing is far from complete. Check
[features/output_display.feature] for tested usage examples.

clidesc allows automatic formatting of the command handlers result. To display
the returned values, `output` must be set to `yes`, or provide the format
and/or format options.

The default output formatting will depend on the data type that is returned
by the command handler. Strings are written as returned, numbers (int, float
    and complex) follow standard Python output conventions.

Lists, tuples and sets are displayed one item per line, with a "dash" before
the item:

```
- First item
- Second item
- Third item
```

Dictionaries are displayed as `key: value` pairs, but the value will be
formatted according to its type, and padded:

```
a_string: Some text.
a_list:
    - an item
    - another item
a_dict:
    a_key: a value
    another_key:
        - an inner list
```

To modify the default display behavior, `output` must be configured. When
configuring the output formatting, `clidesc` uses Python's
[Format String Syntax].

For example, if the result of a handler is the dictionary `{someone: John}`,
and the output is set to `output: Hello, {someone}.`, the output will be
`"Hello, John."`. The complete configuration for such an application might be
(see [examples/output.py]):

```
---
program: output
description: Auto-formatting output.
version: 1.0
handler: output.hello
output: "Hello, {someone}."
arguments:
  - name: someone
    description: Someone to greet.
    required: true
```

Lists can be set to be displayed with the item numbers by setting `enumerate`
to `yes` (by default, it is `1`):

```
output:
   enumerate: yes
```

Which would result in something like:

```
users:
    1. Amy
    2. Peter
    3. Jim
```

To change the base number of the list, set enumerate to the desired value,
for example `enumerate: 0` would result in:

```
users:
    0. Amy
    1. Peter
    2. Jim
```

The list items can also have its format customized, with a format string. To
mimic the `enumerate: yes` configuration, the format sting can be defined as:

```
output:
  users: "{_pad}{_index}. {_item}"
```

This will result in:

```
users:
    1. Amy
    2. Peter
    3. Jim
```

It is also possible to hide the `key` using the `no_key` setting:

```
output:
  users:
    no_key: yes
    format: "{_pad}{_index}. {_item}"
```

Resulting in the output:

```
1. Amy
2. Peter
3. Jim
```

The attributes available to configure the output are:

| Name         | Description                            | Default |
| :----------- | :------------------------------------- | :------ |
| output       | Set to anything than No or False, will force output. If set to a string, will act as the format string. | No |
| _field name_ | The name of the field to control output formatting. If set to a string, will act as the format string. | None |
| format       | The formatting string, can be applied to `output` or to a _field_ | Varies for data type. |
| no_key       | Hide the display of `keys` in dictionaries, if set to `yes`. | No |
| enumerate    | If set to `yes` display numbered lists (starting on `1`), if set to an `int`, set the value for the first element of the list. | No |
| padding      | The amount of _spaces_ to be used for padding for each level of data. Set to 0 or False to disable padding. This attribute must be used with the global `output`, not with a `field`. | 4 |


The format string follows the same rules as the Python's [Format String Syntax], and some special attributes are available to aid in formatting output:

| Name      | Description                                        |
| :-------- | :------------------------------------------------- |
| _pad      | The current padding for the data to be displayed.  |
| _key      | The key of the current item.                       |
| _value    | The value of the current item.                     |
| _path     | The path to the current item (all of its keys).    |
| _index    | The index of the current list item.                |
| _item     | The value of the current list item.                |

> Note: These attributes are available to lists, they might not be available to other data types.


Exceptions
----------

Exceptions might occur during execution of a command handle, and `clidesc`
does not change the default Python behavior, but allows exceptions to be
handled as error messages to the end user.

For example, the following description would print an error message and set
the program exit code if the specific exception occurs:

```
---
program: calculator
description: A simple calculator
version: 1.0
handler: calculator.compute
exceptions:
  - class: ValueError
    exit_code: 5
    message: An error occured with message "{exception}".
arguments:
  - name: lhs
    description: Left hand symbol.
  - name: rhs
    description: Right hand symbol.
```

Exception handlers are set globally, in a handler base.

The following attributes can be used when configuring exception handling:

| Name      | Description                                | Default | Required |
| :-------- | :------------------------------------------| :------ | :------: |
| class     | The name of the exception class to handle. |    -    |   yes    |
| action    | The kind of action to take: raise, abort, traceback. | raise | no |
| exit_code | An integer that will be the program exit code. If explicitly set to a non-zero, force `action` to be `abort`. | 1 | no |
| message   | A format string to be displayed. It will be formatted with an `exception` object of the raised exception. | - | no |


Using attributes for `version`
------------------------------

Often, the program version is available as a module attribute, and
maintaining this value in more than one place adds a duplication that
can make the different locations showing different versions. To avoid
this, `clidesc` supports setting the `version` attribute using an
attribute of a module. The value will still be bound when the `CLIDesc`
is created, that is, if the attribute value changes while the program is
running, it will not be reflected on the CLI.

For example, to define the program version as an attribute, use:

```yaml
---
program: greeting
description: A greeting application.
version:
  attribute: greeting.__version__
```

And the code for `greeting.py` (or `greeting/__init__.py`) should include
the attribute definition, for example:

```
__version__ = "1.2.0"
```


Project configuration
---------------------

When using `clidesc` in your project, if using `yamllint` to verify the CLI
description file structure, you might want to add the following configuration
to `.yamllint`:

```
truthy:
  allowed-values: [yes, no, true, false, True, False]
```


Authors
-------

Rafael Guterres Jeffman <rafasgj@gmail.com>


<!-- References -->
[Format String Syntax]: https://docs.python.org/3/library/string.html#formatstrings
[examples/output.py]:examples/output.py
