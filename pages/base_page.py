from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import Config
import allure


class BasePage:
    """
    Base class for all page objects implementing common web interactions.
    
    This class provides reusable methods for element interactions with built-in
    explicit waits, avoiding fragile time.sleep() calls. All page objects should
    inherit from this class to maintain consistency.
    """
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.TIMEOUT)
        self.config = Config
        self.base_url = Config.BASE_URL  # Add base_url property
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Alias for find_element - waits for element to be visible and returns it"""
        wait = WebDriverWait(self.driver, timeout or Config.TIMEOUT)
        return wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not visible within {timeout or Config.TIMEOUT} seconds"
        )
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Finds and returns a visible element using explicit wait.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            WebElement instance if found
            
        Raises:
            TimeoutException: If element is not visible within timeout period
        """
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element {locator} not visible within {Config.TIMEOUT} seconds"
        )
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """
        Finds and returns all matching elements.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            List of WebElement instances
        """
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Elements {locator} not found within {Config.TIMEOUT} seconds"
        )
    
    def click(self, locator: Tuple[str, str], scroll_first: bool = False) -> None:
        """
        Waits for element to be clickable and performs click action.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            scroll_first: Whether to scroll element into view before clicking
        """
        element = self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element {locator} not clickable within {Config.TIMEOUT} seconds"
        )
        if scroll_first:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
    
    def send_keys(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Enters text into input field with optional clearing.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            text: Text to input
            clear_first: Whether to clear existing text before typing
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Retrieves visible text from element.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            Text content of the element
        """
        return self.find_element(locator).text
    
    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Retrieves specified attribute value from element.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            attribute: Name of attribute to retrieve
            
        Returns:
            Attribute value as string
        """
        return self.find_element(locator).get_attribute(attribute)
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Checks if element is visible without throwing exception.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Custom timeout, defaults to Config.TIMEOUT
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout or Config.TIMEOUT)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Checks if element exists in DOM regardless of visibility.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            
        Returns:
            True if element exists in DOM, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_url_contains(self, url_fragment: str, timeout: int = None) -> bool:
        """
        Waits until current URL contains specified text.
        
        Useful for verifying navigation and page transitions without
        relying on fragile element checks.
        
        Args:
            url_fragment: Text that should appear in URL
            timeout: Custom timeout, defaults to Config.TIMEOUT
            
        Returns:
            True if URL contains fragment within timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout or Config.TIMEOUT)
            wait.until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Waits for element to become invisible or removed from DOM.
        
        Args:
            locator: Tuple of (By.TYPE, "locator_value")
            timeout: Custom timeout, defaults to Config.TIMEOUT
            
        Returns:
            True if element disappeared within timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout or Config.TIMEOUT)
            wait.until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def get_current_url(self) -> str:
        """
        Returns current page URL.
        
        Returns:
            Current URL as string
        """
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """
        Returns current page title.
        
        Returns:
            Page title as string
        """
        return self.driver.title
    
    @allure.step("Taking screenshot: {name}")
    def take_screenshot(self, name: str) -> None:
        """
        Captures and attaches screenshot to test report.
        
        Args:
            name: Descriptive name for screenshot
        """
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

