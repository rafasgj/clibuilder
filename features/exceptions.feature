@stdout @stderr
Feature: Assist handling of exceptions.

Scenario: Simple exception output.
    Given the CLI description
        """
        ---
        program: calculator
        description: A simple calculator
        version: 1.0
        handler: calculator.compute
        exceptions:
          - class: ValueError
            message: "An invalid value was used: {exception}"
            exit_code: 10
        arguments:
          - name: lhs
            description: Left hand symbol.
          - name: rhs
            description: Right hand symbol.
        """
        And a function named "calculator.compute" raises ValueError, with message "Divided by zero"
    When the application is executed with [0, 0]
    Then the output is
        """
        An invalid value was used: Divided by zero
        """
        And the exit code is 10

Scenario: Allow exception to be raised from handler.
    Given the CLI description
        """
        ---
        program: calculator
        description: A simple calculator
        version: 1.0
        handler: calculator.compute
        exceptions:
          - class: ValueError
            action: raise
        arguments:
          - name: lhs
            description: Left hand symbol.
          - name: rhs
            description: Right hand symbol.
        """
        And a function named "calculator.compute" raises ValueError, with message "Divided by zero"
    When the application is executed with [0, 0]
    Then exception ValueError is raised
