"""
Caching utilities for improved performance.
"""
import functools
import hashlib
import pickle
from pathlib import Path
from app.logger import get_logger
from app.config import BASE_DIR

logger = get_logger(__name__)

CACHE_DIR = BASE_DIR / '.cache'
CACHE_DIR.mkdir(exist_ok=True)


def cache_result(cache_key_func=None):
    """
    Decorator to cache function results to disk.
    
    Args:
        cache_key_func: Optional function to generate cache key from args
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if cache_key_func:
                cache_key = cache_key_func(*args, **kwargs)
            else:
                # Default: hash of function name and arguments
                key_data = f"{func.__name__}:{str(args)}:{str(kwargs)}"
                cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            cache_file = CACHE_DIR / f"{cache_key}.cache"
            
            # Try to load from cache
            if cache_file.exists():
                try:
                    with open(cache_file, 'rb') as f:
                        result = pickle.load(f)
                    logger.debug(f"Cache hit for {func.__name__}")
                    return result
                except Exception as e:
                    logger.warning(f"Cache read error: {str(e)}")
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Save to cache
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(result, f)
                logger.debug(f"Cached result for {func.__name__}")
            except Exception as e:
                logger.warning(f"Cache write error: {str(e)}")
            
            return result
        
        return wrapper
    return decorator


def clear_cache():
    """Clear all cached results."""
    count = 0
    for cache_file in CACHE_DIR.glob('*.cache'):
        cache_file.unlink()
        count += 1
    
    logger.info(f"Cleared {count} cache files")
    return count


class LRUCache:
    """Simple LRU cache implementation."""
    
    def __init__(self, max_size=100):
        self.cache = {}
        self.max_size = max_size
        self.access_order = []
    
    def get(self, key):
        """Get value from cache."""
        if key in self.cache:
            # Move to end (most recently used)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def set(self, key, value):
        """Set value in cache."""
        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used
            lru_key = self.access_order.pop(0)
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.access_order.append(key)
    
    def clear(self):
        """Clear the cache."""
        self.cache.clear()
        self.access_order.clear()
