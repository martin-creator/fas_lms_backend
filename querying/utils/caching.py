# utils/caching.py
from django.core.cache import cache
from django_redis import get_redis_connection
from .logging import Logger
import logging

# Initialize your custom logger
logger = Logger()

class CacheManager:
    """
    CacheManager class for handling caching operations in the LMS project.
    """

    @staticmethod
    def cache_key_prefix(entity_name, entity_id):
        """
        Generate a cache key prefix based on entity name and ID.
        """
        return f"{entity_name}_{entity_id}_"

    @staticmethod
    def get_cache_key(entity_name, entity_id):
        """
        Generate a specific cache key for an entity.
        """
        return CacheManager.cache_key_prefix(entity_name, entity_id)

    @staticmethod
    def set_cache(key, value, timeout=None):
        """
        Set a value in the cache with an optional timeout.
        """
        try:
            cache.set(key, value, timeout)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Set Cache", error_message=f"Failed to set cache for key '{key}': {e}")
            raise

    @staticmethod
    def get_cache(key):
        """
        Retrieve a value from the cache.
        """
        try:
            return cache.get(key)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Get Cache", error_message=f"Failed to retrieve cache for key '{key}': {e}")
            return None

    @staticmethod
    def delete_cache(key):
        """
        Delete a value from the cache.
        """
        try:
            cache.delete(key)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Delete Cache", error_message=f"Failed to delete cache for key '{key}': {e}")
            raise

    @staticmethod
    def clear_all_cache():
        """
        Clear all cached data.
        """
        try:
            cache.clear()
        except Exception as e:
            logger.handle_query_execution_error(query_name="Clear All Cache", error_message=f"Failed to clear cache: {e}")
            raise

    @staticmethod
    def cache_exists(key):
        """
        Check if a cache entry exists.
        """
        try:
            return cache.get(key) is not None
        except Exception as e:
            logger.handle_query_execution_error(query_name="Check Cache Exists", error_message=f"Failed to check cache existence for key '{key}': {e}")
            return False

    @staticmethod
    def get_cache_stats():
        """
        Get cache statistics (if supported by the cache backend).
        """
        try:
            # This may vary depending on the cache backend being used
            # Example for Redis cache:
            if hasattr(cache, 'cache'):
                return cache.cache.info()
            else:
                logger.logger.warning("Cache backend does not support statistics retrieval")
                return {}
        except Exception as e:
            logger.handle_query_execution_error(query_name="Get Cache Stats", error_message=f"Failed to retrieve cache statistics: {e}")
            return {}

    @staticmethod
    def invalidate_cache_by_prefix(prefix):
        """
        Invalidate cache entries by prefix.
        """
        try:
            # This implementation depends on the cache backend
            # For example, using Redis:
            if hasattr(cache, 'delete_pattern'):
                cache.delete_pattern(f"{prefix}*")
            else:
                logger.logger.warning("Cache backend does not support delete_pattern")
        except Exception as e:
            logger.handle_query_execution_error(query_name="Invalidate Cache By Prefix", error_message=f"Failed to invalidate cache by prefix '{prefix}': {e}")
            raise

    @staticmethod
    def lock_cache(key, timeout=60):
        """
        Lock a cache key to prevent race conditions.
        """
        try:
            # This implementation depends on the cache backend
            # For example, using Redis:
            if hasattr(cache, 'lock'):
                return cache.lock(key, timeout=timeout)
            else:
                logger.logger.warning("Cache backend does not support locking")
                return None
        except Exception as e:
            logger.handle_query_execution_error(query_name="Lock Cache", error_message=f"Failed to lock cache key '{key}': {e}")
            raise

