import pytest
from settings import BASE_URL, USERNAME, PASSWORD, BROWSER
from driver_factory import create_driver
from login_page import LoginPage


@pytest.fixture
def setup():
    driver = create_driver(BROWSER)
    driver.get(BASE_URL)
    yield driver
    driver.quit()


def test_valid_login(setup):
    login = LoginPage(setup)
    login.login(USERNAME, PASSWORD)

    assert login.is_logged_in()
    print("Login test PASSED")
