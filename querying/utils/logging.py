# utils/logging.py
import logging
import json
import asyncio
from logging.handlers import RotatingFileHandler
from django.utils import timezone
from querying.models import QueryLog

# Configure the root logger
logger = logging.getLogger(__name__)
handler = RotatingFileHandler('lms.log', maxBytes=10**6, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

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
        log_entry = {
            'query_name': query_name,
            'executed_by': executed_by,
            'execution_time': execution_time,
            'timestamp': timezone.now().isoformat()
        }
        logger.info(json.dumps(log_entry))
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
        log_entry = {
            'query_name': query_name,
            'error_message': error_message,
            'timestamp': timezone.now().isoformat()
        }
        logger.error(json.dumps(log_entry))
        # Additional error handling logic such as sending alerts can be added here
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

        log_dict = {
            'user': user.username,
            'query': query,
            'timestamp': timestamp.isoformat()
        }
        logger.info(json.dumps(log_dict))
    except Exception as e:
        logger.error(f"Failed to log data access: {str(e)}")

async def log_async(log_func, *args, **kwargs):
    """
    Log asynchronously to avoid blocking operations.

    Args:
    - log_func: Logging function to execute asynchronously.
    - *args: Arguments for the logging function.
    - **kwargs: Keyword arguments for the logging function.

    Returns:
    - None
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, log_func, *args, **kwargs)

def log_performance_metrics(metrics):
    """
    Log performance metrics.

    Args:
    - metrics: Dictionary containing performance metrics to log.

    Returns:
    - None
    """
    try:
        metrics['timestamp'] = timezone.now().isoformat()
        logger.info(json.dumps(metrics))
    except Exception as e:
        logger.error(f"Failed to log performance metrics: {str(e)}")

def log_security_event(event_type, user, details):
    """
    Log security-related events.

    Args:
    - event_type: Type of the security event (e.g., 'authentication', 'authorization').
    - user: User object related to the event.
    - details: Additional details about the event.

    Returns:
    - None
    """
    try:
        log_entry = {
            'event_type': event_type,
            'user': user.username if user else 'Anonymous',
            'details': details,
            'timestamp': timezone.now().isoformat()
        }
        logger.warning(json.dumps(log_entry))
    except Exception as e:
        logger.error(f"Failed to log security event: {str(e)}")

def batch_log(entries):
    """
    Batch log entries to reduce I/O operations.

    Args:
    - entries: List of log entries to batch log.

    Returns:
    - None
    """
    try:
        for entry in entries:
            logger.info(json.dumps(entry))
    except Exception as e:
        logger.error(f"Failed to batch log entries: {str(e)}")