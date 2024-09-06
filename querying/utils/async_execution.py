# utils/async_execution.py
import asyncio
import time
from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.contrib.auth import get_user_model
from .logging import Logger
from .validation import QueryValidator

class AsyncExecutor:
    def __init__(self, user=None):
        self.user = user
        self.validator = QueryValidator(user=user)
        self.logger = Logger()  # Initialize the Logger class

    async def execute_async_query(self, query, query_params=None, timeout=30):
        """
        Execute a query asynchronously with timeout and retry mechanism.

        Args:
        - query: Asynchronous query function or coroutine.
        - query_params: Optional query parameters to validate before execution.
        - timeout: Time in seconds to wait for the query execution before timing out.

        Returns:
        - Result of the asynchronous query execution.
        """
        try:
            if query_params:
                await self.validate_query_params_async(query_params)

            start_time = time.time()
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(loop.run_in_executor(None, query), timeout=timeout)
            execution_time = time.time() - start_time

            if self.user:
                self.logger.log_query_execution(query_name="Async Query", executed_by=self.user.username, execution_time=execution_time)

            return result

        except ValidationError as ve:
            self.handle_query_validation_error(ve)
            raise ve

        except asyncio.TimeoutError:
            error_message = f"Query execution timed out after {timeout} seconds"
            self.logger.handle_query_execution_error(query_name="Async Query", error_message=error_message)
            raise TimeoutError(error_message)

        except Exception as e:
            self.logger.handle_query_execution_error(query_name="Async Query", error_message=str(e))
            raise e

    async def process_async_task(self, query_params):
        """
        Example of processing an asynchronous task using execute_query.
        """
        try:
            await self.validate_query_params_async(query_params)

            async def async_query():
                # Your asynchronous query logic here
                return "Query result"

            result = await self.execute_async_query(async_query, query_params=query_params)
            return result

        except ValidationError as ve:
            self.handle_query_validation_error(ve)
        except Exception as e:
            self.logger.handle_query_execution_error(query_name="Async Query", error_message=str(e))

    async def validate_query_params_async(self, query_params):
        """
        Asynchronous validation of query parameters.
        """
        await asyncio.get_event_loop().run_in_executor(None, self.validator.validate_query_params, query_params)

    def handle_query_validation_error(self, error):
        """
        Handle validation errors gracefully.
        Example: Log the error.
        """
        self.logger.logger.error(f"Validation Error: {error}")
        
    def handle_query_execution_error(self, error_message):
        """
        Handle query execution errors gracefully.
        Example: Log the error.
        """
        self.logger.logger.error(f"Execution Error: {error_message}")

    async def retry_async_operation(self, operation, retries=3, delay=1):
        """
        Retry an asynchronous operation a specified number of times with a delay.

        Args:
        - operation: Asynchronous operation function or coroutine.
        - retries: Number of retries before giving up.
        - delay: Delay in seconds between retries.

        Returns:
        - Result of the asynchronous operation if successful.
        """
        for attempt in range(retries):
            try:
                return await operation()
            except (DatabaseError, ValidationError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(delay)
                    self.logger.logger.warning(f"Retrying operation due to error: {e}. Attempt {attempt + 1}/{retries}")
                else:
                    self.logger.logger.error(f"Operation failed after {retries} attempts: {e}")
                    raise

    async def async_fetch_data(self, queryset):
        """
        Fetch data asynchronously from a queryset.

        Args:
        - queryset: Django QuerySet to fetch data from.

        Returns:
        - List of results from the queryset.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, list, queryset)

    async def async_save_data(self, model_instance):
        """
        Save a model instance asynchronously.

        Args:
        - model_instance: Django model instance to save.

        Returns:
        - Saved model instance.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, model_instance.save)

    async def async_delete_data(self, model_instance):
        """
        Delete a model instance asynchronously.

        Args:
        - model_instance: Django model instance to delete.

        Returns:
        - None
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, model_instance.delete)
