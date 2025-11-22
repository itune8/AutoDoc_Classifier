"""
Performance monitoring and profiling utilities.
"""
import time
import functools
from app.logger import get_logger

logger = get_logger(__name__)


def timer(func):
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"{func.__name__} took {duration:.4f} seconds")
        return result
    
    return wrapper


def log_performance(operation_name):
    """Decorator to log performance with custom operation name."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            logger.info(f"{operation_name} completed in {duration:.4f}s")
            return result
        return wrapper
    return decorator


class PerformanceMonitor:
    """Context manager for monitoring performance."""
    
    def __init__(self, operation_name):
        self.operation_name = operation_name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        logger.debug(f"Starting {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        if exc_type:
            logger.error(f"{self.operation_name} failed after {duration:.4f}s")
        else:
            logger.info(f"{self.operation_name} completed in {duration:.4f}s")
    
    @property
    def duration(self):
        """Get duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None
