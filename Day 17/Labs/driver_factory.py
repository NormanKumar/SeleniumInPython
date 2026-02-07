from selenium import webdriver

def create_driver(browser):
    if browser.lower() == "edge":
        driver = webdriver.Edge()
    elif browser.lower() == "chrome":
        driver = webdriver.Chrome()
    else:
        raise Exception("Browser not supported")

    driver.maximize_window()
    return driver
