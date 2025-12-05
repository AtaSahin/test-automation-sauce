import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config import Config


@allure.feature("Authentication")
@allure.story("User Login")
class TestLogin:
    """
    Test suite validating login functionality across different scenarios.
    
    Covers standard login, error handling, locked users, and invalid credentials.
    """
    
    @allure.title("Successful login with standard user")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_successful_login_standard_user(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Verifies standard user can authenticate and access inventory.
        """
        login_page.navigate()
        login_page.login_with_user_type("standard")
        
        assert inventory_page.is_inventory_page_loaded(), "Inventory page did not load after login"
        assert inventory_page.get_product_count() > 0, "No products displayed after login"
    
    @allure.title("Login attempt with locked out user")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_locked_out_user(self, login_page: LoginPage):
        """
        Validates error message when locked user attempts login.
        """
        login_page.navigate()
        login_page.login_with_user_type("locked_out")
        
        assert login_page.is_error_displayed(), "Error message not displayed for locked user"
        error_text = login_page.get_error_message()
        assert "locked out" in error_text.lower(), f"Unexpected error message: {error_text}"
    
    @allure.title("Login with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_invalid_credentials(self, login_page: LoginPage):
        """
        Ensures proper error handling for incorrect username/password.
        """
        login_page.navigate()
        login_page.login("invalid_user", "wrong_password")
        
        assert login_page.is_error_displayed(), "No error shown for invalid credentials"
        error_text = login_page.get_error_message()
        assert "do not match" in error_text.lower() or "invalid" in error_text.lower()
    
    @allure.title("Login with empty username")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_username(self, login_page: LoginPage):
        """
        Validates form validation for missing username.
        """
        login_page.navigate()
        login_page.login("", Config.PASSWORD)
        
        assert login_page.is_error_displayed(), "No error shown for empty username"
        error_text = login_page.get_error_message()
        assert "required" in error_text.lower() or "username" in error_text.lower()
    
    @allure.title("Login with empty password")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_password(self, login_page: LoginPage):
        """
        Validates form validation for missing password.
        """
        login_page.navigate()
        login_page.login(Config.STANDARD_USER, "")
        
        assert login_page.is_error_displayed(), "No error shown for empty password"
        error_text = login_page.get_error_message()
        assert "required" in error_text.lower() or "password" in error_text.lower()
    
    @allure.title("Login with both fields empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_empty_credentials(self, login_page: LoginPage):
        """
        Validates form validation when all fields are empty.
        """
        login_page.navigate()
        login_page.login("", "")
        
        assert login_page.is_error_displayed(), "No error shown for empty credentials"
    
    @allure.title("Problem user login and behavior")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_problem_user_login(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Verifies problem user can login despite potential UI issues.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        assert inventory_page.is_inventory_page_loaded(), "Problem user could not access inventory"
    
    @allure.title("Performance glitch user login")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_performance_glitch_user_login(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Tests login with user experiencing performance delays.
        """
        login_page.navigate()
        login_page.login_with_user_type("performance_glitch")
        
        assert inventory_page.is_inventory_page_loaded(), "Performance glitch user login failed"

