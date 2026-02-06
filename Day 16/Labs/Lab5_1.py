from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup driver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    # Open website
    driver.get("https://tutorialsninja.com/demo/index.php?route=common/home")

    # Click My Account dropdown
    my_account = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='My Account']"))
    )
    my_account.click()

    # Click Register
    register = wait.until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Register"))
    )
    register.click()

    # Fill form
    driver.find_element(By.ID, "input-firstname").send_keys("John")
    driver.find_element(By.ID, "input-lastname").send_keys("Doe")
    driver.find_element(By.ID, "input-email").send_keys(f"john{int(time.time())}@mail.com")
    driver.find_element(By.ID, "input-telephone").send_keys("1234567890")
    driver.find_element(By.ID, "input-password").send_keys("Test@1234")
    driver.find_element(By.ID, "input-confirm").send_keys("Test@1234")

    # Subscribe No
    driver.find_element(By.XPATH, "//input[@name='newsletter' and @value='0']").click()

    # Click Continue without accepting Privacy Policy
    driver.find_element(By.XPATH, "//input[@value='Continue']").click()

    # ✅ Verify warning message
    warning = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'alert-danger')]")
        )
    )

    expected_warning = "Warning: You must agree to the Privacy Policy!"
    assert expected_warning in warning.text

    print("✅ Warning message verified successfully!")

finally:
    time.sleep(3)
    driver.quit()
