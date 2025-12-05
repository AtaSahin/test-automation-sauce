import pytest
import allure
from pages.inventory_page import InventoryPage


@allure.feature("Product Management")
@allure.story("Inventory Operations")
class TestInventory:
    """
    Test suite for inventory page functionality.
    
    Validates product display, sorting, filtering, and cart operations.
    """
    
    @allure.title("Verify inventory page displays all products")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_inventory_page_loads_with_products(self, authenticated_user: InventoryPage):
        """
        Confirms product catalog loads with expected item count.
        """
        assert authenticated_user.is_inventory_page_loaded(), "Inventory page not loaded properly"
        product_count = authenticated_user.get_product_count()
        assert product_count == 6, f"Expected 6 products, found {product_count}"
    
    @allure.title("Add single product to cart")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_add_single_product_to_cart(self, authenticated_user: InventoryPage):
        """
        Validates adding individual product updates cart badge.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        cart_count = authenticated_user.get_cart_badge_count()
        assert cart_count == 1, f"Expected cart count 1, got {cart_count}"
    
    @allure.title("Add multiple products to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_add_multiple_products_to_cart(self, authenticated_user: InventoryPage):
        """
        Verifies multiple products can be added sequentially.
        """
        added_products = authenticated_user.add_multiple_products_to_cart(3)
        cart_count = authenticated_user.get_cart_badge_count()
        
        assert len(added_products) == 3, "Failed to add 3 products"
        assert cart_count == 3, f"Expected cart count 3, got {cart_count}"
    
    @allure.title("Remove product from cart on inventory page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_remove_product_from_cart(self, authenticated_user: InventoryPage):
        """
        Tests product removal updates cart count correctly.
        """
        product_name = authenticated_user.get_all_product_names()[0]
        authenticated_user.add_product_to_cart_by_index(0)
        
        assert authenticated_user.get_cart_badge_count() == 1
        
        authenticated_user.remove_product_from_cart_by_name(product_name)
        cart_count = authenticated_user.get_cart_badge_count()
        assert cart_count == 0, f"Expected cart count 0 after removal, got {cart_count}"
    
    @allure.title("Sort products by name A to Z")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_name_a_to_z(self, authenticated_user: InventoryPage):
        """
        Validates alphabetical ascending sort functionality.
        """
        authenticated_user.sort_products("az")
        product_names = authenticated_user.get_all_product_names()
        
        sorted_names = sorted(product_names)
        assert product_names == sorted_names, "Products not sorted A to Z correctly"
    
    @allure.title("Sort products by name Z to A")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_name_z_to_a(self, authenticated_user: InventoryPage):
        """
        Validates alphabetical descending sort functionality.
        """
        authenticated_user.sort_products("za")
        product_names = authenticated_user.get_all_product_names()
        
        sorted_names = sorted(product_names, reverse=True)
        assert product_names == sorted_names, "Products not sorted Z to A correctly"
    
    @allure.title("Sort products by price low to high")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_low_to_high(self, authenticated_user: InventoryPage):
        """
        Validates price ascending sort functionality.
        """
        authenticated_user.sort_products("lohi")
        product_prices = authenticated_user.get_all_product_prices()
        
        sorted_prices = sorted(product_prices)
        assert product_prices == sorted_prices, "Products not sorted by price low to high"
    
    @allure.title("Sort products by price high to low")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sort_products_price_high_to_low(self, authenticated_user: InventoryPage):
        """
        Validates price descending sort functionality.
        """
        authenticated_user.sort_products("hilo")
        product_prices = authenticated_user.get_all_product_prices()
        
        sorted_prices = sorted(product_prices, reverse=True)
        assert product_prices == sorted_prices, "Products not sorted by price high to low"
    
    @allure.title("Verify product details are displayed")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_details_displayed(self, authenticated_user: InventoryPage):
        """
        Ensures all product information is visible and complete.
        """
        product = authenticated_user.get_product_details(0)
        
        assert product.get("name"), "Product name not displayed"
        assert product.get("price"), "Product price not displayed"
        assert product.get("description"), "Product description not displayed"
        assert "$" in product.get("price"), "Price format incorrect"
    
    @allure.title("Navigate to cart from inventory page")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_navigate_to_cart(self, authenticated_user: InventoryPage, cart_page):
        """
        Validates cart navigation maintains product selection.
        """
        authenticated_user.add_product_to_cart_by_index(0)
        authenticated_user.go_to_cart()
        
        assert cart_page.is_cart_page_loaded(), "Failed to navigate to cart page"
        assert cart_page.get_cart_item_count() == 1, "Product not retained in cart after navigation"
    
    @allure.title("Logout from inventory page")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_logout_from_inventory(self, authenticated_user: InventoryPage, login_page):
        """
        Verifies logout returns user to login page and clears session.
        """
        authenticated_user.logout()
        
        assert login_page.is_on_login_page(), "Did not return to login page after logout"

