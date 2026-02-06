from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://tutorialsninja.com/demo/index.php?route=common/home")

    my_account = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='My Account']")))
    my_account.click()

    register = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
    register.click()

    driver.find_element(By.ID, "input-firstname").send_keys("John")
    driver.find_element(By.ID, "input-lastname").send_keys("Doe")
    driver.find_element(By.ID, "input-email").send_keys(f"john{int(time.time())}@mail.com")
    driver.find_element(By.ID, "input-telephone").send_keys("1234567890")
    driver.find_element(By.ID, "input-password").send_keys("Test@1234")
    driver.find_element(By.ID, "input-confirm").send_keys("Test@1234")

    driver.find_element(By.XPATH, "//input[@name='newsletter' and @value='0']").click()
    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    continue_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Continue")))
    continue_btn.click()

    my_orders = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='View your order history']")))
    my_orders.click()

    rows = driver.find_elements(By.XPATH, "//table//tbody/tr")

    if rows:
        print("✅ Orders found:")
        for row in rows:
            print(row.text)
    else:
        no_orders_msg = driver.find_element(
            By.XPATH, "//p[contains(text(),'You have not made any previous orders')]"
        )
        print(no_orders_msg.text)

finally:
    time.sleep(3)
    driver.quit()
