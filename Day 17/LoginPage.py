from selenium import webdriver
from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    username = (By.NAME, "username")
    password = (By.NAME, "password")
    login_button = (By.XPATH, "//button[@type='submit']")

    def enter_username(self,username):
        self.driver.find_element(*self.username).send_keys(username)

    def enter_password(self,password):
        self.driver.find_element(*self.password).send_keys(password)

    def click_login(self):
        self.driver.find_element(*self.login_button).click()