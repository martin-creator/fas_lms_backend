# services/async_query_service.py
from utils.async_execution import execute_async_query
from .query_service.py import QueryService

class AsyncQueryService:
    def __init__(self, user=None):
        self.query_service = QueryService(user=user)
    
    async def execute_async_query(self, query_id):
        """
        Execute an asynchronous query by its ID.
        """
        query = self.query_service.get_query(query_id)
        return await execute_async_query(query)
    
    async def execute_async_custom_query(self, query_func):
        """
        Execute a custom asynchronous query.
        """
        return await execute_async_query(query_func)