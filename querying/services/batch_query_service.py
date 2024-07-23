# services/batch_query_service.py
import asyncio
from utils.async_execution import AsyncExecutor
from .query_service import QueryService
from utils.logging import Logger

class BatchQueryService:
    def __init__(self, user=None):
        self.executor = AsyncExecutor(user=user)
        self.query_service = QueryService(user=user)
        self.logger = Logger()

    async def execute_batch_queries(self, query_ids):
        """
        Execute multiple queries concurrently.
        """
        tasks = [self.query_service.execute_query(query_id) for query_id in query_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for query_id, result in zip(query_ids, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error executing query {query_id}: {result}")
        return results

    async def execute_batch_queries_with_retry(self, query_ids, retries=3, delay=1):
        """
        Execute multiple queries concurrently with retry mechanism.
        """
        tasks = [
            self.executor.retry_async_operation(lambda: self.query_service.execute_query(query_id), retries, delay)
                for query_id in query_ids
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for query_id, result in zip(query_ids, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error executing query {query_id} with retry: {result}")
        return results