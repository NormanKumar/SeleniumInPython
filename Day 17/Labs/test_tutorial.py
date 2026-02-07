import sys
import time
from pathlib import Path

# Add parent directory to path to import locators
sys.path.append(str(Path(__file__).parent.parent))

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Locator import *


class TestTutorialNinja:
    """Test class for Tutorial Ninja website automation"""

    def __init__(self):
        self.driver = None
        self.wait = None
        self.locators = TutorialNinjaLocators()

    def setup(self):
        """Setup method to initialize the browser"""
        edge_options = Options()
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Edge(options=edge_options)
        self.wait = WebDriverWait(self.driver, 15)
        print("Browser setup completed")

    def teardown(self):
        """Teardown method to close the browser"""
        if self.driver:
            time.sleep(2)
            self.driver.quit()
            print("Browser closed successfully")

    def take_screenshot(self, name):
        """Take screenshot for debugging"""
        try:
            self.driver.save_screenshot(f"{name}.png")
            print(f"Screenshot saved: {name}.png")
        except Exception as e:
            print(f"Failed to save screenshot: {str(e)}")

    def test_desktop_mac_product(self):
        """
        Test Case 1: Navigate to Desktops > Mac and sort products
        Steps:
        1. Open URL
        2. Go to 'Desktops' tab
        3. Click on 'Mac'
        4. Select 'Name(A-Z)' from 'Sort By' dropdown
        5. Click on 'Add to Cart' button
        """
        try:
            # Step 1: Open the URL
            print("\n=== Test Case 1: Desktop Mac Product ===")
            self.driver.get("https://tutorialsninja.com/demo/index.php?route=common/home")
            print("Step 1: Opened URL successfully")
            time.sleep(2)

            # Step 2: Go to 'Desktops' tab
            desktops_tab = self.wait.until(
                EC.element_to_be_clickable(self.locators.DESKTOPS_TAB)
            )
            desktops_tab.click()
            print("Step 2: Clicked on 'Desktops' tab")
            time.sleep(1)

            # Step 3: Click on 'Mac'
            mac_link = self.wait.until(
                EC.element_to_be_clickable(self.locators.MAC_LINK)
            )
            mac_link.click()
            print("Step 3: Clicked on 'Mac' link")
            time.sleep(2)

            # Step 4: Select 'Name (A - Z)' from Sort By dropdown
            sort_dropdown = self.wait.until(
                EC.presence_of_element_located(self.locators.SORT_BY_DROPDOWN)
            )
            select = Select(sort_dropdown)
            select.select_by_visible_text("Name (A - Z)")
            print("Step 4: Selected 'Name (A - Z)' from Sort By dropdown")
            time.sleep(3)  # Wait for sorting to apply and page to reload

            # Step 5: Click on 'Add to Cart' button
            print("Step 5: Attempting to click 'Add to Cart' button...")

            # Try primary locator
            try:
                add_to_cart = self.wait.until(
                    EC.element_to_be_clickable(self.locators.ADD_TO_CART_BUTTON_ALT)
                )
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_to_cart)
                time.sleep(1)
                add_to_cart.click()
                print("Step 5: Clicked on 'Add to Cart' button")
                time.sleep(2)

            except (TimeoutException, NoSuchElementException) as e:
                print(f"Primary locator failed: {str(e)}")
                self.take_screenshot("add_to_cart_error")

                # Try alternative approach - find all add to cart buttons and click first
                print("Trying alternative method...")
                buttons = self.driver.find_elements(By.XPATH, "//button[contains(@onclick, 'cart.add')]")
                if buttons:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", buttons[0])
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", buttons[0])
                    print("Step 5: Clicked on 'Add to Cart' button using alternative method")
                    time.sleep(2)
                else:
                    raise Exception("No 'Add to Cart' button found")

            print("✓ Test Case 1 completed successfully\n")

        except Exception as e:
            print(f"✗ Test Case 1 failed: {str(e)}")
            self.take_screenshot("test_case_1_error")
            raise

    def test_mobile_search(self):
        """
        Test Case 2: Search for Mobile and test search criteria
        Steps:
        1. Enter 'Mobile' in Search text box
        2. Click on Search button
        3. Wait for page to load
        4. Clear the text from 'Search Criteria' text box
        5. Click on 'Search in product descriptions' checkbox
        6. Keep active for 5 seconds
        7. Click on Search button
        8. Display mobile search results
        9. Close browser
        """
        try:
            print("=== Test Case 2: Mobile Search ===")

            # Step 1: Enter 'Mobile' in Search text box
            search_box = self.wait.until(
                EC.presence_of_element_located(self.locators.SEARCH_TEXTBOX)
            )
            search_box.clear()
            search_box.send_keys("Mobile")
            print("Step 1: Entered 'Mobile' in search box")
            time.sleep(1)

            # Step 2: Click on Search button
            search_button = self.wait.until(
                EC.element_to_be_clickable(self.locators.SEARCH_BUTTON)
            )
            search_button.click()
            print("Step 2: Clicked on Search button")

            # Step 3: Wait for page to load
            self.wait.until(
                EC.presence_of_element_located(self.locators.SEARCH_CRITERIA_TEXTBOX)
            )
            print("Step 3: Search results page loaded")
            time.sleep(2)

            # Step 4: Clear the text from 'Search Criteria' text box
            search_criteria = self.driver.find_element(*self.locators.SEARCH_CRITERIA_TEXTBOX)
            search_criteria.clear()
            print("Step 4: Cleared text from 'Search Criteria' text box")
            time.sleep(1)

            # Step 5: Click on 'Search in product descriptions' checkbox
            description_checkbox = self.driver.find_element(*self.locators.SEARCH_IN_DESCRIPTION_CHECKBOX)
            if not description_checkbox.is_selected():
                description_checkbox.click()
                print("Step 5: Clicked on 'Search in product descriptions' checkbox")

            # Step 6: Keep active for 5 seconds
            print("Step 6: Keeping checkbox active for 5 seconds...")
            time.sleep(5)

            # Step 7: Click on Search button to search with description enabled
            search_btn_page = self.wait.until(
                EC.element_to_be_clickable(self.locators.SEARCH_BUTTON_PAGE)
            )
            search_btn_page.click()
            print("Step 7: Clicked on Search button")
            time.sleep(3)  # Wait for results to load

            # Step 8: Display mobile search results
            print("\n" + "=" * 60)
            print("MOBILE SEARCH RESULTS:")
            print("=" * 60)

            try:
                # Find all product containers
                products = self.driver.find_elements(By.XPATH, "//div[@class='product-thumb']")

                if products:
                    print(f"\nTotal products found: {len(products)}\n")

                    for index, product in enumerate(products, 1):
                        try:
                            # Get product name
                            product_name = product.find_element(By.XPATH, ".//h4/a").text

                            # Get product price
                            try:
                                price = product.find_element(By.XPATH, ".//p[@class='price']").text
                            except:
                                price = "Price not available"

                            # Get product description
                            try:
                                description = product.find_element(By.XPATH, ".//p[not(@class)]").text
                                # Truncate description if too long
                                if len(description) > 100:
                                    description = description[:100] + "..."
                            except:
                                description = "No description available"

                            print(f"Product {index}:")
                            print(f"  Name: {product_name}")
                            print(f"  Price: {price}")
                            print(f"  Description: {description}")
                            print("-" * 60)

                        except Exception as e:
                            print(f"  Error reading product {index}: {str(e)}")
                            print("-" * 60)
                else:
                    print("No products found in search results")

            except Exception as e:
                print(f"Error displaying search results: {str(e)}")
                self.take_screenshot("search_results_error")

            print("=" * 60 + "\n")

            # Take screenshot of results
            self.take_screenshot("mobile_search_results")
            print("Step 8: Displayed mobile search results\n")

            print("✓ Test Case 2 completed successfully\n")

        except Exception as e:
            print(f"✗ Test Case 2 failed: {str(e)}")
            self.take_screenshot("test_case_2_error")
            raise

    def run_all_tests(self):
        """Run all test cases"""
        try:
            self.setup()
            self.test_desktop_mac_product()
            self.test_mobile_search()
            print("=" * 50)
            print("ALL TESTS PASSED SUCCESSFULLY!")
            print("=" * 50)
        except Exception as e:
            print("=" * 50)
            print(f"TEST EXECUTION FAILED: {str(e)}")
            print("=" * 50)
        finally:
            self.teardown()


if __name__ == "__main__":
    # Create test instance and run all tests
    test = TestTutorialNinja()
    test.run_all_tests()
