import pytest

@pytest.fixture(scope="function")
def add_data():
    return (2, 3)

@pytest.fixture(scope="module")
def subtract_data():
    return (5, 2)
