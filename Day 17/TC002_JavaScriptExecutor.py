from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
driver.get("https://www.amazon.in")
driver.execute_script("alert('Hello Amazon')")

time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(5)