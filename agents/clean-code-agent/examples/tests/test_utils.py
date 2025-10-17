import math
import pytest

from agents.clean-code-agent.examples.utils import add_numbers, subtract_numbers


def test_add_numbers_integers():
    assert add_numbers(2, 3) == 5


def test_add_numbers_floats():
    assert math.isclose(add_numbers(2.5, 3.1), 5.6)


def test_subtract_numbers_integers():
    assert subtract_numbers(5, 3) == 2


def test_subtract_numbers_floats():
    assert math.isclose(subtract_numbers(5.5, 3.2), 2.3)


def test_add_numbers_negative():
    assert add_numbers(-2, -3) == -5


def test_subtract_numbers_negative():
    assert subtract_numbers(-2, -3) == 1
