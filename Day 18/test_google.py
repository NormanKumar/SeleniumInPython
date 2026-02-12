import pytest

from driverfactory import get_driver

@pytest.mark.parametrize("browser",["chrome","edge"])
def test_google_title(browser):
    driver=get_driver(browser)
    driver.get("https://www.google.com/")
    assert "Google" in driver.title
    driver.quit()


@pytest.mark.parametrize("browser", ["chrome", "edge"])
def test_google_serach(browser):
    driver = get_driver(browser)
    driver.get("https://www.google.com/")
    serachbox=driver.find_element("name","q")
    serachbox.send_keys("Selenium Grid")
    serachbox.submit()
    assert "Selenium Grid" in driver.title

    driver.quit()