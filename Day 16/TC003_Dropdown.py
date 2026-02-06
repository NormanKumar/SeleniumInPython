from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
driver=webdriver.Edge()
driver.get("https://tutorialsninja.com/demo/index.php?route=common/home")
driver.find_element(By.LINK_TEXT,"Desktops").click()
driver.find_element(By.LINK_TEXT,"Mac (1)").click()
dropdown=Select(driver.find_element(By.ID,"input-sort"))

options=dropdown.options
for option in options:
    print(option.text)

dropdown.select_by_index(4)