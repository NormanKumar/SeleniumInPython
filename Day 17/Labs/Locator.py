from selenium.webdriver.common.by import By


class TutorialNinjaLocators:
    """Locator class containing all web element locators"""

    # Header Navigation
    DESKTOPS_TAB = (By.LINK_TEXT, "Desktops")
    MAC_LINK = (By.LINK_TEXT, "Mac (1)")

    # Product Listing
    SORT_BY_DROPDOWN = (By.ID, "input-sort")
    # Updated locator for Add to Cart button - more specific
    ADD_TO_CART_BUTTON = (By.XPATH, "//div[@class='button-group']//button[@type='button'][1]")
    # Alternative locator
    ADD_TO_CART_BUTTON_ALT = (By.CSS_SELECTOR, "button[onclick*='cart.add']")

    # Search
    SEARCH_TEXTBOX = (By.NAME, "search")
    SEARCH_BUTTON = (By.XPATH, "//button[@class='btn btn-default btn-lg']")

    # Search Page
    SEARCH_CRITERIA_TEXTBOX = (By.ID, "input-search")
    SEARCH_IN_DESCRIPTION_CHECKBOX = (By.ID, "description")
    SEARCH_BUTTON_PAGE = (By.ID, "button-search")