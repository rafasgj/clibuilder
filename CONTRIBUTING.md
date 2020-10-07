Contributing to autocli
=======================

Thank you for taking time to contribute to autocli!

These are the guidelines for contributing to autocli, it is not a book of
rules. Use your best judgment, and feel free to purpose changes to this document.

autocli is hosted on [Github](https://github.com) and most of the time,
you will be using one of Github's features to make a contribution to the
project, in [autocli repository](https://github.com/rafasgj/autocli).

Reporting Bugs
--------------

We use [issues in Github](https://github.com/rafasgj/autocli/issues), to
track open bugs. Before reporting a bug, look at the open issues, to see
if the bug has not been reported, yet. If it is, we suggest commenting on
the open issue, which will _upvote_ the issue, by showing that more people
is being affected by the problem.

When reporting a new bug, be clear on the problem you reporting, and include:

* Version for autocli, Python and operating system;
* A clear description of the problem;
* A clear description of what you were trying to achieve;
* The expected result, and the result observed;
* A list of steps to reproduce the issue;
* If code is involved (it probably is), include minimum code sample that
  reproduces the issue.

The more complete and accurate information, the easier it is to understand,
find and fix the problem.

Once the bug is filled, it will be triaged, and labelled as `bug`, if it
will be fixed.


Requesting Features
-------------------

Features are actually very similar to bugs, but they are functionality that
is missing, while bugs are functions that misbehave. Features are also
reported as [issues in Github](https://github.com/rafasgj/autocli/issues).

A new feature might be a new functionality or an enhancement over an
existing functionality. Before requesting a feature search the open issues
to check if the new feature is not already proposed, and if it is, comment
on the open issue.

When requesting a new feature request, include:

* A clear description of what you want to achieve;
* Why you need this new feature;
* You might show how you want to use the feature;

Once the feature request, it will be triaged, and labelled as `enhancement`.


Contributing Code
-----------------

Once you are willing to contribute code, you must follow a few rules:

* For every bug fixed, there must be an implemented test that reproduces
  the issue.
* For every feature implemented there must be a behavior defined, and the
  steps to test the behavior.
* Your code should pass the linter evaluation, and all existing tests must
  pass.

### Code Formatting

autocli uses `black` for code formatting. The only configuration needed is
setting up line length to 80 (`-l 80`). If using an editor like Atom or
VSCode, it is suggested that the editor is configured to format with `black`
automatically.

### Linters

autocli uses flake8, pylint, and pydocstyle linters. The configuration for
the linters is found on [setup.cfg](setup.cfg).

The flake8 linter will use the configured linters in the system. The pylint
linter will add McCabe extension and compute the cyclomatic complexity for
the code. Both linters are set for a maximum complexity of 10.

### Testing

Features must be defined using the _Gherkin language_, and steps to test it
must be implemented. [Behave](http://github.com/behave/behave) is used to
run tests for features.

As most features will use either (or both) `stdout` and `stderr`, methods
and configuration to capture and evaluate the output on each stream are
provided. Use the tags `@stdout` and `@stderr` on your features or scenarios
to enable them.

`behave` is used to test expected behavior. To test corner cases, or negative
(i.e. exceptions) behavior, [pytest](https;//pytest.org) is used.

Bugs must have tests that reproduce the issue to be fixed, these tests are
implemented using `pytest`.

To execute all code tests (linters and tests), [Tox](https://tox.readthedocs.io)
is used. A configuration for it is provided in [setup.cfg](setup.cfg), along
with configuration for [coverage](https://github.com/nedbat/coveragepy).

Although it would be cool to have 100% of code test coverage, and it is a
goal of the project, complete code coverage does not guarantee that all
possibilities are covered. Try to be thorough when designing tests for your
code.

### Pull Requests

To have your code merged to the project repository, you must create a
[pull request on github](https://github.com/rafasgj/autocli/pulls). The
pull request will then be reviewed and when approved, it will be merged.

Each commit on the pull request must have a brief description using
present tense and imperative mood, with, at most, 72 characters.
Then, the commit must have a brief description of the problem being fixed,
how it was fixed, and what it changes in autocli usage.

If the pull request was created to fix an open issue, include this
information in a commit message, by adding "Fix: #<issue number>" to it.

### Development Environment

autocli uses `setup.cfg` to handle dependencies. It is suggested that the
development dependencies are installed in a virtual environment, with `pip`,
using an editable install.

```
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -e .[dev]
```