def execute_cached_query(query_key, query_function, timeout=3600, retry_on_failure=3):
    """
    Execute a cached query or fetch from cache if available.

    Args:
    - query_key: Key to identify the cached query result.
    - query_function: Function that executes the query if not found in cache.
    - timeout: Timeout duration in seconds for caching (default is 1 hour).
    - retry_on_failure: Number of retries on failure (default is 3).

    Returns:
    - Cached query result or result from query_function execution.

    Notes:
    - Uses Django's caching framework (defaulting to cache backend set in Django settings).
    - Logs any error encountered during query execution.
    """
    for attempt in range(retry_on_failure):
        try:
            cached_result = cache.get(query_key)
            if cached_result is None:
                result = query_function()
                cache.set(query_key, result, timeout=timeout)
                return result
            return cached_result

        except Exception as e:
            # Handle and log cache execution errors
            logger.handle_query_execution_error(query_name="Cached Query Execution", error_message=f"Error executing cached query for key '{query_key}': {e}")
            if attempt < retry_on_failure - 1:
                logger.logger.warning(f"Retrying cached query execution for key '{query_key}' (attempt {attempt + 1}/{retry_on_failure})")
            else:
                raise e  # Re-raise the exception for the caller to handle

class RedisCacheManager:
    """
    RedisCacheManager class for handling caching operations using Redis.
    """

    def __init__(self):
        self.redis_conn = get_redis_connection("default")

    @staticmethod
    def cache_key_prefix(entity_name, entity_id):
        """
        Generate a cache key prefix based on entity name and ID.
        """
        return f"{entity_name}_{entity_id}_"

    def get_cache_key(self, entity_name, entity_id):
        """
        Generate a specific cache key for an entity.
        """
        return self.cache_key_prefix(entity_name, entity_id)

    def set_cache(self, key, value, timeout=None):
        """
        Set a value in the cache with an optional timeout.
        """
        try:
            cache.set(key, value, timeout)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Set Cache", error_message=f"Failed to set cache for key '{key}': {e}")
            raise

    def get_cache(self, key):
        """
        Retrieve a value from the cache.
        """
        try:
            return cache.get(key)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Get Cache", error_message=f"Failed to retrieve cache for key '{key}': {e}")
            return None

    def delete_cache(self, key):
        """
        Delete a value from the cache.
        """
        try:
            cache.delete(key)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Delete Cache", error_message=f"Failed to delete cache for key '{key}': {e}")
            raise

    def clear_all_cache(self):
        """
        Clear all cached data.
        """
        try:
            cache.clear()
        except Exception as e:
            logger.handle_query_execution_error(query_name="Clear All Cache", error_message=f"Failed to clear cache: {e}")
            raise

    def cache_exists(self, key):
        """
        Check if a cache entry exists.
        """
        try:
            return cache.get(key) is not None
        except Exception as e:
            logger.handle_query_execution_error(query_name="Check Cache Exists", error_message=f"Failed to check cache existence for key '{key}': {e}")
            return False

    def get_cache_stats(self):
        """
        Get cache statistics (if supported by the cache backend).
        """
        try:
            return self.redis_conn.info()
        except Exception as e:
            logger.handle_query_execution_error(query_name="Get Cache Stats", error_message=f"Failed to retrieve cache statistics: {e}")
            return {}

    def invalidate_cache_by_prefix(self, prefix):
        """
        Invalidate cache entries by prefix.
        """
        try:
            keys = self.redis_conn.keys(f"{prefix}*")
            if keys:
                self.redis_conn.delete(*keys)
        except Exception as e:
            logger.handle_query_execution_error(query_name="Invalidate Cache By Prefix", error_message=f"Failed to invalidate cache by prefix '{prefix}': {e}")
            raise

    def lock_cache(self, key, timeout=60):
        """
        Lock a cache key to prevent race conditions.
        """
        try:
            lock = self.redis_conn.lock(key, timeout=timeout)
            if lock.acquire(blocking=False):
                return lock
            return None
        except Exception as e:
            logger.handle_query_execution_error(query_name="Lock Cache", error_message=f"Failed to lock cache key '{key}': {e}")
            raise

def execute_redis_cached_query(query_key, query_function, timeout=3600, retry_on_failure=3):
    # Same as previously defined execute_redis_cached_query...
    pass

    
def notify_admins(message):
    """
    Notify administrators of critical cache errors.

    Args:
    - message: Message to send to administrators.

    Returns:
    - None
    """
    # Implement your notification logic here, e.g., send an email or a message to a monitoring system
    pass
