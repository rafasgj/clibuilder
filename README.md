autocli
=======

`autocli` is a CLI interface framework that can be used to build simple, yet
functional, command line interfaces with minimal client code.

The goal is to create a framework to build the command line interface only
using configuration files (YAML or JSON format), and minimizing the need to
write code for it.

For example, to create a simple "Greeting" application, the CLI definition
file, should look like:

```yaml
---
program: greeting
description: A greeting application.
version: 1.0
handler: greeting.hello
arguments:
  someone:
    description: Someone to greet.
    type: string
    required: true
```

And the application code would be:

```python
from autocli.autocli import AutoCLI

def hello(someone):
    print(f"Hello, {someone}!")

if __name__ == "__main__":
    cli = AutoCLI.from_file("greeting.yml")
    cli.run()
```

With this setup, the application will have options to display its version
(--version), help instructions (-h or --help), and a required positional
argument. If run with `--help`, the output is:

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
