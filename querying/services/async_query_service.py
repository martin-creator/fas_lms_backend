# services/async_query_service.py
from utils.async_execution import AsyncExecutor
from utils.caching import CacheManager
from utils.pagination import PaginatorService
from utils.logging import Logger
from .query_service import QueryService
from django.core.exceptions import ValidationError

class AsyncQueryService:
    def __init__(self, user=None):
        self.executor = AsyncExecutor(user=user)
        self.query_service = QueryService(user=user)
        self.paginator = PaginatorService()
        self.logger = Logger()
        self.cache = CacheManager()
        self.user = user

    async def execute_async_query(self, query_id, page_number=1, page_size=10):
        try:
            query = self.query_service.get_query(query_id)
            await self.executor.validate_query_params_async(query.query_params, self.user)

            cache_key = f"query_result_{query_id}"
            result = await self.cache.execute_cached_query(cache_key, lambda: self.executor.execute_async_query(query))

            paged_result = self.paginator.execute_paged_query(result['results'], page_number, page_size)
            
            self.logger.log_query_execution(query_name=query.name, executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return {'results': paged_result, 'execution_time': result.get('execution_time', 0)}
        except ValidationError as ve:
            self.executor.handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            self.executor.handle_query_execution_error(query_name=query.name, error_message=str(e))
            raise e

    async def execute_async_custom_query(self, query_func, query_params=None):
        try:
            if query_params:
                await self.executor.validate_query_params_async(query_params, self.user)
            
            result = await self.executor.execute_async_query(query_func)
            self.logger.log_query_execution(query_name="Custom Async Query", executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return result
        except ValidationError as ve:
            self.executor.handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            self.executor.handle_query_execution_error(query_name="Custom Async Query", error_message=str(e))
            raise e

    async def execute_async_query_with_retry(self, query_func, retries=3, delay=1, query_params=None):
        try:
            if query_params:
                await self.executor.validate_query_params_async(query_params, self.user)
            
            result = await self.executor.retry_async_operation(lambda: self.executor.execute_async_query(query_func), retries, delay)
            self.logger.log_query_execution(query_name="Async Query with Retry", executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return result
        except ValidationError as ve:
            self.executor.handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            self.executor.handle_query_execution_error(query_name="Async Query with Retry", error_message=str(e))
            raise e

    async def fetch_data(self, queryset):
        return await self.executor.async_fetch_data(queryset)

    async def save_data(self, model_instance):
        return await self.executor.async_save_data(model_instance)

    async def delete_data(self, model_instance):
        return await self.executor.async_delete_data(model_instance)
