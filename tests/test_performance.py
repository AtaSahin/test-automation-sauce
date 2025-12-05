import pytest
import allure
import time
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Performance & Load")
@allure.story("Response Time Validation")
class TestPerformance:
    """
    Performance test suite validating page load times and responsiveness.
    
    Ensures application meets performance SLAs and responds
    within acceptable timeframes under normal load.
    """
    
    @allure.title("Login performance - should complete under 5 seconds")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_login_performance(self, login_page: LoginPage, inventory_page: InventoryPage):
        """
        Validates login completes within performance threshold.
        """
        login_page.navigate()
        
        start_time = time.time()
        login_page.login_with_user_type("standard")
        inventory_page.wait_for_url_contains("inventory.html", timeout=15)
        end_time = time.time()
        
        login_duration = end_time - start_time
        
        with allure.step(f"Login completed in {login_duration:.2f} seconds"):
            assert login_duration < 5.0, f"Login took {login_duration:.2f}s, expected < 5s"
    
    @allure.title("Page load performance - inventory page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_inventory_load_performance(self, authenticated_user: InventoryPage):
        """
        Measures inventory page load time and product rendering.
        """
        start_time = time.time()
        product_count = authenticated_user.get_product_count()
        end_time = time.time()
        
        load_duration = end_time - start_time
        
        with allure.step(f"Loaded {product_count} products in {load_duration:.2f} seconds"):
            assert product_count > 0, "No products loaded"
            assert load_duration < 3.0, f"Product load took {load_duration:.2f}s, expected < 3s"
    
    @allure.title("Cart operations responsiveness")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_operations_speed(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests cart add/remove operations complete quickly.
        """
        start_time = time.time()
        
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.add_product_to_cart_by_index(1)
        authenticated_user.add_product_to_cart_by_index(2)
        
        end_time = time.time()
        add_duration = end_time - start_time
        
        with allure.step(f"Added 3 products in {add_duration:.2f} seconds"):
            assert add_duration < 5.0, f"Adding products took {add_duration:.2f}s"
        
        authenticated_user.go_to_cart()
        
        start_remove = time.time()
        cart_page.remove_product_by_index(0)
        end_remove = time.time()
        remove_duration = end_remove - start_remove
        
        with allure.step(f"Removed 1 product in {remove_duration:.2f} seconds"):
            assert remove_duration < 2.0, f"Removing product took {remove_duration:.2f}s"
    
    @allure.title("Sorting algorithm performance")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_sorting_performance(self, authenticated_user: InventoryPage):
        """
        Measures sorting operation speed across different sort types.
        """
        sort_options = ["az", "za", "lohi", "hilo"]
        
        for sort_type in sort_options:
            start_time = time.time()
            authenticated_user.sort_products(sort_type)
            authenticated_user.get_all_product_names()
            end_time = time.time()
            
            sort_duration = end_time - start_time
            
            with allure.step(f"Sort '{sort_type}' completed in {sort_duration:.2f} seconds"):
                assert sort_duration < 2.0, f"Sort {sort_type} took {sort_duration:.2f}s"


@allure.feature("Multi-Step Workflows")
@allure.story("Complex User Journeys")
class TestComplexWorkflows:
    """
    Advanced workflow test suite for realistic user scenarios.
    
    Simulates complete shopping sessions with decision changes,
    comparison shopping, and multi-step processes.
    """
    
    @allure.title("Comparison shopping - sort, compare, decide workflow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_comparison_shopping_workflow(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Simulates user comparing products by price before purchasing.
        """
        with allure.step("User sorts by price to find deals"):
            authenticated_user.sort_products("lohi")
            cheapest_products = authenticated_user.get_all_product_names()[:2]
            cheapest_prices = authenticated_user.get_all_product_prices()[:2]
        
        with allure.step("User adds cheapest products to cart"):
            for product in cheapest_products:
                authenticated_user.add_product_to_cart_by_name(product)
        
        with allure.step("User reviews cart"):
            authenticated_user.go_to_cart()
            cart_total = cart_page.get_total_price()
            expected_total = sum(cheapest_prices)
            assert abs(cart_total - expected_total) < 0.01
        
        with allure.step("User decides to check expensive items instead"):
            cart_page.clear_cart()
            cart_page.continue_shopping()
        
        with allure.step("User sorts by price high to low"):
            authenticated_user.sort_products("hilo")
            expensive_product = authenticated_user.get_all_product_names()[0]
            authenticated_user.add_product_to_cart_by_name(expensive_product)
        
        with allure.step("User finalizes with expensive item"):
            authenticated_user.go_to_cart()
            assert cart_page.get_cart_item_count() == 1
            assert cart_page.is_product_in_cart(expensive_product)
    
    @allure.title("Indecisive shopper - multiple cart modifications")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_indecisive_shopper_workflow(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Simulates user changing mind multiple times before checkout.
        """
        product_names = authenticated_user.get_all_product_names()
        
        with allure.step("User adds 3 products"):
            for i in range(3):
                authenticated_user.add_product_to_cart_by_name(product_names[i])
            assert authenticated_user.get_cart_badge_count() == 3
        
        with allure.step("User goes to cart and removes 2 items"):
            authenticated_user.go_to_cart()
            cart_page.remove_product_by_index(0)
            cart_page.remove_product_by_index(0)
            assert cart_page.get_cart_item_count() == 1
        
        with allure.step("User continues shopping and adds 2 more"):
            cart_page.continue_shopping()
            authenticated_user.add_product_to_cart_by_name(product_names[3])
            authenticated_user.add_product_to_cart_by_name(product_names[4])
            assert authenticated_user.get_cart_badge_count() == 3
        
        with allure.step("User reviews final cart"):
            authenticated_user.go_to_cart()
            final_items = cart_page.get_cart_item_names()
            assert len(final_items) == 3
    
    @allure.title("Window shopper - browse all, buy none")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_window_shopper_workflow(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Simulates user browsing without purchasing anything.
        """
        with allure.step("User views all products"):
            product_count = authenticated_user.get_product_count()
            assert product_count == 6
        
        with allure.step("User tries different sorts"):
            authenticated_user.sort_products("az")
            authenticated_user.get_all_product_names()
            
            authenticated_user.sort_products("lohi")
            authenticated_user.get_all_product_prices()
        
        with allure.step("User checks cart without adding anything"):
            authenticated_user.go_to_cart()
            assert cart_page.is_cart_empty()
        
        with allure.step("User returns to shopping"):
            cart_page.continue_shopping()
            assert authenticated_user.is_inventory_page_loaded()
    
    @allure.title("Budget shopper - price conscious workflow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_budget_shopper_workflow(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Simulates user shopping with a budget constraint.
        """
        budget = 50.00
        
        with allure.step("User sorts by price low to high"):
            authenticated_user.sort_products("lohi")
            prices = authenticated_user.get_all_product_prices()
            product_names = authenticated_user.get_all_product_names()
        
        with allure.step("User adds products within budget"):
            current_total = 0
            added_count = 0
            
            for i, price in enumerate(prices):
                if current_total + price <= budget:
                    authenticated_user.add_product_to_cart_by_name(product_names[i])
                    current_total += price
                    added_count += 1
        
        with allure.step("User verifies cart total is within budget"):
            authenticated_user.go_to_cart()
            cart_total = cart_page.get_total_price()
            
            assert cart_total <= budget, f"Cart total ${cart_total} exceeds budget ${budget}"
            assert cart_page.get_cart_item_count() == added_count
    
    @allure.title("Complete shopping session with logout")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_complete_session_workflow(self, authenticated_user: InventoryPage, 
                                       cart_page: CartPage, login_page: LoginPage):
        """
        Full shopping session from browse to logout.
        """
        with allure.step("User browses products"):
            authenticated_user.sort_products("za")
            product_names = authenticated_user.get_all_product_names()
        
        with allure.step("User adds products"):
            authenticated_user.add_product_to_cart_by_name(product_names[0])
            authenticated_user.add_product_to_cart_by_name(product_names[1])
        
        with allure.step("User reviews cart"):
            authenticated_user.go_to_cart()
            assert cart_page.get_cart_item_count() == 2
        
        with allure.step("User decides not to checkout and logs out"):
            cart_page.continue_shopping()
            authenticated_user.logout()
            assert login_page.is_on_login_page()

