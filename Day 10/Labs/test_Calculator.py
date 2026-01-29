import pytest
from AssignmentDay10_2_Calculator import add, subtract, multiply, divide

def test_addition():
    assert add(2, 3) == 5

def test_subtraction():
    assert subtract(5, 2) == 3

def test_multiplication():
    assert multiply(4, 3) == 12

def test_division():
    assert divide(10, 2) == 5

def test_division_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
