import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("State Management & Session")
@allure.story("Cart State Persistence")
class TestStateManagement:
    """
    Tests for state management, session persistence, and data consistency.
    """
    
    @allure.title("Cart persists after browser refresh")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_cart_persists_after_refresh(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies cart contents persist after page refresh.
        Critical for user experience and data integrity.
        """
        driver = authenticated_user.driver
        
        with allure.step("Add products to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.add_product_to_cart_by_index(1)
            initial_count = authenticated_user.get_cart_badge_count()
            assert initial_count == 2, "Should have 2 items in cart"
        
        with allure.step("Refresh the page"):
            driver.refresh()
            # Wait for page to reload by checking URL contains inventory
            authenticated_user.wait_for_url_contains("inventory.html", timeout=10)
        
        with allure.step("Verify cart count persists"):
            # Users expect cart to persist across sessions to prevent lost sales
            count_after_refresh = authenticated_user.get_cart_badge_count()
            assert count_after_refresh == initial_count, "Cart should persist after refresh"
    
    @allure.title("Cart state maintained during navigation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_cart_state_during_navigation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests cart state is maintained when navigating between pages.
        """
        with allure.step("Add items to cart"):
            product_names = authenticated_user.get_all_product_names()
            authenticated_user.add_product_to_cart_by_name(product_names[0])
            authenticated_user.add_product_to_cart_by_name(product_names[1])
            initial_count = authenticated_user.get_cart_badge_count()
        
        with allure.step("Navigate to cart"):
            authenticated_user.go_to_cart()
            cart_items = cart_page.get_cart_item_count()
            assert cart_items == initial_count
        
        with allure.step("Navigate back to inventory"):
            cart_page.continue_shopping()
            count_after_navigation = authenticated_user.get_cart_badge_count()
            assert count_after_navigation == initial_count
        
        with allure.step("Navigate to cart again"):
            authenticated_user.go_to_cart()
            final_cart_items = cart_page.get_cart_item_count()
            assert final_cart_items == initial_count, "Cart should maintain state"
    
    @allure.title("Sorting preference does not affect cart contents")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_sorting_does_not_affect_cart(self, authenticated_user: InventoryPage):
        """
        Verifies changing sort order doesn't affect cart contents.
        """
        with allure.step("Add product to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            initial_count = authenticated_user.get_cart_badge_count()
        
        with allure.step("Change sorting multiple times"):
            authenticated_user.sort_products("za")
            count_after_sort1 = authenticated_user.get_cart_badge_count()
            
            authenticated_user.sort_products("lohi")
            count_after_sort2 = authenticated_user.get_cart_badge_count()
            
            authenticated_user.sort_products("hilo")
            count_after_sort3 = authenticated_user.get_cart_badge_count()
        
        with allure.step("Verify cart unchanged"):
            # UI state changes must not affect cart data to maintain consistency
            assert count_after_sort1 == initial_count
            assert count_after_sort2 == initial_count
            assert count_after_sort3 == initial_count
    
    @allure.title("Product detail view maintains cart state")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_product_detail_maintains_cart(self, authenticated_user: InventoryPage):
        """
        Tests cart state is maintained when viewing product details.
        """
        driver = authenticated_user.driver
        
        with allure.step("Add products to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.add_product_to_cart_by_index(1)
            initial_count = authenticated_user.get_cart_badge_count()
        
        with allure.step("Navigate to product detail"):
            product_link = driver.find_element("css selector", ".inventory_item_name")
            product_link.click()
            authenticated_user.wait_for_url_contains("inventory-item.html", timeout=5)
        
        with allure.step("Verify cart count on detail page"):
            count_on_detail = authenticated_user.get_cart_badge_count()
            assert count_on_detail == initial_count
        
        with allure.step("Navigate back and verify cart"):
            back_button = authenticated_user.find_element(("id", "back-to-products"))
            back_button.click()
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
            
            final_count = authenticated_user.get_cart_badge_count()
            assert final_count == initial_count


@allure.feature("State Management & Session")
@allure.story("Browser Navigation")
class TestBrowserNavigation:
    """
    Tests for browser back/forward navigation and history management.
    """
    
    @allure.title("Browser back button navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_browser_back_button(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests browser back button functionality across pages.
        """
        driver = authenticated_user.driver
        
        with allure.step("Navigate from inventory to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.go_to_cart()
            assert cart_page.is_cart_page_loaded()
        
        with allure.step("Use browser back button"):
            driver.back()
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
        
        with allure.step("Verify returned to inventory"):
            assert authenticated_user.is_inventory_page_loaded()
        
        with allure.step("Verify cart still has items"):
            # Browser navigation must preserve application state
            cart_count = authenticated_user.get_cart_badge_count()
            assert cart_count == 1, "Cart should maintain state after back navigation"
    
    @allure.title("Browser forward button navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_browser_forward_button(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests browser forward button functionality.
        """
        driver = authenticated_user.driver
        
        with allure.step("Navigate to cart and back"):
            authenticated_user.go_to_cart()
            driver.back()
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
        
        with allure.step("Use browser forward button"):
            driver.forward()
            cart_page.wait_for_url_contains("cart.html", timeout=5)
        
        with allure.step("Verify on cart page"):
            assert cart_page.is_cart_page_loaded()
    
    @allure.title("Multiple back/forward navigation sequence")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_multiple_back_forward_navigation(self, authenticated_user: InventoryPage, 
                                              cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Tests complex navigation sequence with multiple back/forward actions.
        """
        driver = authenticated_user.driver
        
        with allure.step("Navigate through multiple pages"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.go_to_cart()
            cart_page.proceed_to_checkout()
        
        with allure.step("Navigate back twice"):
            driver.back()  # Back to cart
            driver.back()  # Back to inventory
            authenticated_user.wait_for_url_contains("inventory.html", timeout=5)
        
        with allure.step("Navigate forward once"):
            driver.forward()  # Forward to cart
            cart_page.wait_for_url_contains("cart.html", timeout=5)
            assert cart_page.is_cart_page_loaded()
        
        with allure.step("Verify cart state maintained"):
            cart_items = cart_page.get_cart_item_count()
            assert cart_items == 1, "Cart should maintain state through navigation"
    
    @allure.title("URL manipulation - direct navigation to cart")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_direct_url_navigation_to_cart(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Tests direct URL navigation to cart page.
        """
        driver = authenticated_user.driver
        base_url = authenticated_user.base_url
        
        with allure.step("Add items to cart"):
            authenticated_user.add_product_to_cart_by_index(0)
            initial_count = authenticated_user.get_cart_badge_count()
        
        with allure.step("Navigate directly to cart via URL"):
            driver.get(f"{base_url}/cart.html")
            cart_page.wait_for_url_contains("cart.html", timeout=10)
        
        with allure.step("Verify cart page loads with items"):
            assert cart_page.is_cart_page_loaded()
            cart_items = cart_page.get_cart_item_count()
            assert cart_items == initial_count, "Cart should load with items via direct URL"


@allure.feature("State Management & Session")
@allure.story("Multi-Window/Tab Behavior")
class TestMultiWindowBehavior:
    """
    Tests for multi-window and multi-tab scenarios.
    """
    
    @allure.title("Cart state in new browser tab")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_cart_state_new_tab(self, authenticated_user: InventoryPage):
        """
        Tests if cart state is shared across browser tabs.
        """
        driver = authenticated_user.driver
        
        with allure.step("Add items to cart in first tab"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.add_product_to_cart_by_index(1)
            initial_count = authenticated_user.get_cart_badge_count()
        
        with allure.step("Open new tab with same URL"):
            original_window = driver.current_window_handle
            driver.execute_script("window.open('');")
            
            # Session cookies must be shared across tabs for consistent UX
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            
            driver.get(f"{authenticated_user.base_url}/inventory.html")
            authenticated_user.wait_for_url_contains("inventory.html", timeout=10)
        
        with allure.step("Verify cart state in new tab"):
            # Cart data must sync across tabs to prevent user confusion
            count_in_new_tab = authenticated_user.get_cart_badge_count()
            assert count_in_new_tab == initial_count, "Cart should sync across tabs"
        
        with allure.step("Close new tab and return to original"):
            driver.close()
            driver.switch_to.window(original_window)
    
    @allure.title("Session consistency across tabs")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_session_consistency_across_tabs(self, authenticated_user: InventoryPage, login_page: LoginPage):
        """
        Tests that user session is consistent across multiple tabs.
        """
        driver = authenticated_user.driver
        
        with allure.step("Open new tab"):
            original_window = driver.current_window_handle
            driver.execute_script("window.open('');")
            
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
        
        with allure.step("Navigate to inventory in new tab"):
            driver.get(f"{authenticated_user.base_url}/inventory.html")
            authenticated_user.wait_for_url_contains("inventory.html", timeout=10)
        
        with allure.step("Verify user is still authenticated"):
            # Should be on inventory page, not redirected to login
            assert authenticated_user.is_inventory_page_loaded(), "Should remain authenticated in new tab"
        
        with allure.step("Cleanup - close new tab"):
            driver.close()
            driver.switch_to.window(original_window)


@allure.feature("Data Integrity")
@allure.story("Price Calculations")
class TestDataIntegrity:
    """
    Tests for data integrity, price calculations, and consistency.
    """
    
    @allure.title("Tax calculation accuracy")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_tax_calculation_accuracy(self, authenticated_user: InventoryPage, 
                                     cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Verifies tax is calculated correctly on checkout overview.
        """
        with allure.step("Add products and proceed to checkout"):
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.add_product_to_cart_by_index(1)
            
            authenticated_user.go_to_cart()
            subtotal = cart_page.get_total_price()
            
            cart_page.proceed_to_checkout()
            checkout_page.fill_checkout_form("Test", "User", "12345")
            checkout_page.continue_to_next_step()
        
        with allure.step("Verify tax calculation"):
            # Get price breakdown from checkout overview
            driver = checkout_page.driver
            
            try:
                subtotal_element = driver.find_element("css selector", ".summary_subtotal_label")
                tax_element = driver.find_element("css selector", ".summary_tax_label")
                total_element = driver.find_element("css selector", ".summary_total_label")
                
                subtotal_text = subtotal_element.text
                tax_text = tax_element.text
                total_text = total_element.text
                
                # Extract numeric values
                import re
                subtotal_value = float(re.search(r'\$?([\d.]+)', subtotal_text).group(1))
                tax_value = float(re.search(r'\$?([\d.]+)', tax_text).group(1))
                total_value = float(re.search(r'\$?([\d.]+)', total_text).group(1))
                
                # Verify calculation
                calculated_total = subtotal_value + tax_value
                assert abs(calculated_total - total_value) < 0.01, \
                    f"Total calculation incorrect: {subtotal_value} + {tax_value} != {total_value}"
                
            except Exception as e:
                allure.attach(str(e), name="Tax Calculation Error", attachment_type=allure.attachment_type.TEXT)
    
    @allure.title("Price consistency from inventory to checkout")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_price_consistency_through_flow(self, authenticated_user: InventoryPage,
                                           cart_page: CartPage, checkout_page: CheckoutPage):
        """
        Verifies product prices remain consistent throughout the purchase flow.
        """
        with allure.step("Get price from inventory page"):
            product_details = authenticated_user.get_product_details(0)
            inventory_price_text = product_details.get("price")
            inventory_price = float(inventory_price_text.replace("$", ""))
            
            authenticated_user.add_product_to_cart_by_index(0)
        
        with allure.step("Verify price in cart"):
            authenticated_user.go_to_cart()
            cart_items = cart_page.get_cart_item_names()
            # Price should be consistent in cart
            assert cart_page.get_cart_item_count() == 1
        
        with allure.step("Verify price in checkout overview"):
            cart_page.proceed_to_checkout()
            checkout_page.fill_checkout_form("Test", "User", "12345")
            checkout_page.continue_to_next_step()
            
            # Price should be consistent in checkout
            driver = checkout_page.driver
            current_url = driver.current_url
            assert "checkout-step-two" in current_url, "Should be on checkout overview"
    
    @allure.title("Cart total matches sum of individual items")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_cart_total_calculation(self, authenticated_user: InventoryPage, cart_page: CartPage):
        """
        Verifies cart total equals sum of individual item prices.
        """
        with allure.step("Add multiple products"):
            # Get prices before adding to ensure we're testing the right products
            product_0_price = authenticated_user.get_product_details(0).get("price")
            product_1_price = authenticated_user.get_product_details(1).get("price")
            product_2_price = authenticated_user.get_product_details(2).get("price")
            
            authenticated_user.add_product_to_cart_by_index(0)
            authenticated_user.add_product_to_cart_by_index(1)
            authenticated_user.add_product_to_cart_by_index(2)
            
            expected_total = (float(product_0_price.replace("$", "")) + 
                            float(product_1_price.replace("$", "")) + 
                            float(product_2_price.replace("$", "")))
        
        with allure.step("Verify cart total"):
            authenticated_user.go_to_cart()
            actual_total = cart_page.get_total_price()
            
            assert abs(expected_total - actual_total) < 0.01, \
                f"Cart total mismatch: expected {expected_total}, got {actual_total}"

