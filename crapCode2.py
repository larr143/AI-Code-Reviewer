# Example Python code for testing Pylint

def fibonacci(n):
    if n <= 0:
        return "Invalid input"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(n - 2):
            a, b = b, a + b
        return b

def print_fibonacci_sequence(count):
    for i in range(1, count + 1):
        print(f"Fibonacci({i}): {fibonacci(i)}")

# Example function with intentional pylint error (unused variable)
def unused_variable_example():
    unused_variable = 42

# Example class with pylint convention issue (naming convention)
class myClass:
    def __init__(self):
        self.my_variable = 10

    def print_variable(self):
        print(self.my_variable)

# Example code with pylint warning (line too long)
long_string = "This is a very long string that exceeds the maximum line length allowed by Pylint. Pylint will generate a warning for this line."

# Example code with pylint convention issue (unused import)
import math

# Example code with pylint error (undefined variable)
print(undefined_variable)

# Example code with pylint convention issue (variable name not lowercase)
InvalidVariableName = 42

# Example code with pylint convention issue (missing function docstring)
def undocumented_function():
    pass

# Example code with pylint warning (redefined variable)
redefined_variable = 10
redefined_variable = 20
