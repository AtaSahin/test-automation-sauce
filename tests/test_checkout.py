import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from faker import Faker


fake = Faker()


@allure.feature("Checkout Process")
@allure.story("Order Completion")
class TestCheckout:
    """
    Test suite for complete checkout flow.
    
    Validates customer information entry, order review, and purchase completion.
    """
    
    @allure.title("Complete checkout with valid information")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_successful_checkout(self, authenticated_user: InventoryPage, cart_page: CartPage, 
                                 checkout_page: CheckoutPage):
        """
        Verifies end-to-end purchase flow with valid customer data.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one("John", "Doe", "12345")
        
        assert checkout_page.get_subtotal() > 0, "Subtotal should be greater than 0"
        assert checkout_page.get_tax() > 0, "Tax should be greater than 0"
        assert checkout_page.get_total() > 0, "Total should be greater than 0"
        
        checkout_page.finish_checkout()
        
        assert checkout_page.is_checkout_complete(), "Checkout completion page not displayed"
        completion_msg = checkout_page.get_completion_message()
        assert "complete" in completion_msg.lower() or "thank" in completion_msg.lower()
    
    @allure.title("Checkout with empty first name")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_first_name(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                       checkout_page: CheckoutPage):
        """
        Validates form validation for missing first name field.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one("", fake.last_name(), fake.zipcode()[:5])
        
        assert checkout_page.is_error_displayed(), "No error shown for empty first name"
        error_msg = checkout_page.get_error_message()
        assert "first name" in error_msg.lower() or "required" in error_msg.lower()
    
    @allure.title("Checkout with empty last name")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_last_name(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                      checkout_page: CheckoutPage):
        """
        Validates form validation for missing last name field.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one(fake.first_name(), "", fake.zipcode()[:5])
        
        assert checkout_page.is_error_displayed(), "No error shown for empty last name"
        error_msg = checkout_page.get_error_message()
        assert "last name" in error_msg.lower() or "required" in error_msg.lower()
    
    @allure.title("Checkout with empty postal code")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_empty_postal_code(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                        checkout_page: CheckoutPage):
        """
        Validates form validation for missing postal code field.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one(fake.first_name(), fake.last_name(), "")
        
        assert checkout_page.is_error_displayed(), "No error shown for empty postal code"
        error_msg = checkout_page.get_error_message()
        assert "postal" in error_msg.lower() or "zip" in error_msg.lower() or "required" in error_msg.lower()
    
    @allure.title("Checkout with all fields empty")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_checkout_all_fields_empty(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                       checkout_page: CheckoutPage):
        """
        Validates form validation when all fields are blank.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one("", "", "")
        
        assert checkout_page.is_error_displayed(), "No error shown for empty form"
    
    @allure.title("Cancel checkout and return to cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cancel_checkout(self, authenticated_user: InventoryPage, cart_page: CartPage,
                            checkout_page: CheckoutPage):
        """
        Verifies cancel button returns to cart without losing items.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        initial_cart_count = cart_page.get_cart_item_count()
        
        cart_page.proceed_to_checkout()
        checkout_page.cancel_checkout()
        
        assert cart_page.is_cart_page_loaded(), "Did not return to cart page"
        assert cart_page.get_cart_item_count() == initial_cart_count, "Cart items lost during cancel"
    
    @allure.title("Verify price calculations in checkout overview")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_checkout_price_calculations(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                         checkout_page: CheckoutPage):
        """
        Validates subtotal, tax, and total calculations are correct.
        """
        authenticated_user.add_multiple_products_to_cart(2)
        authenticated_user.go_to_cart()
        
        expected_subtotal = cart_page.get_total_price()
        
        cart_page.proceed_to_checkout()
        checkout_page.complete_checkout_step_one(fake.first_name(), fake.last_name(), fake.zipcode()[:5])
        
        subtotal = checkout_page.get_subtotal()
        tax = checkout_page.get_tax()
        total = checkout_page.get_total()
        
        assert abs(subtotal - expected_subtotal) < 0.01, f"Subtotal mismatch: {subtotal} vs {expected_subtotal}"
        assert tax > 0, "Tax should be greater than 0"
        
        calculated_total = round(subtotal + tax, 2)
        assert abs(total - calculated_total) < 0.01, f"Total calculation incorrect: {total} vs {calculated_total}"
    
    @allure.title("Complete checkout with multiple products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_checkout_multiple_products(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                        checkout_page: CheckoutPage):
        """
        Verifies checkout handles multiple products correctly.
        """
        added_products = authenticated_user.add_multiple_products_to_cart(3)
        authenticated_user.go_to_cart()
        
        assert cart_page.get_cart_item_count() == 3
        
        cart_page.proceed_to_checkout()
        checkout_page.complete_checkout_step_one("Jane", "Smith", "54321")
        checkout_page.finish_checkout()
        
        assert checkout_page.is_checkout_complete(), "Checkout failed with multiple products"
    
    @allure.title("Return to products after order completion")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_back_to_home_after_checkout(self, authenticated_user: InventoryPage, cart_page: CartPage,
                                         checkout_page: CheckoutPage):
        """
        Validates return to inventory after successful purchase.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        cart_page.proceed_to_checkout()
        
        checkout_page.complete_checkout_step_one(fake.first_name(), fake.last_name(), fake.zipcode()[:5])
        checkout_page.finish_checkout()
        
        assert checkout_page.is_checkout_complete()
        
        checkout_page.back_to_home()
        assert authenticated_user.is_inventory_page_loaded(), "Did not return to inventory page"

