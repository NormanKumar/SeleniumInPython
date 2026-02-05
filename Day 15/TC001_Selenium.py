from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get('https://tutorialsninja.com/demo')
driver.maximize_window()
print("title is ", driver.title)
driver.get('https://google.com')
print("title is ", driver.title)
print("Performing back()")
driver.back()
print('page title after back', driver.title)
print("Performing forward()")
driver.forward()
print("title after forward", driver.title)
time.sleep(5)
driver.minimize_window()
driver.close()