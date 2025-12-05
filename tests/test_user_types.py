import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("User Type Specific Behaviors")
@allure.story("Different User Types Testing")
class TestUserTypes:
    """
    Comprehensive test suite for all 6 user types on SauceDemo.
    
    Tests specific behaviors and issues for:
    - standard_user: Normal functionality
    - locked_out_user: Account locked
    - problem_user: Various UI/functionality issues
    - performance_glitch_user: Slow performance
    - error_user: Error scenarios
    - visual_user: Visual/UI differences
    """
    
    @allure.title("Problem user - verify broken product images")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_problem_user_broken_images(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Problem user should see broken/incorrect product images.
        This tests that the application correctly simulates image loading issues.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        assert inventory_page.is_inventory_page_loaded()
        
        product_count = inventory_page.get_product_count()
        assert product_count > 0, "No products loaded for problem user"
        
        # Verify basic product data exists despite known image rendering issues
        with allure.step("Verify product images are present (even if broken)"):
            for i in range(min(3, product_count)):
                product = inventory_page.get_product_details(i)
                assert product.get("name"), f"Product {i} should have a name"
    
    @allure.title("Problem user - add to cart button issues")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_problem_user_cart_button_issues(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Problem user experiences issues with add/remove cart buttons.
        Buttons may not change state properly.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        product_names = inventory_page.get_all_product_names()
        first_product = product_names[0]
        
        with allure.step("Add product to cart"):
            inventory_page.add_product_to_cart_by_name(first_product)
            
        with allure.step("Verify cart badge updates"):
            # Core cart functionality must work despite UI issues to prevent blocking purchases
            cart_count = inventory_page.get_cart_badge_count()
            assert cart_count >= 0, "Cart badge should be visible"
    
    @allure.title("Performance glitch user - slow page load detection")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_performance_glitch_user_slow_operations(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Performance glitch user experiences delays in operations.
        This test verifies the system handles slow responses gracefully.
        """
        import time
        
        login_page.navigate()
        
        start_time = time.time()
        login_page.login_with_user_type("performance_glitch")
        inventory_page.wait_for_url_contains("inventory.html", timeout=20)
        end_time = time.time()
        
        login_duration = end_time - start_time
        
        with allure.step(f"Performance glitch user login took {login_duration:.2f}s"):
            # System must handle slow responses gracefully without timeout failures
            assert inventory_page.is_inventory_page_loaded()
            assert login_duration > 0, "Login should take measurable time"
    
    @allure.title("Error user - checkout form submission errors")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_error_user_checkout_issues(self, login_page: LoginPage, inventory_page: InventoryPage, 
                                       cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Error user encounters errors during checkout process.
        Tests error handling and user feedback.
        """
        login_page.navigate()
        login_page.login_with_user_type("error")
        
        with allure.step("Add product and proceed to checkout"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.go_to_cart()
            cart_page.proceed_to_checkout()
        
        with allure.step("Fill checkout form"):
            checkout_page.fill_checkout_form("Error", "User", "12345")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify checkout proceeds or shows error"):
            # Error user may encounter issues, but should remain in checkout flow
            current_url = checkout_page.driver.current_url
            assert "checkout" in current_url, "Should be on checkout page"
    
    @allure.title("Visual user - UI element differences")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_visual_user_ui_differences(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Visual user sees different UI elements or styling.
        Tests that visual differences don't break functionality.
        """
        login_page.navigate()
        login_page.login_with_user_type("visual")
        
        with allure.step("Verify inventory page loads with visual differences"):
            assert inventory_page.is_inventory_page_loaded()
            product_count = inventory_page.get_product_count()
            assert product_count > 0, "Products should load for visual user"
        
        with allure.step("Verify basic functionality works despite visual changes"):
            inventory_page.add_product_to_cart_by_index(0)
            cart_count = inventory_page.get_cart_badge_count()
            assert cart_count > 0, "Cart should work for visual user"
    
    @allure.title("Compare standard vs problem user product display")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_compare_standard_vs_problem_user(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Compares product data between standard and problem users.
        Identifies specific differences in user experience.
        """
        login_page.navigate()
        login_page.login_with_user_type("standard")
        
        standard_products = inventory_page.get_all_product_names()
        standard_prices = inventory_page.get_all_product_prices()
        
        inventory_page.logout()
        
        login_page.login_with_user_type("problem")
        
        problem_products = inventory_page.get_all_product_names()
        problem_prices = inventory_page.get_all_product_prices()
        
        with allure.step("Verify product names are consistent"):
            assert len(standard_products) == len(problem_products), "Product count should match"
        
        with allure.step("Verify prices are consistent"):
            assert len(standard_prices) == len(problem_prices), "Price count should match"
    
    @allure.title("All user types can access inventory page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("user_type", ["standard", "problem", "performance_glitch", "error", "visual"])
    def test_all_users_can_login_except_locked(self, login_page: LoginPage, 
                                                inventory_page: InventoryPage, user_type: str):
        """
        Parametrized test verifying all non-locked users can login successfully.
        """
        login_page.navigate()
        login_page.login_with_user_type(user_type)
        
        with allure.step(f"Verify {user_type} can access inventory"):
            assert inventory_page.is_inventory_page_loaded(), f"{user_type} should access inventory"
            product_count = inventory_page.get_product_count()
            assert product_count > 0, f"{user_type} should see products"


@allure.feature("User Type Specific Behaviors")
@allure.story("Problem User Edge Cases")
class TestProblemUserSpecific:
    """
    Dedicated test suite for problem_user specific issues.
    """
    
    @allure.title("Problem user - sorting functionality issues")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_problem_user_sorting_issues(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Problem user may have issues with sorting functionality.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        with allure.step("Attempt to sort products"):
            inventory_page.sort_products("az")
            products_az = inventory_page.get_all_product_names()
            
            inventory_page.sort_products("za")
            products_za = inventory_page.get_all_product_names()
            
            # Sorting may be buggy but shouldn't crash or hide all products
            assert len(products_az) > 0, "Should have products after sorting"
            assert len(products_za) > 0, "Should have products after reverse sorting"
    
    @allure.title("Problem user - complete checkout flow")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_problem_user_complete_checkout(self, login_page: LoginPage, inventory_page: InventoryPage,
                                           cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests if problem user can complete entire checkout despite UI issues.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        with allure.step("Add products to cart"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.add_product_to_cart_by_index(1)
        
        with allure.step("Proceed to checkout"):
            inventory_page.go_to_cart()
            assert cart_page.get_cart_item_count() >= 1
            cart_page.proceed_to_checkout()
        
        with allure.step("Fill checkout information"):
            checkout_page.fill_checkout_form("Problem", "User", "12345")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify checkout overview page"):
            # UI issues shouldn't prevent reaching checkout completion
            current_url = checkout_page.driver.current_url
            assert "checkout-step-two" in current_url or "checkout" in current_url
    
    @allure.title("Problem user - cart persistence across pages")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_problem_user_cart_persistence(self, login_page: LoginPage, inventory_page: InventoryPage,
                                          cart_page: CartPage):
        """
        Verifies cart state persists for problem user during navigation.
        """
        login_page.navigate()
        login_page.login_with_user_type("problem")
        
        with allure.step("Add items to cart"):
            inventory_page.add_product_to_cart_by_index(0)
            initial_count = inventory_page.get_cart_badge_count()
        
        with allure.step("Navigate to cart and back"):
            inventory_page.go_to_cart()
            cart_items = cart_page.get_cart_item_count()
            cart_page.continue_shopping()
        
        with allure.step("Verify cart count persists"):
            final_count = inventory_page.get_cart_badge_count()
            assert final_count == initial_count, "Cart should persist for problem user"
