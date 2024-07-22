# services/async_query_service.py
from utils.async_execution import (
    execute_async_query,
    retry_async_operation,
    validate_query_params_async,
    handle_query_execution_error,
    handle_query_validation_error,
    async_fetch_data,
    async_save_data,
    async_delete_data
)
from utils.caching import execute_cached_query
from utils.pagination import execute_paged_query
from utils.logging import log_query_execution
from .query_service import QueryService
from django.core.exceptions import ValidationError

class AsyncQueryService:
    def __init__(self, user=None):
        self.query_service = QueryService(user=user)
        self.user = user

    async def execute_async_query(self, query_id, page_number=1, page_size=10):
        try:
            query = self.query_service.get_query(query_id)
            await validate_query_params_async(query.query_params, self.user)

            cache_key = f"query_result_{query_id}"
            result = await execute_cached_query(cache_key, lambda: execute_async_query(query))

            paged_result = execute_paged_query(result['results'], page_number, page_size)
            
            log_query_execution(query_name=query.name, executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return {'results': paged_result, 'execution_time': result.get('execution_time', 0)}
        except ValidationError as ve:
            handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            handle_query_execution_error(query_name=query.name, error_message=str(e))
            raise e

    async def execute_async_custom_query(self, query_func, query_params=None):
        try:
            if query_params:
                await validate_query_params_async(query_params, self.user)
            
            result = await execute_async_query(query_func)
            log_query_execution(query_name="Custom Async Query", executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return result
        except ValidationError as ve:
            handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            handle_query_execution_error(query_name="Custom Async Query", error_message=str(e))
            raise e

    async def execute_async_query_with_retry(self, query_func, retries=3, delay=1, query_params=None):
        try:
            if query_params:
                await validate_query_params_async(query_params, self.user)
            
            result = await retry_async_operation(lambda: execute_async_query(query_func), retries, delay)
            log_query_execution(query_name="Async Query with Retry", executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return result
        except ValidationError as ve:
            handle_query_validation_error(ve)
            raise ve
        except Exception as e:
            handle_query_execution_error(query_name="Async Query with Retry", error_message=str(e))
            raise e

    async def fetch_data(self, queryset):
        return await async_fetch_data(queryset)

    async def save_data(self, model_instance):
        return await async_save_data(model_instance)

    async def delete_data(self, model_instance):
        return await async_delete_data(model_instance)
