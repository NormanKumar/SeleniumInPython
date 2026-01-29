import pytest
from utilities.math_utils import add

# utilities/math_utils.py
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
