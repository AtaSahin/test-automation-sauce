from typing import Dict, List


class TestData:
    """
    Centralized test data repository for consistent test inputs.
    
    Provides predefined datasets for various test scenarios, reducing
    duplication and improving test maintainability.
    """
    
    VALID_USERS = {
        "standard": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "performance_glitch": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        }
    }
    
    INVALID_USERS = {
        "locked_out": {
            "username": "locked_out_user",
            "password": "secret_sauce"
        }
    }
    
    INVALID_CREDENTIALS = [
        {"username": "invalid_user", "password": "wrong_password"},
        {"username": "test@test.com", "password": "12345678"},
        {"username": "admin", "password": "admin"}
    ]
    
    EMPTY_FIELD_SCENARIOS = [
        {"username": "", "password": "secret_sauce", "expected_error": "username"},
        {"username": "standard_user", "password": "", "expected_error": "password"},
        {"username": "", "password": "", "expected_error": "username"}
    ]
    
    CHECKOUT_INFO_VALID = [
        {"first_name": "John", "last_name": "Doe", "postal_code": "12345"},
        {"first_name": "Jane", "last_name": "Smith", "postal_code": "90210"},
        {"first_name": "Test", "last_name": "User", "postal_code": "00000"}
    ]
    
    CHECKOUT_INFO_INVALID = [
        {"first_name": "", "last_name": "Doe", "postal_code": "12345"},
        {"first_name": "John", "last_name": "", "postal_code": "12345"},
        {"first_name": "John", "last_name": "Doe", "postal_code": ""}
    ]
    
    EXPECTED_PRODUCT_COUNT = 6
    
    SORT_OPTIONS = {
        "name_asc": "az",
        "name_desc": "za",
        "price_asc": "lohi",
        "price_desc": "hilo"
    }
    
    @staticmethod
    def get_valid_user(user_type: str = "standard") -> Dict[str, str]:
        """
        Retrieves valid user credentials by type.
        
        Args:
            user_type: Type of user to retrieve
            
        Returns:
            Dictionary with username and password
        """
        return TestData.VALID_USERS.get(user_type, TestData.VALID_USERS["standard"])
    
    @staticmethod
    def get_checkout_info(index: int = 0) -> Dict[str, str]:
        """
        Retrieves valid checkout information by index.
        
        Args:
            index: Index of checkout info to retrieve
            
        Returns:
            Dictionary with first_name, last_name, postal_code
        """
        if 0 <= index < len(TestData.CHECKOUT_INFO_VALID):
            return TestData.CHECKOUT_INFO_VALID[index]
        return TestData.CHECKOUT_INFO_VALID[0]

