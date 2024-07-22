# services/query_service.py
from utils.query_execution import QueryExecutor
from utils.validation import QueryValidator
from utils.security import sanitize_input
from utils.cache import CacheManager, RedisCacheManager
from utils.logging import Logger
from utils.monitoring import QueryMonitor
from utils.analytics import UsageAnalytics
from querying.models import Query
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
import asyncio

class QueryService:
    def __init__(self, user=None):
        self.executor = QueryExecutor(user=user)
        self.cache = RedisCacheManager() if user else CacheManager()
        self.logger = Logger()
        self.monitor = QueryMonitor()
        self.analytics = UsageAnalytics()
        self.user = user
    
    def execute_query(self, query_id):
        """
        Execute a query by its ID with logging, caching, and monitoring.
        """
        try:
            query = self.get_query(query_id)
            self.analytics.log_usage(query_id, self.user)

            # Check cache first
            cache_key = f"query_result_{query_id}"
            cached_result = self.cache.fetch(cache_key)
            if cached_result:
                return cached_result

            # Execute and cache the query result
            result = self.executor.execute_query(query_id)
            self.cache.store(cache_key, result)
            self.monitor.record(query_id, result)
            return result

        except Exception as e:
            self.logger.log_error(query_id, str(e))
            raise e

    def execute_sync_query(self, query_id):
        """
        Execute a synchronous query by its ID with logging and monitoring.
        """
        try:
            query = self.get_query(query_id)
            self.analytics.log_usage(query_id, self.user)
            result = self.executor.execute_sync_query(query)
            self.monitor.record(query_id, result)
            return result
        except Exception as e:
            self.logger.log_error(query_id, str(e))
            raise e

    def execute_parameterized_query(self, query, params):
        """
        Execute a parameterized query with input sanitization.
        """
        sanitized_params = sanitize_input(params)
        return self.executor.execute_parameterized_query(query, sanitized_params)

    def execute_raw_sql(self, sql_query):
        """
        Execute a raw SQL query with input sanitization.
        """
        sanitized_query = sanitize_input(sql_query)
        return self.executor.execute_query(sanitized_query)

    def validate_query(self, query_id):
        """
        Validate a query by its ID.
        """
        try:
            query = self.get_query(query_id)
            validator = QueryValidator(query.query_params)
            validator.validate()
            return True
        except ValidationError as ve:
            self.executor.handle_query_validation_error(ve)
            return False

    def get_query(self, query_id):
        """
        Retrieve a query by its ID.
        """
        try:
            return Query.objects.get(pk=query_id)
        except Query.DoesNotExist:
            self.executor.log_query_execution_error(query_name=f"Query ID: {query_id}", error_message="Query does not exist.")
            return None

    def has_permission(self, query_id):
        """
        Check if the user has permission to execute a query by its ID.
        """
        query = self.get_query(query_id)
        if query:
            return self.executor.has_permission(query)
        return False

    def recommend_indexing(self, query_id):
        """
        Recommend indexing strategy for a query by its ID.
        """
        query = self.get_query(query_id)
        if query:
            return self.executor.recommend_indexing_strategy(query.model._meta.db_table, query.query_string)
        return []

    @transaction.atomic
    def log_execution(self, query_id, success=True, error_message=None):
        """
        Log the execution of a query by its ID.
        """
        query = self.get_query(query_id)
        if query:
            log_entry = QueryLog(
                query=query,
                executed_by=self.user,
                executed_at=timezone.now(),
                is_error=not success,
                error_message=error_message
            )
            log_entry.save()

    def execute_query_with_logging(self, query_id):
        """
        Execute a query by its ID and log the execution details.
        """
        try:
            result = self.execute_query(query_id)
            self.log_execution(query_id, success=True)
            return result
        except Exception as e:
            self.log_execution(query_id, success=False, error_message=str(e))
            raise e

    def execute_custom_query(self, custom_func, *args, **kwargs):
        """
        Execute a custom query function with provided arguments.
        """
        try:
            result = custom_func(*args, **kwargs)
            self.executor.log_query_execution(query_name="Custom Query", executed_by=self.user.username)
            return result
        except Exception as e:
            self.executor.log_query_execution_error(query_name="Custom Query", error_message=str(e))
            raise e

    def cache_query_result(self, query_id, result):
        """
        Cache the result of a query execution.
        """
        query = self.get_query(query_id)
        if query and query.query_params.get('cache', False):
            cache_key = f"query_result_{query_id}"
            self.cache.store(cache_key, result)

    def fetch_cached_query_result(self, query_id):
        """
        Fetch cached result of a query execution.
        """
        query = self.get_query(query_id)
        if query and query.query_params.get('cache', False):
            cache_key = f"query_result_{query_id}"
            return self.cache.fetch(cache_key)
        return None

    def notify_admins(self, message):
        """
        Notify administrators of critical errors.
        """
        self.executor.notify_admins(message)

    def execute_async_query(self, query_id):
        """
        Execute an asynchronous query by its ID.
        """
        try:
            query = self.get_query(query_id)
            if not query:
                raise ValidationError("Query does not exist.")
            return asyncio.run(self.executor.execute_async_query(query))
        except Exception as e:
            self.logger.log_error(query_id, str(e))
            raise e

    def execute_async_custom_query(self, query_func, query_params=None):
        """
        Execute a custom asynchronous query function with optional parameters.
        """
        try:
            return asyncio.run(self.executor.execute_async_custom_query(query_func, query_params))
        except Exception as e:
            self.logger.log_error("Custom Async Query", str(e))
            raise e

    def execute_async_query_with_retry(self, query_func, retries=3, delay=1, query_params=None):
        """
        Execute an asynchronous query function with retry logic.
        """
        try:
            return asyncio.run(self.executor.execute_async_query_with_retry(query_func, retries, delay, query_params))
        except Exception as e:
            self.logger.log_error("Async Query with Retry", str(e))
            raise e

    async def fetch_data_async(self, queryset):
        “””
        Asynchronously fetch data from a queryset.
        “””
        return await self.executor.async_fetch_data(queryset)
        
    async def save_data_async(self, model_instance):
        """
        Asynchronously save a Django model instance.
        """
        return await self.executor.async_save_data(model_instance)
    
    async def delete_data_async(self, model_instance):
        """
        Asynchronously delete a Django model instance.
        """
        return await self.executor.async_delete_data(model_instance)