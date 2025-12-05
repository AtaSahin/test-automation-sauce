import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration management for test environment.
    
    Loads settings from environment variables to avoid hardcoding
    sensitive data or environment-specific values.
    """
    
    BASE_URL: str = os.getenv("BASE_URL", "https://www.saucedemo.com")
    BROWSER: str = os.getenv("BROWSER", "chrome").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    
    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_OUT_USER: str = os.getenv("LOCKED_OUT_USER", "locked_out_user")
    PROBLEM_USER: str = os.getenv("PROBLEM_USER", "problem_user")
    PERFORMANCE_GLITCH_USER: str = os.getenv("PERFORMANCE_GLITCH_USER", "performance_glitch_user")
    PASSWORD: str = os.getenv("PASSWORD", "secret_sauce")
    
    @classmethod
    def get_user_credentials(cls, user_type: str = "standard") -> Dict[str, str]:
        """
        Returns username and password for specified user type.
        
        Args:
            user_type: Type of user (standard, locked_out, problem, performance_glitch)
            
        Returns:
            Dictionary containing username and password
        """
        user_map = {
            "standard": cls.STANDARD_USER,
            "locked_out": cls.LOCKED_OUT_USER,
            "problem": cls.PROBLEM_USER,
            "performance_glitch": cls.PERFORMANCE_GLITCH_USER
        }
        
        return {
            "username": user_map.get(user_type, cls.STANDARD_USER),
            "password": cls.PASSWORD
        }

