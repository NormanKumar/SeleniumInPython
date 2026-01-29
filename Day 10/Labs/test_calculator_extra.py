import pytest
from AssignmentDay10_2_Calculator import divide

def test_divide(add_data):
    assert divide(*add_data) == 2 / 3

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
