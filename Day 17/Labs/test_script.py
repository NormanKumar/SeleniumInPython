from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.edge.service import Service
from locators import *
import time

class TestTutorialsNinja:
    """Test class for TutorialsNinja demo site"""

    def __init__(self):
        self.driver = None
        self.wait = None
        self.base_url = "https://tutorialsninja.com/demo/index.php?route=common/home"

    def setup(self):
        """Setup method to initialize the Edge browser"""
        print("Setting up Edge browser...")
        self.driver = webdriver.Edge()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 15)
        print("Browser setup complete")

    def teardown(self):
        """Teardown method to close the browser"""
        if self.driver:
            print("Closing browser...")
            time.sleep(2)
            self.driver.quit()
            print("Browser closed")

    def test_add_mac_to_cart(self):
        """Test case to add Mac product to cart"""
        try:
            # Step 1: Open the URL
            print(f"\nStep 1: Opening URL: {self.base_url}")
            self.driver.get(self.base_url)
            print("✓ URL opened successfully")

            # Step 2: Go to 'Desktops' tab
            print("\nStep 2: Hovering over 'Desktops' tab")
            desktops_tab = self.wait.until(
                EC.element_to_be_clickable(Locators.DESKTOPS_TAB)
            )
            desktops_tab.click()
            print("✓ Clicked on 'Desktops' tab")

            # Step 3: Click on 'Mac'
            print("\nStep 3: Clicking on 'Mac' option")
            mac_option = self.wait.until(
                EC.element_to_be_clickable(Locators.MAC_OPTION)
            )
            mac_option.click()
            print("✓ Clicked on 'Mac' option")
            time.sleep(1)

            # Step 4: Select 'Name (A-Z)' from Sort By dropdown
            print("\nStep 4: Selecting 'Name (A-Z)' from Sort By dropdown")
            sort_dropdown = self.wait.until(
                EC.presence_of_element_located(Locators.SORT_BY_DROPDOWN)
            )
            select = Select(sort_dropdown)
            select.select_by_visible_text("Name (A - Z)")
            print("✓ Selected 'Name (A-Z)' from dropdown")
            time.sleep(1)

            # Step 5: Click on 'Add to Cart' button
            print("\nStep 5: Clicking 'Add to Cart' button")
            # Wait for page to load after sorting
            time.sleep(2)

            # Scroll to make products visible
            self.driver.execute_script("window.scrollBy(0, 400);")
            time.sleep(1)

            # Find all Add to Cart buttons
            add_to_cart_buttons = self.wait.until(
                EC.presence_of_all_elements_located(Locators.ADD_TO_CART_BUTTONS)
            )

            if len(add_to_cart_buttons) > 0:
                # Click the first Add to Cart button (iMac after A-Z sorting)
                first_button = add_to_cart_buttons[0]

                # Scroll to the button
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_button)
                time.sleep(1)

                # Try regular click first
                try:
                    self.wait.until(EC.element_to_be_clickable(first_button))
                    first_button.click()
                except:
                    # Fallback to JavaScript click
                    self.driver.execute_script("arguments[0].click();", first_button)

                print("✓ Clicked 'Add to Cart' button")
                time.sleep(2)
            else:
                raise Exception("No Add to Cart buttons found on the page")

            # Step 6: Verify whether product is added to cart
            print("\nStep 6: Verifying product added to cart")
            success_message = self.wait.until(
                EC.visibility_of_element_located(Locators.SUCCESS_MESSAGE)
            )

            if success_message.is_displayed():
                message_text = success_message.text
                print(f"✓ Success message displayed: {message_text}")

                # Additional verification - check cart total
                cart_total = self.driver.find_element(*Locators.CART_TOTAL)
                cart_text = cart_total.text
                print(f"✓ Cart total updated: {cart_text}")

                if "1 item(s)" in cart_text or "1 item" in cart_text:
                    print("\n" + "=" * 50)
                    print("TEST PASSED: Product successfully added to cart!")
                    print("=" * 50)
                    return True
                else:
                    print("\n" + "=" * 50)
                    print("TEST FAILED: Cart count not updated correctly")
                    print("=" * 50)
                    return False
            else:
                print("\n" + "=" * 50)
                print("TEST FAILED: Success message not displayed")
                print("=" * 50)
                return False

        except Exception as e:
            print(f"\n❌ ERROR occurred: {str(e)}")
            print("\n" + "=" * 50)
            print("TEST FAILED: Exception occurred during execution")
            print("=" * 50)
            return False

    def run_test(self):
        """Main method to run the complete test"""
        print("\n" + "=" * 50)
        print("Starting Test Execution")
        print("=" * 50)

        self.setup()

        try:
            result = self.test_add_mac_to_cart()
            return result
        finally:
            self.teardown()


# Main execution
if __name__ == "__main__":
    test = TestTutorialsNinja()
    test.run_test()