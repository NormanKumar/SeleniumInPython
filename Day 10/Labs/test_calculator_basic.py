import pytest
from AssignmentDay10_2_Calculator import add, subtract

def setup_module(module):
    print("\nSetup module")

def teardown_module(module):
    print("\nTeardown module")

def setup_function(function):
    print("\nSetup function")

def teardown_function(function):
    print("\nTeardown function")

def test_add(add_data):
    assert add(*add_data) == 5

def test_subtract(subtract_data):
    assert subtract(*subtract_data) == 3
