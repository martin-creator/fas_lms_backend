# services/query_cache_service.py
from utils.caching import execute_cached_query

class QueryCacheService:
    def cache_query_result(self, cache_key, result):
        """
        Cache query result with a specific key.
        """
        execute_cached_query(cache_key, lambda: result)
    
    def get_cached_query_result(self, cache_key):
        """
        Retrieve cached query result by key.
        """
        return execute_cached_query(cache_key)