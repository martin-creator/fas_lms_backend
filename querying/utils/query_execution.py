# utils/query_execution.py
import asyncio
import logging
import time
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import connection, DatabaseError, transaction
from django.utils import timezone
from .logging import log_query_execution, log_query_execution_error, handle_query_execution_error
from .pagination import execute_paged_query
from .caching import execute_cached_query
from .async_execution import execute_async_query, retry_async_operation
from querying.models import Query, QueryExecutionPermission, QueryLog
from django.contrib.auth import get_user_model
from .validation import QueryValidator

User = get_user_model()
logger = logging.getLogger(__name__)

class QueryExecutor:
    def __init__(self, user=None):
        self.user = user

    def execute_query(self, query_id):
        """
        Execute a query identified by its ID.

        Args:
        - query_id: ID of the query to execute.

        Returns:
        - Query result or None if execution failed.
        """
        try:
            query = Query.objects.get(pk=query_id)
        except Query.DoesNotExist:
            log_query_execution_error(query_name=f"Query ID: {query_id}", error_message="Query does not exist.")
            return None

        if not self.has_permission(query):
            log_query_execution_error(query_name=query.name, error_message="Permission denied.")
            return None

        try:
            # Example: Execute query asynchronously if specified
            if query.query_params.get('async', False):
                result = self.execute_async_query(query)
            else:
                result = self.execute_sync_query(query)

            # Log successful execution
            log_query_execution(query_name=query.name, executed_by=self.user.username, execution_time=result.get('execution_time', 0))
            return result

        except Exception as e:
            log_query_execution_error(query_name=query.name, error_message=str(e))
            return None

    def execute_sync_query(self, query):
        """
        Execute a synchronous query.

        Args:
        - query: Query object to execute.

        Returns:
        - Query result dictionary with execution details.
        """
        start_time = timezone.now()

        # Example: Parameterized query execution
        params = query.query_params.get('params', {})
        queryset = self.execute_parameterized_query(query.queryset(), params)

        # Example: Pagination
        if query.query_params.get('paginate', False):
            page_number = query.query_params.get('page_number', 1)
            page_size = query.query_params.get('page_size', 10)
            results = execute_paged_query(queryset, page_number, page_size)
        else:
            results = list(queryset)

        end_time = timezone.now()
        execution_time = (end_time - start_time).total_seconds()

        # Example: Caching the query result
        if query.query_params.get('cache', False):
            cache_key = f"query_result_{query.id}"
            execute_cached_query(cache_key, lambda: results)

        # Example: Logging query execution duration
        log_entry = QueryLog(query=query, executed_by=self.user, executed_at=start_time, execution_duration=execution_time)
        log_entry.save()

        return {'results': results, 'execution_time': execution_time}

    async def execute_async_query(self, query):
        """
        Execute an asynchronous query.

        Args:
        - query: Query object to execute.

        Returns:
        - Asynchronous execution result dictionary.
        """
        async_result = await execute_async_query(query.async_execution())
        return async_result

    def has_permission(self, query):
        """
        Check if the current user has permission to execute a query.

        Args:
        - query: Query object to check permissions for.

        Returns:
        - Boolean indicating if the user has permission.
        """
        if not self.user:
            return False

        try:
            permission = QueryExecutionPermission.objects.get(query=query)
            return self.user.groups.filter(id__in=permission.allowed_groups.all()).exists() or permission.allowed_users.filter(id=self.user.id).exists()
        except QueryExecutionPermission.DoesNotExist:
            return False

    @staticmethod
    def execute_parameterized_query(query, params):
        """
        Execute a parameterized query safely.

        Args:
        - query: Django ORM query or raw SQL query.
        - params: Dictionary of parameters to filter or execute the query. 

        Returns:
        - QuerySet or result of the parameterized query execution.
        """
        # Example implementation using Django ORM
        return query.filter(**params)

    @staticmethod
    def execute_query(query_string, user=None):
        """
        Execute a database query.

        Args:
        - query_string: SQL query string to execute.
        - user: User object (optional) performing the query.

        Returns:
        - Query result as fetched from the database.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query_string)
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    return [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]
                else:
                    return None
        except Exception as e:
            log_query_execution_error(query_string, str(e))
            raise

    @staticmethod
    def log_query_execution(query_string, user=None):
        """
        Log query execution details.

        Args:
        - query_string: SQL query string executed.
        - user: User object performing the query (optional).

        Returns:
        - None
        """
        try:
            log_entry = QueryLog(query=query_string, user=user, timestamp=timezone.now())
            log_entry.save()
        except Exception as e:
            raise RuntimeError(f"Failed to log query execution: {str(e)}")

    @staticmethod
    def log_query_execution_error(query_string, error_message, user=None):
        """
        Log query execution errors.

        Args:
        - query_string: SQL query string that caused the error.
        - error_message: Error message describing the issue.
        - user: User object (optional) performing the query.

        Returns:
        - None
        """
        try:
            error_log_entry = QueryLog(
                query=query_string,
                error_message=error_message,
                user=user,
                timestamp=timezone.now(),
                is_error=True
            )
            error_log_entry.save()
        except Exception as e:
            raise RuntimeError(f"Failed to log query execution error: {str(e)}")

    @staticmethod
    def check_query_execution_permission(query_string, user):
        """
        Check if the user has permission to execute the query.

        Args:
        - query_string: SQL query string to be executed.
        - user: User object performing the query.

        Returns:
        - Boolean indicating whether the user has permission to execute the query.
        """
        try:
            permission = QueryExecutionPermission.objects.get(query=query_string)
            return user.groups.filter(id__in=permission.allowed_groups.all()).exists() or permission.allowed_users.filter(id=user.id).exists()
        except ObjectDoesNotExist:
            return False

    @staticmethod
    def recommend_indexing_strategy(table_name, query):
        """
        Recommend indexing strategy based on the query.

        Args:
        - table_name: Name of the database table.
        - query: Query object or SQL string.

        Returns:
        - Recommended indexing strategy as a list of field names.
        """
        if isinstance(query, str):
            sql_query = query
        else:
            sql_query = query.query_params.get('query', '')

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"EXPLAIN ANALYZE {sql_query}")
                query_plan = cursor.fetchall()

                index_recommendations = []
                for row in query_plan:
                    if 'Seq Scan' in row[0]:
                        index_recommendations.append(row[0].split('on ')[-1].strip())

                return index_recommendations
        except Exception as e:
            raise RuntimeError(f"Failed to recommend indexing strategy: {str(e)}")

    def notify_admins(self, message):
        """
        Notify administrators of critical errors.

        Args:
        - message: Message to send to administrators.

        Returns:
        - None
        """
        # Implement your notification logic here, e.g., send an email or a message to a monitoring system
        pass

    async def async_fetch_data(self, queryset):
        """
        Fetch data asynchronously from a queryset.

        Args:
        - queryset: Django QuerySet to fetch data from.

        Returns:
        - List of results from the queryset.
        “””
        return await asyncio.to_thread(list, queryset)
        
    async def async_save_data(self, model_instance):
        """
        Save a Django model instance asynchronously.
    
        Args:
        - model_instance: Django model instance to save.
    
        Returns:
        - Saved model instance.
        """
        return await asyncio.to_thread(model_instance.save)
    
    async def async_delete_data(self, model_instance):
        """
        Delete a Django model instance asynchronously.
    
        Args:
        - model_instance: Django model instance to delete.
    
        Returns:
        - None.
        """
        return await asyncio.to_thread(model_instance.delete)