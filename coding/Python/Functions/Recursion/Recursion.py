"""
Recursion in Python – Definition

Recursion is a programming technique where a function calls itself directly or indirectly to solve a problem.

The function usually works by breaking a problem into smaller sub-problems.

Each recursive call should have a base case to stop the recursion, otherwise it will lead to an infinite loop / stack overflow.

Key Points

Base Case: Condition to stop recursion.

Recursive Case: The part where the function calls itself.
"""


def factorial(n):
    if n == 0 or n == 1:  # Base case
        return 1
    else:
        return n * factorial(n-1)  # Recursive case

print(factorial(5))  # Output: 120
