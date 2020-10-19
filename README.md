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
