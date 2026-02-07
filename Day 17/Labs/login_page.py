from selenium.webdriver.common.by import By
from base_page import BasePage

class LoginPage(BasePage):

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit']")
    DASHBOARD = (By.XPATH, "//h6[text()='Dashboard']")

    def login(self, user, pwd):
        self.type(self.USERNAME, user)
        self.type(self.PASSWORD, pwd)
        self.click(self.LOGIN_BTN)

    def is_logged_in(self):
        return self.wait.until(lambda d: d.find_element(*self.DASHBOARD))
