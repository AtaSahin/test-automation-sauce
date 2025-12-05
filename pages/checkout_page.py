from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
import allure


class CheckoutPage(BasePage):
    """
    Checkout page object managing purchase flow completion.
    
    Handles customer information entry, order review, and final confirmation.
    Split into step one (information), step two (overview), and completion.
    """
    
    _FIRST_NAME_INPUT = (By.ID, "first-name")
    _LAST_NAME_INPUT = (By.ID, "last-name")
    _POSTAL_CODE_INPUT = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _CANCEL_BUTTON = (By.ID, "cancel")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    _SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    _SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    _FINISH_BUTTON = (By.ID, "finish")
    _BACK_HOME_BUTTON = (By.ID, "back-to-products")
    
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Filling checkout information: {first_name} {last_name}, {postal_code}")
    def fill_checkout_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Completes customer information form on checkout step one.
        
        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            postal_code: Zip/postal code
        """
        first_name_field = self.find_element(self._FIRST_NAME_INPUT)
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        
        last_name_field = self.find_element(self._LAST_NAME_INPUT)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        
        postal_code_field = self.find_element(self._POSTAL_CODE_INPUT)
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
    
    @allure.step("Continuing to checkout overview")
    def click_continue(self) -> None:
        """
        Submits customer information and proceeds to order review.
        """
        self.click(self._CONTINUE_BUTTON)
        self.is_element_visible(self._SUMMARY_SUBTOTAL, timeout=15)
    
    @allure.step("Completing checkout with info: {first_name} {last_name}")
    def complete_checkout_step_one(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Convenience method combining form fill and submission.
        
        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            postal_code: Zip/postal code
        """
        self.fill_checkout_information(first_name, last_name, postal_code)
        self.click_continue()
    
    # Alias methods for test compatibility
    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Alias for fill_checkout_information"""
        return self.fill_checkout_information(first_name, last_name, postal_code)
    
    def continue_to_next_step(self) -> None:
        """Alias for click_continue"""
        return self.click_continue()
    
    def cancel_checkout(self) -> None:
        """
        Aborts checkout process and returns to cart.
        """
        self.click(self._CANCEL_BUTTON)
    
    def get_error_message(self) -> str:
        """
        Retrieves validation error message from checkout form.
        
        Returns:
            Error message text
        """
        return self.get_text(self._ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Checks if form validation error is shown.
        
        Returns:
            True if error message is visible
        """
        return self.is_element_visible(self._ERROR_MESSAGE, timeout=3)
    
    def get_subtotal(self) -> float:
        """
        Extracts subtotal amount from order summary.
        
        Returns:
            Subtotal as float
        """
        text = self.get_text(self._SUMMARY_SUBTOTAL)
        return float(text.replace("Item total: $", ""))
    
    def get_tax(self) -> float:
        """
        Extracts tax amount from order summary.
        
        Returns:
            Tax amount as float
        """
        text = self.get_text(self._SUMMARY_TAX)
        return float(text.replace("Tax: $", ""))
    
    def get_total(self) -> float:
        """
        Extracts final total from order summary.
        
        Returns:
            Total amount including tax as float
        """
        text = self.get_text(self._SUMMARY_TOTAL)
        return float(text.replace("Total: $", ""))
    
    @allure.step("Finishing order")
    def finish_checkout(self) -> None:
        """
        Completes purchase on order review page.
        """
        self.click(self._FINISH_BUTTON, scroll_first=True)
    
    def is_checkout_complete(self) -> bool:
        """
        Verifies order completion page is displayed.
        
        Returns:
            True if completion header is visible
        """
        return self.is_element_visible(self._COMPLETE_HEADER)
    
    def get_completion_message(self) -> str:
        """
        Retrieves order confirmation message.
        
        Returns:
            Confirmation header text
        """
        return self.get_text(self._COMPLETE_HEADER)
    
    @allure.step("Returning to products page")
    def back_to_home(self) -> None:
        """
        Navigates back to inventory after order completion.
        """
        self.click(self._BACK_HOME_BUTTON)

