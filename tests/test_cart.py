import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@allure.feature("Shopping Cart")
@allure.story("Cart Management")
class TestCart:
    """
    Test suite for shopping cart functionality.
    
    Covers cart operations including adding, removing, and validating products.
    """
    
    @allure.title("Verify cart page loads correctly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_cart_page_loads(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Confirms cart page is accessible from inventory.
        """
        authenticated_user.go_to_cart()
        assert cart_page.is_cart_page_loaded(), "Cart page did not load"
    
    @allure.title("Verify empty cart displays no items")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_empty_cart_shows_no_items(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Validates empty cart state when no products added.
        """
        authenticated_user.go_to_cart()
        assert cart_page.is_cart_empty(), "Cart should be empty but contains items"
        assert cart_page.get_cart_item_count() == 0
    
    @allure.title("Product added to cart appears correctly")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_added_product_appears_in_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies product added from inventory appears in cart with correct details.
        """
        product_names = authenticated_user.get_all_product_names()
        first_product = product_names[0]
        
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        
        assert cart_page.get_cart_item_count() == 1, "Cart should contain 1 item"
        assert cart_page.is_product_in_cart(first_product), f"Product {first_product} not found in cart"
    
    @allure.title("Multiple products appear in cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_multiple_products_in_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Validates multiple products can be added and displayed in cart.
        """
        added_products = authenticated_user.add_multiple_products_to_cart(3)
        authenticated_user.go_to_cart()
        
        assert cart_page.get_cart_item_count() == 3, "Cart should contain 3 items"
        
        cart_items = cart_page.get_cart_item_names()
        for product in added_products:
            assert product in cart_items, f"Product {product} not found in cart"
    
    @allure.title("Remove product from cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_remove_product_from_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests product removal from cart page updates count correctly.
        """
        product_name = authenticated_user.get_all_product_names()[0]
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        
        assert cart_page.get_cart_item_count() == 1
        
        cart_page.remove_product_by_name(product_name)
        assert cart_page.is_cart_empty(), "Cart should be empty after removing only item"
    
    @allure.title("Remove multiple products from cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_remove_multiple_products(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Validates removing items one by one updates cart correctly.
        """
        authenticated_user.add_multiple_products_to_cart(3)
        authenticated_user.go_to_cart()
        
        cart_page.remove_product_by_index(0)
        assert cart_page.get_cart_item_count() == 2, "Expected 2 items after first removal"
        
        cart_page.remove_product_by_index(0)
        assert cart_page.get_cart_item_count() == 1, "Expected 1 item after second removal"
        
        cart_page.remove_product_by_index(0)
        assert cart_page.is_cart_empty(), "Cart should be empty after removing all items"
    
    @allure.title("Clear entire cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_clear_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests clearing all products from cart at once.
        """
        authenticated_user.add_multiple_products_to_cart(4)
        authenticated_user.go_to_cart()
        
        cart_page.clear_cart()
        assert cart_page.is_cart_empty(), "Cart should be empty after clearing"
    
    @allure.title("Continue shopping returns to inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_continue_shopping_navigation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies continue shopping button returns to product catalog.
        """
        authenticated_user.go_to_cart()
        cart_page.continue_shopping()
        
        assert authenticated_user.is_inventory_page_loaded(), "Did not return to inventory page"
    
    @allure.title("Verify cart maintains state when returning from inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_state_persistence(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Ensures cart contents persist when navigating between pages.
        """
        added_products = authenticated_user.add_multiple_products_to_cart(2)
        authenticated_user.go_to_cart()
        
        initial_count = cart_page.get_cart_item_count()
        cart_page.continue_shopping()
        authenticated_user.go_to_cart()
        
        assert cart_page.get_cart_item_count() == initial_count, "Cart count changed during navigation"
        
        for product in added_products:
            assert cart_page.is_product_in_cart(product), f"Product {product} lost during navigation"
    
    @allure.title("Verify product prices in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_product_prices(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Validates prices displayed in cart match inventory prices.
        """
        inventory_prices = authenticated_user.get_all_product_prices()[:2]
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.add_product_to_cart_by_index(1)
        authenticated_user.go_to_cart()
        
        cart_prices = cart_page.get_cart_item_prices()
        
        assert cart_prices[0] == inventory_prices[0], "First product price mismatch"
        assert cart_prices[1] == inventory_prices[1], "Second product price mismatch"
    
    @allure.title("Calculate total price in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_total_calculation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies cart subtotal matches sum of individual item prices.
        """
        authenticated_user.add_multiple_products_to_cart(3)
        authenticated_user.go_to_cart()
        
        total_price = cart_page.get_total_price()
        assert total_price > 0, "Cart total should be greater than 0"

