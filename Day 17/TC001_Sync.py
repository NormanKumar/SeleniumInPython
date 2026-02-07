from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from LoginPage import *

driver = webdriver.Edge()
wait = WebDriverWait(driver, 10)

driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

# wait.until(EC.visibility_of_element_located((By.NAME, "username"))).send_keys("Admin")
# driver.find_element(By.NAME, "password").send_keys("admin123")
# driver.find_element(By.XPATH, "//button[@type='submit']").click()
#
# wait.until(EC.url_contains("dashboard"))
#
# print("Logged in successfully — dashboard loaded!")
#
# input("Press ENTER to close browser...")
# driver.quit()

loginobj=LoginPage(driver)
time.sleep(5)
loginobj.enter_username("Admin")
loginobj.enter_password("admin123")

loginobj.click_login()

