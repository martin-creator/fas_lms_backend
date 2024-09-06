# services/query_cache_service.py
from utils.caching import CacheManager

class QueryCacheService:
    def __init__(self):
        self.cache = CacheManager()

    def cache_query_result(self, cache_key, result):
        """
        Cache query result with a specific key.
        """
        self.cache.set_cache(cache_key, result)
    
    def get_cached_query_result(self, cache_key):
        """
        Retrieve cached query result by key.
        """
        return self.cache.get_cache(cache_key)
    
    def invalidate_cache(self, cache_key):
        """
        Invalidate cache for a specific key.
        """
        self.cache.invalidate_cache_by_prefix(cache_key)