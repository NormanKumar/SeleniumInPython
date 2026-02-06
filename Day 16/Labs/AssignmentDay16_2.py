from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import Select
driver=webdriver.Edge()
driver.get("https://letcode.in/alert")
driver.find_element(By.ID,"accept").click()
alert=driver.switch_to.alert
print(alert.text)
alert.accept()

driver.find_element(By.ID,"confirm").click()
alert = driver.switch_to.alert
print(alert.text)
alert.accept()

driver.find_element(By.ID,"prompt").click()
alert = driver.switch_to.alert
alert.send_keys("RobinHood")
alert.accept()
print(driver.find_element(By.ID, "myName").text)
driver.quit()