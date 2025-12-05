from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
import allure


class CartPage(BasePage):
    """
    Shopping cart page object handling cart review and modification.
    
    Manages cart item validation, removal, and checkout initiation.
    Provides methods to verify cart state before proceeding to checkout.
    """
    
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CART_ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _CART_QUANTITIES = (By.CLASS_NAME, "cart_quantity")
    _REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[id^='remove']")
    _CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    _CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Verifying cart page is loaded")
    def is_cart_page_loaded(self) -> bool:
        """
        Confirms successful navigation to cart page.
        
        Returns:
            True if checkout button is visible
        """
        return self.is_element_visible(self._CHECKOUT_BUTTON)
    
    def get_cart_item_count(self) -> int:
        """
        Counts number of unique products in cart.
        
        Note: This counts line items, not total quantity if multiples
        of same product were added separately.
        
        Returns:
            Number of cart items
        """
        try:
            return len(self.find_elements(self._CART_ITEMS))
        except:
            return 0
    
    def get_cart_item_names(self) -> List[str]:
        """
        Extracts names of all products in cart.
        
        Returns:
            List of product names in cart order
        """
        elements = self.find_elements(self._CART_ITEM_NAMES)
        return [element.text for element in elements]
    
    def get_cart_item_prices(self) -> List[float]:
        """
        Extracts prices of all products in cart.
        
        Returns:
            List of prices as floats for calculation
        """
        elements = self.find_elements(self._CART_ITEM_PRICES)
        return [float(element.text.replace("$", "")) for element in elements]
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """
        Checks if specific product exists in cart.
        
        Args:
            product_name: Name of product to find
            
        Returns:
            True if product is in cart
        """
        cart_items = self.get_cart_item_names()
        return product_name in cart_items
    
    @allure.step("Removing product from cart: {product_name}")
    def remove_product_by_name(self, product_name: str) -> None:
        """
        Removes specific product from cart.
        
        Args:
            product_name: Exact name of product to remove
        """
        product_id = product_name.lower().replace(" ", "-")
        remove_button = (By.ID, f"remove-{product_id}")
        self.click(remove_button)
    
    @allure.step("Removing product from cart by index: {index}")
    def remove_product_by_index(self, index: int = 0) -> None:
        """
        Removes product by its position in cart.
        
        Args:
            index: Zero-based position of item to remove
        """
        buttons = self.find_elements(self._REMOVE_BUTTONS)
        if 0 <= index < len(buttons):
            buttons[index].click()
    
    @allure.step("Clearing all items from cart")
    def clear_cart(self) -> None:
        """
        Removes all products from cart sequentially.
        """
        while self.get_cart_item_count() > 0:
            self.remove_product_by_index(0)
    
    @allure.step("Continuing to shopping")
    def continue_shopping(self) -> None:
        """
        Returns to inventory page from cart.
        """
        self.click(self._CONTINUE_SHOPPING_BUTTON)
    
    @allure.step("Proceeding to checkout")
    def proceed_to_checkout(self) -> None:
        """
        Initiates checkout flow from cart.
        """
        self.click(self._CHECKOUT_BUTTON)
    
    def is_cart_empty(self) -> bool:
        """
        Determines if cart contains no items.
        
        Returns:
            True if cart is empty
        """
        return self.get_cart_item_count() == 0
    
    def get_total_price(self) -> float:
        """
        Calculates sum of all item prices in cart.
        
        Note: This is pre-tax subtotal as displayed on cart page.
        
        Returns:
            Total price as float
        """
        prices = self.get_cart_item_prices()
        return sum(prices)

