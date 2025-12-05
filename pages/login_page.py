from typing import Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """
    Login page object encapsulating authentication interactions.
    
    Handles user login functionality including standard, locked, and
    problematic user scenarios for comprehensive test coverage.
    """
    
    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    _ERROR_BUTTON = (By.CSS_SELECTOR, "button.error-button")
    
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
    
    @allure.step("Navigating to login page")
    def navigate(self) -> None:
        """
        Opens the application login page.
        """
        self.driver.get(self.config.BASE_URL)
    
    @allure.step("Logging in as: {username}")
    def login(self, username: str, password: str) -> None:
        """
        Performs login with provided credentials.
        
        This method handles the complete login flow including field population
        and submission. Use with various user types to test different scenarios.
        
        Args:
            username: User's login name
            password: User's password
        """
        self.send_keys(self._USERNAME_INPUT, username)
        self.send_keys(self._PASSWORD_INPUT, password)
        self.click(self._LOGIN_BUTTON)
    
    @allure.step("Quick login with user type: {user_type}")
    def login_with_user_type(self, user_type: str = "standard") -> None:
        """
        Convenience method for logging in with predefined user types.
        
        Retrieves credentials from config based on user type, reducing
        test code duplication and improving maintainability.
        
        Args:
            user_type: Type of user (standard, locked_out, problem, performance_glitch)
        """
        credentials = self.config.get_user_credentials(user_type)
        self.login(credentials["username"], credentials["password"])
    
    def get_error_message(self) -> str:
        """
        Retrieves error message text when login fails.
        
        Returns:
            Error message displayed to user
        """
        return self.get_text(self._ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Checks if error message is visible on page.
        
        Returns:
            True if error is displayed, False otherwise
        """
        return self.is_element_visible(self._ERROR_MESSAGE, timeout=3)
    
    @allure.step("Clearing error message")
    def clear_error_message(self) -> None:
        """
        Closes error message by clicking dismiss button.
        """
        if self.is_element_visible(self._ERROR_BUTTON, timeout=2):
            self.click(self._ERROR_BUTTON)
    
    def is_on_login_page(self) -> bool:
        """
        Verifies current page is login page.
        
        Checks for presence of login button rather than URL to handle
        potential redirects and maintain flexibility.
        
        Returns:
            True if on login page, False otherwise
        """
        return self.is_element_present(self._LOGIN_BUTTON)

