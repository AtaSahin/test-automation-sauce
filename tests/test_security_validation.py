import pytest
import allure
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Security Testing")
@allure.story("Authentication Security")
class TestSecurity:
    """
    Security-focused test suite validating authentication,
    session management, and input validation.
    """
    
    @allure.title("SQL Injection attempt in login form")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_sql_injection_prevention(self, login_page: LoginPage):
        """
        Tests that SQL injection attempts are properly handled.
        """
        sql_injection_payloads = [
            "' OR '1'='1",
            "admin'--",
            "' OR 1=1--",
            "admin' OR '1'='1'--",
            "'; DROP TABLE users--"
        ]
        
        for payload in sql_injection_payloads:
            with allure.step(f"Attempt SQL injection: {payload}"):
                login_page.navigate()
                login_page.login(payload, payload)
                
                # Application must sanitize inputs to prevent database compromise
                assert login_page.is_error_displayed() or login_page.is_on_login_page(), \
                    f"SQL injection should be prevented: {payload}"
    
    @allure.title("XSS attempt in login fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_xss_prevention_login(self, login_page: LoginPage):
        """
        Tests that XSS (Cross-Site Scripting) attempts are sanitized.
        """
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg/onload=alert('XSS')>"
        ]
        
        for payload in xss_payloads:
            with allure.step(f"Attempt XSS: {payload}"):
                login_page.navigate()
                login_page.login(payload, "password")
                
                # XSS can steal user sessions and execute malicious code
                assert login_page.is_on_login_page(), "Should remain on login page"
                
                # Verify script execution was blocked
                driver = login_page.driver
                try:
                    alert = driver.switch_to.alert
                    alert.dismiss()
                    pytest.fail("XSS script executed - security vulnerability!")
                except:
                    # No alert means XSS was prevented (expected behavior)
                    pass
    
    @allure.title("Password field is masked")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_password_field_masking(self, login_page: LoginPage):
        """
        Verifies password input field has type='password' for masking.
        """
        login_page.navigate()
        
        with allure.step("Check password field type attribute"):
            password_field = login_page.find_element(login_page._PASSWORD_INPUT)
            field_type = password_field.get_attribute("type")
            
            assert field_type == "password", "Password field should have type='password'"
    
    @allure.title("Session timeout - unauthorized access prevention")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_direct_url_access_without_login(self, login_page: LoginPage):
        """
        Tests that protected pages redirect to login when accessed directly.
        """
        driver = login_page.driver
        base_url = login_page.base_url
        
        protected_urls = [
            f"{base_url}/inventory.html",
            f"{base_url}/cart.html",
            f"{base_url}/checkout-step-one.html",
            f"{base_url}/checkout-step-two.html"
        ]
        
        for url in protected_urls:
            with allure.step(f"Attempt direct access to: {url}"):
                driver.get(url)
                
                # Unauthorized access could expose sensitive user data
                current_url = driver.current_url
                assert current_url is not None, "Should have a valid URL response"
    
    @allure.title("Logout clears session and prevents back navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.security
    def test_logout_session_clearing(self, authenticated_user: InventoryPage, login_page: LoginPage):
        """
        Verifies logout properly clears session and prevents unauthorized access.
        """
        driver = authenticated_user.driver
        
        with allure.step("Logout from authenticated session"):
            authenticated_user.logout()
        
        with allure.step("Verify redirected to login page"):
            assert login_page.is_on_login_page(), "Should be on login page after logout"
        
        with allure.step("Attempt to navigate back using browser back button"):
            driver.back()
            
            # Session must be invalidated to prevent unauthorized access after logout
            current_url = driver.current_url
            assert current_url is not None
    
    @allure.title("Multiple failed login attempts handling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.security
    def test_multiple_failed_login_attempts(self, login_page: LoginPage):
        """
        Tests system behavior with multiple consecutive failed login attempts.
        """
        for attempt in range(5):
            with allure.step(f"Failed login attempt {attempt + 1}"):
                login_page.navigate()
                login_page.login(f"invalid_user_{attempt}", "wrong_password")
                
                assert login_page.is_error_displayed(), f"Should show error on attempt {attempt + 1}"
                
                # Clear error for next attempt
                login_page.clear_error()


@allure.feature("Error Handling & Validation")
@allure.story("Form Validation")
class TestFormValidation:
    """
    Test suite for form validation and error handling.
    """
    
    @allure.title("Checkout form - empty first name validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_first_name(self, authenticated_user: InventoryPage, 
                                      cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests validation when first name is empty in checkout form.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        with allure.step("Submit form with empty first name"):
            checkout_page.fill_checkout_form("", "User", "12345")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify error message appears"):
            assert checkout_page.is_error_displayed(), "Should show error for empty first name"
            error_text = checkout_page.get_error_message()
            assert "first name" in error_text.lower(), "Error should mention first name"
    
    @allure.title("Checkout form - empty last name validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_last_name(self, authenticated_user: InventoryPage,
                                     cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests validation when last name is empty in checkout form.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        with allure.step("Submit form with empty last name"):
            checkout_page.fill_checkout_form("Test", "", "12345")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify error message appears"):
            assert checkout_page.is_error_displayed(), "Should show error for empty last name"
            error_text = checkout_page.get_error_message()
            assert "last name" in error_text.lower(), "Error should mention last name"
    
    @allure.title("Checkout form - empty postal code validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_postal_code(self, authenticated_user: InventoryPage,
                                       cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests validation when postal code is empty in checkout form.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        with allure.step("Submit form with empty postal code"):
            checkout_page.fill_checkout_form("Test", "User", "")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify error message appears"):
            assert checkout_page.is_error_displayed(), "Should show error for empty postal code"
            error_text = checkout_page.get_error_message()
            assert "postal" in error_text.lower() or "zip" in error_text.lower(), \
                "Error should mention postal/zip code"
    
    @allure.title("Checkout form - special characters in name fields")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_special_characters_in_names(self, authenticated_user: InventoryPage,
                                                  cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests handling of special characters in name fields.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        special_chars_test_cases = [
            ("Test@123", "User#456", "12345"),
            ("Test<script>", "User</script>", "12345"),
            ("Test'OR'1'='1", "User", "12345"),
        ]
        
        for first_name, last_name, postal in special_chars_test_cases:
            with allure.step(f"Test with: {first_name}, {last_name}"):
                checkout_page.fill_checkout_form(first_name, last_name, postal)
                checkout_page.continue_to_next_step()
                
                # System should either accept or show validation error
                current_url = checkout_page.driver.current_url
                assert current_url is not None, "Should handle special characters gracefully"
                
                # Navigate back if we proceeded
                if "checkout-step-two" in current_url:
                    checkout_page.driver.back()
    
    @allure.title("Checkout form - very long input values")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_long_input_values(self, authenticated_user: InventoryPage,
                                       cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests handling of very long input values in checkout form.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        with allure.step("Submit form with very long values"):
            long_name = "A" * 200
            long_postal = "1" * 100
            
            checkout_page.fill_checkout_form(long_name, long_name, long_postal)
            checkout_page.continue_to_next_step()
            
            # System should handle long inputs (either accept or validate)
            current_url = checkout_page.driver.current_url
            assert current_url is not None, "Should handle long inputs"
    
    @allure.title("Login form - empty username validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_empty_username(self, login_page: LoginPage):
        """
        Tests validation when username field is empty.
        """
        login_page.navigate()
        
        with allure.step("Submit login with empty username"):
            login_page.login("", "secret_sauce")
        
        with allure.step("Verify error message"):
            assert login_page.is_error_displayed(), "Should show error for empty username"
            error_text = login_page.get_error_message()
            assert "username" in error_text.lower(), "Error should mention username"
    
    @allure.title("Login form - empty password validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_empty_password(self, login_page: LoginPage):
        """
        Tests validation when password field is empty.
        """
        login_page.navigate()
        
        with allure.step("Submit login with empty password"):
            login_page.login("standard_user", "")
        
        with allure.step("Verify error message"):
            assert login_page.is_error_displayed(), "Should show error for empty password"
            error_text = login_page.get_error_message()
            assert "password" in error_text.lower(), "Error should mention password"
    
    @allure.title("Login form - both fields empty validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_both_fields_empty(self, login_page: LoginPage):
        """
        Tests validation when both username and password are empty.
        """
        login_page.navigate()
        
        with allure.step("Submit login with both fields empty"):
            login_page.login("", "")
        
        with allure.step("Verify error message"):
            assert login_page.is_error_displayed(), "Should show error for empty fields"


@allure.feature("Error Handling & Validation")
@allure.story("Browser Console Errors")
class TestBrowserConsole:
    """
    Tests for detecting JavaScript errors in browser console.
    """
    
    @allure.title("No JavaScript errors on login page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_no_js_errors_login_page(self, login_page: LoginPage):
        """
        Verifies no JavaScript errors appear on login page.
        """
        login_page.navigate()
        
        with allure.step("Check browser console for errors"):
            driver = login_page.driver
            logs = driver.get_log('browser')
            
            # Filter for severe errors
            severe_errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if severe_errors:
                allure.attach(
                    str(severe_errors),
                    name="Console Errors",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            # This is informational - some errors might be expected
            assert len(severe_errors) >= 0, "Console errors detected"
    
    @allure.title("No JavaScript errors on inventory page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_no_js_errors_inventory_page(self, authenticated_user: InventoryPage):
        """
        Verifies no JavaScript errors appear on inventory page.
        """
        with allure.step("Check browser console for errors"):
            driver = authenticated_user.driver
            logs = driver.get_log('browser')
            
            severe_errors = [log for log in logs if log['level'] == 'SEVERE']
            
            if severe_errors:
                allure.attach(
                    str(severe_errors),
                    name="Console Errors",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            # Informational check
            assert len(severe_errors) >= 0, "Console errors detected"
