from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
import allure


class InventoryPage(BasePage):
    """
    Product inventory page object managing product listing and cart operations.
    
    Provides methods for filtering, sorting, and adding products to cart.
    Handles dynamic product lists and validates inventory state.
    """
    
    _INVENTORY_CONTAINER = (By.ID, "inventory_container")
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    _PRODUCT_TITLES = (By.CLASS_NAME, "inventory_item_name")
    _PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _PRODUCT_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    _REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    _BURGER_MENU = (By.ID, "react-burger-menu-btn")
    _LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Verifying inventory page is loaded")
    def is_inventory_page_loaded(self) -> bool:
        """
        Confirms successful navigation to inventory page.
        
        Returns:
            True if inventory container is visible
        """
        return self.is_element_visible(self._INVENTORY_CONTAINER)
    
    def get_product_count(self) -> int:
        """
        Counts number of products displayed on page.
        
        Returns:
            Total number of inventory items
        """
        return len(self.find_elements(self._INVENTORY_ITEMS))
    
    def get_all_product_names(self) -> List[str]:
        """
        Extracts names of all displayed products.
        
        Returns:
            List of product names in display order
        """
        elements = self.find_elements(self._PRODUCT_TITLES)
        return [element.text for element in elements]
    
    def get_all_product_prices(self) -> List[float]:
        """
        Extracts prices of all displayed products.
        
        Parses price strings to float for numerical comparison in tests.
        
        Returns:
            List of product prices as floats
        """
        elements = self.find_elements(self._PRODUCT_PRICES)
        return [float(element.text.replace("$", "")) for element in elements]
    
    @allure.step("Adding product to cart: {product_name}")
    def add_product_to_cart_by_name(self, product_name: str) -> None:
        """
        Adds specific product to cart by its display name.
        
        Args:
            product_name: Exact name of product to add
        """
        product_id = product_name.lower().replace(" ", "-")
        add_button = (By.ID, f"add-to-cart-{product_id}")
        self.click(add_button)
    
    @allure.step("Adding product to cart by index: {index}")
    def add_product_to_cart_by_index(self, index: int = 0) -> None:
        """
        Adds product to cart by its position in list.
        
        Args:
            index: Zero-based position of product (0 = first product)
        """
        buttons = self.find_elements(self._ADD_TO_CART_BUTTONS)
        if 0 <= index < len(buttons):
            buttons[index].click()
    
    @allure.step("Adding multiple products to cart")
    def add_multiple_products_to_cart(self, count: int = 3) -> List[str]:
        """
        Adds specified number of products to cart.
        
        Returns names of added products for verification in tests.
        
        Args:
            count: Number of products to add
            
        Returns:
            List of product names that were added
        """
        product_names = self.get_all_product_names()
        added_products = []
        
        for i in range(min(count, len(product_names))):
            product_name = product_names[i]
            self.add_product_to_cart_by_name(product_name)
            added_products.append(product_name)
        
        return added_products
    
    @allure.step("Removing product from cart: {product_name}")
    def remove_product_from_cart_by_name(self, product_name: str) -> None:
        """
        Removes specific product from cart by its display name.
        
        Args:
            product_name: Exact name of product to remove
        """
        product_id = product_name.lower().replace(" ", "-")
        remove_button = (By.ID, f"remove-{product_id}")
        self.click(remove_button)
    
    def get_cart_badge_count(self) -> int:
        """
        Reads number displayed on cart badge.
        
        Returns:
            Item count in cart, or 0 if badge not visible
        """
        if self.is_element_visible(self._CART_BADGE, timeout=2):
            return int(self.get_text(self._CART_BADGE))
        return 0
    
    @allure.step("Navigating to cart")
    def go_to_cart(self) -> None:
        """
        Clicks cart icon to view cart contents.
        """
        self.click(self._CART_LINK)
    
    @allure.step("Sorting products by: {sort_option}")
    def sort_products(self, sort_option: str) -> None:
        """
        Applies sorting to product list.
        
        Args:
            sort_option: One of 'az', 'za', 'lohi', 'hilo'
        """
        sort_values = {
            "az": "az",
            "za": "za",
            "lohi": "lohi",
            "hilo": "hilo"
        }
        
        dropdown = self.find_element(self._SORT_DROPDOWN)
        dropdown.click()
        
        option_locator = (By.CSS_SELECTOR, f"option[value='{sort_values.get(sort_option, 'az')}']")
        self.click(option_locator)
    
    @allure.step("Logging out from application")
    def logout(self) -> None:
        """
        Performs logout operation via burger menu.
        """
        self.click(self._BURGER_MENU)
        self.click(self._LOGOUT_LINK)
    
    def get_product_details(self, product_index: int = 0) -> Dict[str, str]:
        """
        Retrieves all details for a specific product.
        
        Args:
            product_index: Zero-based position of product
            
        Returns:
            Dictionary containing name, price, and description
        """
        items = self.find_elements(self._INVENTORY_ITEMS)
        if product_index < len(items):
            item = items[product_index]
            return {
                "name": item.find_element(By.CLASS_NAME, "inventory_item_name").text,
                "price": item.find_element(By.CLASS_NAME, "inventory_item_price").text,
                "description": item.find_element(By.CLASS_NAME, "inventory_item_desc").text
            }
        return {}

