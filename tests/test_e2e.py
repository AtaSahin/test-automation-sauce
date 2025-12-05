import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from faker import Faker


fake = Faker()


@allure.feature("End to End Scenarios")
@allure.story("Complete User Journeys")
class TestE2E:
    """
    End-to-end test suite simulating complete user workflows.
    
    Tests full shopping experiences from login through purchase completion.
    """
    
    @allure.title("Complete purchase flow - Happy path")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_complete_purchase_flow(self, login_page: LoginPage, inventory_page: InventoryPage,
                                   cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Validates entire shopping journey from login to order completion.
        
        This represents the critical happy path that must always function
        for the business to operate successfully.
        """
        with allure.step("User logs in"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
            inventory_page.wait_for_url_contains("inventory.html", timeout=15)
            assert inventory_page.is_inventory_page_loaded()
        
        with allure.step("User adds products to cart"):
            product_names = inventory_page.add_multiple_products_to_cart(2)
            assert inventory_page.get_cart_badge_count() == 2
        
        with allure.step("User navigates to cart"):
            inventory_page.go_to_cart()
            assert cart_page.is_cart_page_loaded()
            assert cart_page.get_cart_item_count() == 2
        
        with allure.step("User proceeds to checkout"):
            cart_page.proceed_to_checkout()
        
        with allure.step("User fills checkout information"):
            checkout_page.complete_checkout_step_one("Test", "User", "90210")
        
        with allure.step("User completes order"):
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
    
    @allure.title("Browse, add, remove, and checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_shopping_with_cart_modifications(self, login_page: LoginPage, inventory_page: InventoryPage,
                                               cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests user changing mind about products before checkout.
        """
        with allure.step("Login and browse products"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
            assert inventory_page.is_inventory_page_loaded()
        
        with allure.step("Add multiple products"):
            products = inventory_page.add_multiple_products_to_cart(4)
            assert inventory_page.get_cart_badge_count() == 4
        
        with allure.step("Go to cart and remove some items"):
            inventory_page.go_to_cart()
            cart_page.remove_product_by_index(0)
            cart_page.remove_product_by_index(0)
            assert cart_page.get_cart_item_count() == 2
        
        with allure.step("Complete checkout with remaining items"):
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
    
    @allure.title("Sort products and purchase highest priced item")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_and_purchase_expensive_item(self, login_page: LoginPage, inventory_page: InventoryPage,
                                               cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Simulates user looking for premium product via price sorting.
        """
        with allure.step("Login"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
        
        with allure.step("Sort by price high to low"):
            inventory_page.sort_products("hilo")
            prices = inventory_page.get_all_product_prices()
            assert prices[0] >= prices[-1], "Prices not sorted correctly"
        
        with allure.step("Add highest priced item"):
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.go_to_cart()
        
        with allure.step("Complete purchase"):
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
    
    @allure.title("Add all products and purchase")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_purchase_all_products(self, login_page: LoginPage, inventory_page: InventoryPage,
                                   cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests cart functionality with maximum product count.
        """
        with allure.step("Login"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
        
        with allure.step("Add all available products"):
            total_products = inventory_page.get_product_count()
            inventory_page.add_multiple_products_to_cart(total_products)
            assert inventory_page.get_cart_badge_count() == total_products
        
        with allure.step("Verify all products in cart"):
            inventory_page.go_to_cart()
            assert cart_page.get_cart_item_count() == total_products
        
        with allure.step("Complete checkout"):
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
    
    @allure.title("Abandoned cart recovery - Continue shopping flow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_continue_shopping_and_add_more(self, login_page: LoginPage, inventory_page: InventoryPage,
                                            cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Simulates user adding items in multiple sessions before checkout.
        """
        with allure.step("Login and add initial products"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
            inventory_page.add_product_to_cart_by_index(0)
        
        with allure.step("Go to cart and continue shopping"):
            inventory_page.go_to_cart()
            assert cart_page.get_cart_item_count() == 1
            cart_page.continue_shopping()
        
        with allure.step("Add more products"):
            inventory_page.add_product_to_cart_by_index(1)
            inventory_page.add_product_to_cart_by_index(2)
            assert inventory_page.get_cart_badge_count() == 3
        
        with allure.step("Complete checkout"):
            inventory_page.go_to_cart()
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
    
    @allure.title("Checkout and return to inventory for new order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_multiple_purchases_same_session(self, login_page: LoginPage, inventory_page: InventoryPage,
                                             cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests user making second purchase without logging out.
        """
        with allure.step("Complete first purchase"):
            login_page.navigate()
            login_page.login_with_user_type("standard")
            inventory_page.add_product_to_cart_by_index(0)
            inventory_page.go_to_cart()
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()
        
        with allure.step("Return to inventory"):
            checkout_page.back_to_home()
            assert inventory_page.is_inventory_page_loaded()
        
        with allure.step("Make second purchase"):
            inventory_page.add_product_to_cart_by_index(1)
            inventory_page.go_to_cart()
            cart_page.proceed_to_checkout()
            checkout_page.complete_checkout_step_one(
                fake.first_name(),
                fake.last_name(),
                fake.zipcode()[:5]
            )
            checkout_page.finish_checkout()
            assert checkout_page.is_checkout_complete()

