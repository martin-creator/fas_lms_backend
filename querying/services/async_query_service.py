# services/async_query_service.py

from utils.async_execution import AsyncExecutor
from utils.caching import CacheManager
from utils.pagination import PaginatorService
from utils.logging import Logger
from .query_service import QueryService
from django.core.exceptions import ValidationError

class AsyncQueryService:
    """
    A service class for managing and executing asynchronous queries with support for caching, pagination, and retries.

    Attributes:
        executor (AsyncExecutor): The executor for asynchronous operations.
        query_service (QueryService): The service for retrieving query definitions.
        paginator (PaginatorService): The service for handling query result pagination.
        logger (Logger): The logger for recording query execution details.
        cache (CacheManager): The manager for caching query results.
        user (User, optional): The user associated with query operations. Defaults to None.
    """

    def __init__(self, user=None):
        """
        Initialize the AsyncQueryService with utility services and optional user context.

        Args:
            user (User, optional): The user performing the query operations. Defaults to None.
        """
        self.executor = AsyncExecutor(user=user)
        self.query_service = QueryService(user=user)
        self.paginator = PaginatorService()
        self.logger = Logger()
        self.cache = CacheManager()
        self.user = user

    async def execute_async_query(self, query_id, page_number=1, page_size=10):
        """
        Execute an asynchronous query based on the provided query ID, with optional pagination.

        Args:
            query_id (str): The unique identifier for the query to be executed.
            page_number (int, optional): The page number for pagination. Defaults to 1.
            page_size (int, optional): The number of results per page. Defaults to 10.

        Returns:
            dict: A dictionary containing:
                - 'results': The paginated results of the query.
                - 'execution_time': The time taken to execute the query in seconds.

        Raises:
            ValidationError: If the query parameters are invalid.
            Exception: For any errors encountered during query execution.

        Notes:
            - Retrieves the query definition using `QueryService`.
            - Validates the query parameters asynchronously.
            - Caches the query results to improve performance.
            - Applies pagination to the results.
            - Logs details of the query execution, including execution time.
        """
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
        """
        Execute a custom asynchronous query function with optional parameters.

        Args:
            query_func (callable): The custom function to execute asynchronously.
            query_params (dict, optional): Parameters for the custom query function. Defaults to None.

        Returns:
            dict: The result of the custom query execution, including execution time.

        Raises:
            ValidationError: If the query parameters are invalid.
            Exception: For any errors encountered during query execution.

        Notes:
            - Validates the query parameters asynchronously if provided.
            - Executes the custom query function asynchronously.
            - Logs details of the query execution, including execution time.
        """
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
        """
        Execute an asynchronous query function with retry logic.

        Args:
            query_func (callable): The function to execute asynchronously.
            retries (int, optional): The number of retry attempts in case of failure. Defaults to 3.
            delay (int, optional): The delay between retry attempts in seconds. Defaults to 1.
            query_params (dict, optional): Parameters for the query function. Defaults to None.

        Returns:
            dict: The result of the query execution after retries.

        Raises:
            ValidationError: If the query parameters are invalid.
            Exception: For any errors encountered during query execution after retries.

        Notes:
            - Validates the query parameters asynchronously if provided.
            - Retries the query execution upon failure, with configurable retry attempts and delay.
            - Logs details of the query execution, including execution time.
        """
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
        """
        Asynchronously fetch data from a queryset.

        Args:
            queryset (QuerySet): The queryset from which to fetch data.

        Returns:
            list: A list of data fetched from the queryset.

        Notes:
            - Utilizes the `AsyncExecutor` to fetch data asynchronously.
        """
        return await self.executor.async_fetch_data(queryset)

    async def save_data(self, model_instance):
        """
        Asynchronously save a Django model instance.

        Args:
            model_instance (Model): The Django model instance to be saved.

        Returns:
            Model: The saved model instance.

        Notes:
            - Utilizes the `AsyncExecutor` to save the model instance asynchronously.
        """
        return await self.executor.async_save_data(model_instance)

    async def delete_data(self, model_instance):
        """
        Asynchronously delete a Django model instance.

        Args:
            model_instance (Model): The Django model instance to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.

        Notes:
            - Utilizes the `AsyncExecutor` to delete the model instance asynchronously.
        """
        return await self.executor.async_delete_data(model_instance)