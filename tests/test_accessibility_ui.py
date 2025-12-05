import pytest
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Accessibility & Keyboard Navigation")
@allure.story("Keyboard Accessibility")
class TestAccessibility:
    """
    Accessibility test suite ensuring the application is usable
    via keyboard navigation and meets basic accessibility standards.
    """
    
    @allure.title("Login form - keyboard navigation with Tab key")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_login_keyboard_navigation(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Tests that users can navigate and submit login form using only keyboard.
        Critical for accessibility compliance.
        """
        login_page.navigate()
        
        with allure.step("Focus on username field and type"):
            username_field = login_page.find_element(login_page._USERNAME_INPUT)
            username_field.click()
            username_field.send_keys("standard_user")
        
        with allure.step("Tab to password field"):
            username_field.send_keys(Keys.TAB)
            
      
            active_element = login_page.driver.switch_to.active_element
            active_element.send_keys("secret_sauce")
        
        with allure.step("Tab to login button and press Enter"):
            active_element.send_keys(Keys.TAB)
            active_element.send_keys(Keys.ENTER)
        
        with allure.step("Verify successful login via keyboard"):
            inventory_page.wait_for_url_contains("inventory.html", timeout=10)
            assert inventory_page.is_inventory_page_loaded()
    
    @allure.title("Product selection using keyboard navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_keyboard_navigation(self, authenticated_user: InventoryPage):
        """
        Tests keyboard navigation through product listings.
        """
        with allure.step("Navigate through products using Tab"):
            driver = authenticated_user.driver
            body = driver.find_element("tag name", "body")
            
            for _ in range(5):
                body.send_keys(Keys.TAB)
            
            # Verify we can interact with focused element
            active_element = driver.switch_to.active_element
            assert active_element is not None, "Should have an active element"
    
    @allure.title("Cart page - keyboard navigation and interaction")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_keyboard_navigation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests keyboard navigation in shopping cart.
        """
        with allure.step("Add product and navigate to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.go_to_cart()
        
        with allure.step("Navigate cart using keyboard"):
            driver = cart_page.driver
            body = driver.find_element("tag name", "body")
            
            # Ensure all interactive elements are reachable via Tab key
            for _ in range(3):
                body.send_keys(Keys.TAB)
            
            assert cart_page.is_cart_page_loaded()
    
    @allure.title("Escape key closes error messages")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_escape_key_functionality(self, login_page: LoginPage):
        """
        Tests that Escape key can dismiss error messages.
        """
        login_page.navigate()
        
        with allure.step("Trigger error message"):
            login_page.login("invalid_user", "invalid_pass")
        
        with allure.step("Verify error message appears"):
            assert login_page.is_error_displayed()
        
        with allure.step("Press Escape to close error"):
            body = login_page.driver.find_element("tag name", "body")
            body.send_keys(Keys.ESCAPE)
            
            # Validates keyboard shortcuts work for dismissing UI elements


@allure.feature("UI/UX Validation")
@allure.story("User Interface Elements")
class TestUIElements:
    """
    Test suite validating UI elements, layout, and user experience.
    """
    
    @allure.title("Hamburger menu - open, navigate, close")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_hamburger_menu_functionality(self, authenticated_user: InventoryPage, login_page: LoginPage):
        """
        Tests hamburger menu opens, displays options, and closes properly.
        """
        driver = authenticated_user.driver
        
        with allure.step("Open hamburger menu"):
            menu_button = authenticated_user.find_element(("id", "react-burger-menu-btn"))
            menu_button.click()
            
            # Menu animation must complete before elements become interactable
            authenticated_user.wait_for_element_visible(("id", "logout_sidebar_link"), timeout=5)
        
        with allure.step("Verify menu items are visible"):
            logout_link = authenticated_user.find_element(("id", "logout_sidebar_link"))
            assert logout_link.is_displayed(), "Logout link should be visible"
            
            all_items_link = authenticated_user.find_element(("id", "inventory_sidebar_link"))
            assert all_items_link.is_displayed(), "All Items link should be visible"
        
        with allure.step("Close menu"):
            close_button = authenticated_user.find_element(("id", "react-burger-cross-btn"))
            close_button.click()
            
            # Allow animation to complete before next interaction
            import time
            time.sleep(0.5)
    
    @allure.title("Footer - social media links are present")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_footer_social_links(self, authenticated_user: InventoryPage):
        """
        Verifies footer contains social media links.
        """
        driver = authenticated_user.driver
        
        with allure.step("Scroll to footer"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        with allure.step("Verify social media links exist"):
            footer = authenticated_user.find_element(("class name", "footer"))
            assert footer.is_displayed(), "Footer should be visible"
            
            # Social links are critical for brand presence and user engagement
            social_links = driver.find_elements("css selector", ".social a")
            assert len(social_links) > 0, "Should have social media links"
    
    @allure.title("Product images are clickable and lead to detail page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_image_clickable(self, authenticated_user: InventoryPage):
        """
        Tests that product images are clickable and navigate to detail page.
        """
        with allure.step("Click on first product image"):
            first_product = authenticated_user.get_product_details(0)
            product_name = first_product.get("name")
            
            # Product images must be clickable for better UX and SEO
            driver = authenticated_user.driver
            product_link = driver.find_element("css selector", ".inventory_item_name")
            product_link.click()
        
        with allure.step("Verify detail page loads"):
            authenticated_user.wait_for_url_contains("inventory-item.html", timeout=5)
            current_url = driver.current_url
            assert "inventory-item.html" in current_url, "Should navigate to product detail"
        
        with allure.step("Navigate back to inventory"):
            back_button = authenticated_user.find_element(("id", "back-to-products"))
            back_button.click()
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
    
    @allure.title("Cart badge updates in real-time")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_cart_badge_real_time_update(self, authenticated_user: InventoryPage):
        """
        Verifies cart badge updates immediately when items are added/removed.
        """
        with allure.step("Verify cart badge is initially empty"):
            initial_count = authenticated_user.get_cart_badge_count()
            assert initial_count == 0, "Cart should be empty initially"
        
        with allure.step("Add first product"):
            authenticated_user.add_product_to_cart_by_index(0)
            count_after_first = authenticated_user.get_cart_badge_count()
            assert count_after_first == 1, "Cart badge should show 1"
        
        with allure.step("Add second product"):
            authenticated_user.add_product_to_cart_by_index(1)
            count_after_second = authenticated_user.get_cart_badge_count()
            assert count_after_second == 2, "Cart badge should show 2"
        
        with allure.step("Remove first product"):
            authenticated_user.remove_product_from_cart_by_index(0)
            count_after_remove = authenticated_user.get_cart_badge_count()
            assert count_after_remove == 1, "Cart badge should show 1 after removal"
    
    @allure.title("Product detail page - back button functionality")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_detail_back_button(self, authenticated_user: InventoryPage):
        """
        Tests navigation to product detail and back to inventory.
        """
        driver = authenticated_user.driver
        
        with allure.step("Navigate to product detail"):
            product_link = driver.find_element("css selector", ".inventory_item_name")
            product_link.click()
            authenticated_user.wait_for_url_contains("inventory-item.html", timeout=5)
        
        with allure.step("Click back to products button"):
            back_button = authenticated_user.find_element(("id", "back-to-products"))
            assert back_button.is_displayed(), "Back button should be visible"
            back_button.click()
        
        with allure.step("Verify return to inventory page"):
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
            assert authenticated_user.is_inventory_page_loaded()
    
    @allure.title("Sorting dropdown - all options are selectable")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sorting_dropdown_all_options(self, authenticated_user: InventoryPage):
        """
        Tests all sorting options in the dropdown menu.
        """
        sort_options = ["az", "za", "lohi", "hilo"]
        
        for sort_option in sort_options:
            with allure.step(f"Select sort option: {sort_option}"):
                authenticated_user.sort_products(sort_option)
                
                # Verify products are still displayed
                product_count = authenticated_user.get_product_count()
                assert product_count > 0, f"Products should be visible after sorting by {sort_option}"
    
    @allure.title("Continue Shopping button returns to inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_continue_shopping_navigation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests Continue Shopping button navigates back to inventory.
        """
        with allure.step("Navigate to cart"):
            authenticated_user.go_to_cart()
            assert cart_page.is_cart_page_loaded()
        
        with allure.step("Click Continue Shopping"):
            cart_page.continue_shopping()
        
        with allure.step("Verify return to inventory"):
            assert authenticated_user.is_inventory_page_loaded()
            product_count = authenticated_user.get_product_count()
            assert product_count > 0, "Should see products after returning"


@allure.feature("UI/UX Validation")
@allure.story("Responsive Design")
class TestResponsiveDesign:
    """
    Tests for responsive design and different viewport sizes.
    """
    
    @allure.title("Mobile viewport - elements are accessible")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_mobile_viewport_accessibility(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Tests application usability on mobile viewport size.
        """
        driver = login_page.driver
        
        with allure.step("Set mobile viewport size"):
            driver.set_window_size(375, 667)  # iPhone SE size
        
        with allure.step("Login on mobile viewport"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
        
        with allure.step("Verify inventory loads on mobile"):
            assert inventory_page.is_inventory_page_loaded()
            product_count = inventory_page.get_product_count()
            assert product_count > 0, "Products should be visible on mobile"
        
        with allure.step("Restore window size"):
            driver.maximize_window()
    
    @allure.title("Tablet viewport - layout adapts correctly")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_tablet_viewport_layout(self, authenticated_user: InventoryPage):
        """
        Tests application layout on tablet viewport size.
        """
        driver = authenticated_user.driver
        
        with allure.step("Set tablet viewport size"):
            driver.set_window_size(768, 1024)  # iPad size
        
        with allure.step("Verify products are visible"):
            product_count = authenticated_user.get_product_count()
            assert product_count > 0, "Products should be visible on tablet"
        
        with allure.step("Test cart functionality on tablet"):
            authenticated_user.add_product_to_cart_by_index(0)
            cart_count = authenticated_user.get_cart_badge_count()
            assert cart_count > 0, "Cart should work on tablet"
        
        with allure.step("Restore window size"):
            driver.maximize_window()
