"""Utility math functions.

This module provides basic arithmetic operations with type hints and docstrings.
"""
from typing import Union

Number = Union[int, float]

def add_numbers(a: Number, b: Number) -> Number:
    """Return the sum of two numbers.

    Args:
        a: First addend (int or float).
        b: Second addend (int or float).

    Returns:
        The sum of a and b.
    """
    return a + b


def subtract_numbers(a: Number, b: Number) -> Number:
    """Return the difference of two numbers (a - b).

    Args:
        a: Minuend (int or float).
        b: Subtrahend (int or float).

    Returns:
        The result of a - b.
    """
    return a - b
