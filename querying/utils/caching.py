# utils/caching.py
from django.core.cache import cache
from .logging import handle_query_execution_error
import logging

logger = logging.getLogger(__name__)

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
            logger.error(f"Failed to set cache for key '{key}': {e}")
            # Handle cache set failure gracefully based on your application's requirements
            raise

    @staticmethod
    def get_cache(key):
        """
        Retrieve a value from the cache.
        """
        try:
            return cache.get(key)
        except Exception as e:
            logger.error(f"Failed to retrieve cache for key '{key}': {e}")
            return None  # Return None or handle cache get failure as needed

    @staticmethod
    def delete_cache(key):
        """
        Delete a value from the cache.
        """
        try:
            cache.delete(key)
        except Exception as e:
            logger.error(f"Failed to delete cache for key '{key}': {e}")
            # Handle cache delete failure based on your application's requirements
            raise

    @staticmethod
    def clear_all_cache():
        """
        Clear all cached data.
        """
        try:
            cache.clear()
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")
            # Handle cache clear failure based on your application's requirements
            raise

def execute_cached_query(query_key, query_function, timeout=3600):
    """
    Execute a cached query or fetch from cache if available.

    Args:
    - query_key: Key to identify the cached query result.
    - query_function: Function that executes the query if not found in cache.
    - timeout: Timeout duration in seconds for caching (default is 1 hour).

    Returns:
    - Cached query result or result from query_function execution.

    Notes:
    - Uses Django's caching framework (defaulting to cache backend set in Django settings).
    - Logs any error encountered during query execution.
    """
    try:
        cached_result = cache.get(query_key)
        if cached_result is None:
            result = query_function()
            cache.set(query_key, result, timeout=timeout)
            return result
        return cached_result

    except Exception as e:
        # Handle and log cache execution errors
        handle_query_execution_error(query_name="Cached Query Execution", error_message=str(e))
        raise e  # Re-raise the exception for the caller to handle
