from selenium.webdriver.common.by import By
class Locators:
    """Class to store all locators for the application"""

    # Navigation
    DESKTOPS_TAB = (By.LINK_TEXT, "Desktops")
    MAC_OPTION = (By.LINK_TEXT, "Mac (1)")

    # Sorting
    SORT_BY_DROPDOWN = (By.ID, "input-sort")

    # Product - iMac specific
    IMAC_PRODUCT = (By.LINK_TEXT, "iMac")
    ADD_TO_CART_BUTTONS = (By.XPATH, "//button[contains(@onclick, 'cart.add')]")
    PRODUCT_GRID = (By.CLASS_NAME, "product-layout")

    # Success Message
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "div.alert.alert-success")
    SUCCESS_MESSAGE_TEXT = (By.XPATH, "//div[contains(@class, 'alert-success')]")

    # Cart
    CART_BUTTON = (By.ID, "cart")
    CART_TOTAL = (By.ID, "cart-total")