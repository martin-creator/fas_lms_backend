# utils/logging.py
import logging
from querying.models import QueryLog
from django.utils import timezone

logger = logging.getLogger(__name__)

def log_query_execution(query_name, executed_by, execution_time):
    """
    Log query execution details.

    Args:
    - query_name: Name or description of the executed query.
    - executed_by: User or system executing the query.
    - execution_time: Execution time in seconds.

    Returns:
    - None
    """
    try:
        logger.info(f"Query '{query_name}' executed by '{executed_by}' in {execution_time:.4f} seconds.")
    except Exception as e:
        logger.error(f"Failed to log query execution: {str(e)}")

def handle_query_execution_error(query_name, error_message):
    """
    Handle query execution errors.

    Args:
    - query_name: Name or description of the query that caused the error.
    - error_message: Error message or details.

    Returns:
    - None
    """
    try:
        logger.error(f"Error executing query '{query_name}': {error_message}")
        # Implement additional error handling logic as needed, e.g., send alerts
    except Exception as e:
        logger.error(f"Failed to handle query execution error: {str(e)}")

def log_data_access(user, query, timestamp=None):
    """
    Log data access events for auditing purposes.

    Args:
    - user: User object who accessed the data.
    - query: Query or action performed.
    - timestamp: Timestamp of the data access event (default is current time).

    Returns:
    - None
    """
    try:
        if timestamp is None:
            timestamp = timezone.now()
        
        log_entry = QueryLog(user=user, query=query, timestamp=timestamp)
        log_entry.save()
        logger.info(f"Data access logged for user '{user.username}' at {timestamp}. Query: '{query}'")
    except Exception as e:
        logger.error(f"Failed to log data access: {str(e)}")
