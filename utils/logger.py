import logging
import os
from datetime import datetime


class TestLogger:
    """
    Custom logger for test execution tracking.
    
    Provides structured logging with file and console output,
    helping with debugging and test analysis.
    """
    
    @staticmethod
    def setup_logger(name: str = "test_automation", level: int = logging.INFO) -> logging.Logger:
        """
        Creates and configures logger instance with file and console handlers.
        
        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if logger.handlers:
            return logger
        
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_run_{timestamp}.log")
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(file_formatter)
        
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger


logger = TestLogger.setup_logger()

