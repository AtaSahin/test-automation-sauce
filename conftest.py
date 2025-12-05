import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import Config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from typing import Generator


@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Remote, None, None]:
    """
    Provides WebDriver instance with automatic cleanup.
    
    Creates browser instance based on config, maximizes window,
    and ensures proper teardown regardless of test outcome.
    
    Yields:
        WebDriver instance for test execution
    """
    driver_instance = None
    
    if Config.BROWSER == "chrome":
        options = webdriver.ChromeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Disable all password-related pop-ups and warnings
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
            "autofill.profile_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        # Suppress automation warnings and info bars
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-save-password-bubble")
        
        driver_instance = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
    
    elif Config.BROWSER == "firefox":
        options = webdriver.FirefoxOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        
        driver_instance = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )
    
    elif Config.BROWSER == "edge":
        options = webdriver.EdgeOptions()
        if Config.HEADLESS:
            options.add_argument("--headless")
        
        driver_instance = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    
    else:
        raise ValueError(f"Unsupported browser: {Config.BROWSER}")
    
    driver_instance.maximize_window()
    driver_instance.implicitly_wait(0)
    
    yield driver_instance
    
    driver_instance.quit()


@pytest.fixture(scope="function")
def login_page(driver: webdriver.Remote) -> LoginPage:
    """
    Provides LoginPage instance for test methods.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        LoginPage object
    """
    return LoginPage(driver)


@pytest.fixture(scope="function")
def inventory_page(driver: webdriver.Remote) -> InventoryPage:
    """
    Provides InventoryPage instance for test methods.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        InventoryPage object
    """
    return InventoryPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver: webdriver.Remote) -> CartPage:
    """
    Provides CartPage instance for test methods.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        CartPage object
    """
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page(driver: webdriver.Remote) -> CheckoutPage:
    """
    Provides CheckoutPage instance for test methods.
    
    Args:
        driver: WebDriver fixture
        
    Returns:
        CheckoutPage object
    """
    return CheckoutPage(driver)


@pytest.fixture(scope="function")
def authenticated_user(login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """
    Provides pre-authenticated session for tests requiring logged-in state.
    
    This fixture handles login setup, allowing tests to focus on their
    actual scenarios rather than repeating authentication steps.
    
    Args:
        login_page: LoginPage fixture
        inventory_page: InventoryPage fixture
        
    Returns:
        InventoryPage object after successful login
    """
    login_page.navigate()
    login_page.login_with_user_type("standard")
    assert inventory_page.wait_for_url_contains("inventory.html", timeout=15), "Login failed - did not navigate to inventory"
    assert inventory_page.is_inventory_page_loaded(), "Login failed - inventory page not loaded"
    return inventory_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook for capturing test results and screenshots on failure.
    
    Automatically attaches screenshots to Allure reports when tests fail,
    providing visual context for debugging without manual intervention.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        if Config.SCREENSHOT_ON_FAILURE:
            driver = None
            
            for fixture_name in item.fixturenames:
                if fixture_name == "driver":
                    driver = item.funcargs.get("driver")
                    break
            
            if driver:
                try:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"failure_{item.name}",
                        attachment_type=allure.attachment_type.PNG
                    )
                except Exception as e:
                    print(f"Failed to capture screenshot: {str(e)}")


def pytest_configure(config):
    """
    Pytest configuration hook for setting up test environment.
    
    Registers custom markers and configures Allure reporting metadata.
    """
    config.addinivalue_line(
        "markers", "smoke: marks tests as smoke tests"
    )
    config.addinivalue_line(
        "markers", "regression: marks tests as regression tests"
    )

