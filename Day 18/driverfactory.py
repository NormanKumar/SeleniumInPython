from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions

from selenium.webdriver.edge.options import Options as EdgeOptions

GRIDURL =  "http://192.168.137.1:4444"


def get_driver(browser):
    if browser == "chrome":

        options = ChromeOptions()

        options.add_argument("--disable-blink-features=AutomationControlled")

    elif browser == "edge":

        options = EdgeOptions()

        options.add_argument("--disable-blink-features=AutomationControlled")

    else:

        raise ValueError("Browser not supported")

    driver = webdriver.Remote(

        command_executor=GRIDURL,

        options=options

    )

    driver.maximize_window()

    return driver