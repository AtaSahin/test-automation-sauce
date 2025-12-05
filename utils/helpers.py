import os
from datetime import datetime
from typing import Any
import json


class Helpers:
    """
    Utility functions for common test operations.
    
    Provides reusable helper methods for file operations,
    data manipulation, and test utilities.
    """
    
    @staticmethod
    def create_directory(directory_path: str) -> None:
        """
        Creates directory if it doesn't exist.
        
        Args:
            directory_path: Path to directory
        """
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
    
    @staticmethod
    def get_timestamp(format_string: str = "%Y%m%d_%H%M%S") -> str:
        """
        Generates timestamp string for file naming.
        
        Args:
            format_string: Desired timestamp format
            
        Returns:
            Formatted timestamp string
        """
        return datetime.now().strftime(format_string)
    
    @staticmethod
    def save_json(data: Any, file_path: str) -> None:
        """
        Saves data to JSON file.
        
        Args:
            data: Data to serialize
            file_path: Output file path
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def load_json(file_path: str) -> Any:
        """
        Loads data from JSON file.
        
        Args:
            file_path: Input file path
            
        Returns:
            Deserialized data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
        """
        Polls condition function until it returns True or timeout.
        
        Args:
            condition_func: Function returning boolean
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds
            
        Returns:
            True if condition met, False if timeout
        """
        import time
        elapsed = 0
        
        while elapsed < timeout:
            if condition_func():
                return True
            time.sleep(interval)
            elapsed += interval
        
        return False
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Removes invalid characters from filename.
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename safe for file system
        """
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        return filename
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 100) -> str:
        """
        Truncates text to maximum length with ellipsis.
        
        Args:
            text: Original text
            max_length: Maximum allowed length
            
        Returns:
            Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - 3] + "..."

