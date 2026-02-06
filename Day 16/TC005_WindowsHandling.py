from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Edge()
driver.get("https://letcode.in/window")
time.sleep(5)
driver.find_element(By.ID,"multi").click()
windows = driver.window_handles
for child in windows:
    driver.switch_to.window(child)
    time.sleep(5)
    print("title",driver.current_url)