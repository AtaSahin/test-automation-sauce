import pytest
import allure
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Advanced Test Scenarios")
@allure.story("Complex Business Logic")
class TestAdvanced:
    """
    Advanced test suite for complex scenarios and edge cases.
    
    Tests business logic, price calculations, sorting algorithms,
    and multi-step user workflows.
    """
    
    @allure.title("Verify price sorting accuracy with calculations")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_price_sorting_and_calculation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Validates that price sorting works correctly and prices are consistent.
        """
        authenticated_user.sort_products("lohi")
        prices_ascending = authenticated_user.get_all_product_prices()
        
        assert prices_ascending == sorted(prices_ascending), "Low to high sort failed"
        
        authenticated_user.sort_products("hilo")
        prices_descending = authenticated_user.get_all_product_prices()
        product_names_desc = authenticated_user.get_all_product_names()
        
        assert prices_descending == sorted(prices_descending, reverse=True), "High to low sort failed"
        
        authenticated_user.add_product_to_cart_by_name(product_names_desc[0])
        authenticated_user.add_product_to_cart_by_name(product_names_desc[1])
        
        expected_total = prices_descending[0] + prices_descending[1]
        
        authenticated_user.go_to_cart()
        actual_total = cart_page.get_total_price()
        
        assert abs(expected_total - actual_total) < 0.01, f"Price mismatch: {expected_total} vs {actual_total}"
    
    @allure.title("Add all products, remove half, verify cart state")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_complex_cart_manipulation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests adding all products, then selectively removing half.
        """
        total_products = authenticated_user.get_product_count()
        
        added_products = authenticated_user.add_multiple_products_to_cart(total_products)
        assert authenticated_user.get_cart_badge_count() == total_products
        
        authenticated_user.go_to_cart()
        assert cart_page.get_cart_item_count() == total_products
        
        products_to_remove = total_products // 2
        for i in range(products_to_remove):
            cart_page.remove_product_by_index(0)
        
        remaining_count = total_products - products_to_remove
        assert cart_page.get_cart_item_count() == remaining_count
        
        cart_page.continue_shopping()
        assert authenticated_user.get_cart_badge_count() == remaining_count
    
    @allure.title("Sort by name, add first 3, verify alphabetical order in cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_alphabetical_sort_with_cart_verification(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Ensures alphabetical sorting reflects correctly in cart.
        """
        authenticated_user.sort_products("az")
        product_names_sorted = authenticated_user.get_all_product_names()[:3]
        
        for name in product_names_sorted:
            authenticated_user.add_product_to_cart_by_name(name)
        
        authenticated_user.go_to_cart()
        cart_items = cart_page.get_cart_item_names()
        
        assert len(cart_items) == 3
        for product in product_names_sorted:
            assert product in cart_items, f"{product} not found in cart"
    
    @allure.title("Add product, remove it, add different product, verify correct item")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sequential_add_remove_different_products(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests cart state consistency when adding and removing different products.
        """
        product_names = authenticated_user.get_all_product_names()
        first_product = product_names[0]
        second_product = product_names[1]
        
        authenticated_user.add_product_to_cart_by_name(first_product)
        assert authenticated_user.get_cart_badge_count() == 1
        
        authenticated_user.go_to_cart()
        assert cart_page.is_product_in_cart(first_product)
        cart_page.remove_product_by_name(first_product)
        assert cart_page.is_cart_empty()
        
        cart_page.continue_shopping()
        authenticated_user.add_product_to_cart_by_name(second_product)
        
        authenticated_user.go_to_cart()
        assert cart_page.is_product_in_cart(second_product)
        assert not cart_page.is_product_in_cart(first_product)
    
    @allure.title("Compare prices: cheapest vs most expensive product")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    def test_price_comparison_extremes(self, authenticated_user: InventoryPage):
        """
        Validates price range by comparing cheapest and most expensive items.
        """
        authenticated_user.sort_products("lohi")
        prices_asc = authenticated_user.get_all_product_prices()
        cheapest_price = prices_asc[0]
        
        authenticated_user.sort_products("hilo")
        prices_desc = authenticated_user.get_all_product_prices()
        most_expensive_price = prices_desc[0]
        
        assert most_expensive_price > cheapest_price, "Most expensive should be greater than cheapest"
        
        price_difference = most_expensive_price - cheapest_price
        assert price_difference > 0, "Price difference should be positive"
    
    @allure.title("Rapid add/remove operations stress test")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_rapid_cart_operations(self, authenticated_user: InventoryPage):
        """
        Stress tests cart by rapidly adding and removing products.
        """
        product_names = authenticated_user.get_all_product_names()
        
        for i in range(3):
            authenticated_user.add_product_to_cart_by_name(product_names[i])
        assert authenticated_user.get_cart_badge_count() == 3
        
        for i in range(3):
            authenticated_user.remove_product_from_cart_by_name(product_names[i])
        assert authenticated_user.get_cart_badge_count() == 0
        
        for i in range(3):
            authenticated_user.add_product_to_cart_by_name(product_names[i])
        assert authenticated_user.get_cart_badge_count() == 3
    
    @allure.title("Verify all products have valid prices and names")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_all_products_data_integrity(self, authenticated_user: InventoryPage):
        """
        Data integrity test ensuring all products have valid information.
        """
        product_count = authenticated_user.get_product_count()
        
        for i in range(product_count):
            product = authenticated_user.get_product_details(i)
            
            assert product.get("name"), f"Product {i} has no name"
            assert product.get("price"), f"Product {i} has no price"
            assert product.get("description"), f"Product {i} has no description"
            assert "$" in product.get("price"), f"Product {i} price format invalid"
            
            price_value = float(product.get("price").replace("$", ""))
            assert price_value > 0, f"Product {i} has invalid price: {price_value}"


@allure.feature("Edge Cases & Negative Scenarios")
@allure.story("Boundary Testing")
class TestEdgeCases:
    """
    Test suite for edge cases and boundary conditions.
    
    Validates system behavior at limits and unusual scenarios.
    """
    
    @allure.title("Empty cart checkout attempt")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_empty_cart_checkout_disabled(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies that checkout button behaves correctly with empty cart.
        """
        authenticated_user.go_to_cart()
        
        assert cart_page.is_cart_empty(), "Cart should be empty initially"
        assert cart_page.is_cart_page_loaded(), "Cart page should load"
    
    @allure.title("Navigate back and forth between pages")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_page_navigation_consistency(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests navigation stability when moving between pages multiple times.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        
        authenticated_user.go_to_cart()
        assert cart_page.is_cart_page_loaded()
        
        cart_page.continue_shopping()
        assert authenticated_user.is_inventory_page_loaded()
        
        authenticated_user.go_to_cart()
        assert cart_page.is_cart_page_loaded()
        assert cart_page.get_cart_item_count() == 1
    
    @allure.title("Add same product multiple times from different sorts")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_duplicate_add_prevention(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies cart handles duplicate additions correctly.
        """
        product_names = authenticated_user.get_all_product_names()
        first_product = product_names[0]
        
        authenticated_user.add_product_to_cart_by_name(first_product)
        initial_count = authenticated_user.get_cart_badge_count()
        
        authenticated_user.sort_products("za")
        
        product_names_desc = authenticated_user.get_all_product_names()
        if first_product in product_names_desc:
            current_count = authenticated_user.get_cart_badge_count()
            assert current_count == initial_count
    
    @allure.title("Maximum cart capacity test")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_add_all_products_to_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests cart behavior when adding maximum number of different products.
        """
        total_products = authenticated_user.get_product_count()
        added_products = authenticated_user.add_multiple_products_to_cart(total_products)
        
        cart_count = authenticated_user.get_cart_badge_count()
        assert cart_count == total_products, f"Expected {total_products} items, got {cart_count}"
        
        authenticated_user.go_to_cart()
        cart_items_count = cart_page.get_cart_item_count()
        assert cart_items_count == total_products
        
        cart_items = cart_page.get_cart_item_names()
        assert len(cart_items) == len(added_products)

