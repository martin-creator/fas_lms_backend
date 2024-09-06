# utils/logging.py
import logging
import json
import asyncio
from logging.handlers import RotatingFileHandler
from django.utils import timezone
from querying.models import QueryLog

class Logger:
    def __init__(self, log_file='lms.log', max_bytes=10**6, backup_count=5):
        """
        Initialize the Logger class with a RotatingFileHandler.

        Args:
        - log_file (str): Path to the log file. Defaults to 'lms.log'.
        - max_bytes (int): Maximum file size before rotation. Defaults to 1MB (10**6 bytes).
        - backup_count (int): Number of backup files to keep. Defaults to 5.

        This configures the root logger with a file handler that rotates logs when they reach a certain size.
        The logs are stored in the specified log file, with a maximum file size and backup count as defined.
        """
        self.logger = logging.getLogger(__name__)
        handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
    def info(self, message):
        """Log an informational message."""
        self.logger.info(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def log_query_execution(self, query_name, executed_by, execution_time):
        """
        Log details about the execution of a query.

        Args:
        - query_name (str): Name or description of the query that was executed.
        - executed_by (str): The user or system that executed the query.
        - execution_time (float): The time taken to execute the query, in seconds.

        Logs the query execution details in JSON format, including a timestamp.

        Raises:
        - Exception: If logging the query execution fails, an error message is logged.
        """
        try:
            log_entry = {
                'query_name': query_name,
                'executed_by': executed_by,
                'execution_time': execution_time,
                'timestamp': timezone.now().isoformat()
            }
            self.logger.info(json.dumps(log_entry))
        except Exception as e:
            self.logger.error(f"Failed to log query execution: {str(e)}")

    def handle_query_execution_error(self, query_name, error_message):
        """
        Handle and log errors encountered during query execution.

        Args:
        - query_name (str): Name or description of the query that caused the error.
        - error_message (str): Detailed error message or description.

        Logs the error details in JSON format, including a timestamp.

        Raises:
        - Exception: If logging the error fails, an error message is logged.
        """
        try:
            log_entry = {
                'query_name': query_name,
                'error_message': error_message,
                'timestamp': timezone.now().isoformat()
            }
            self.logger.error(json.dumps(log_entry))
        except Exception as e:
            self.logger.error(f"Failed to handle query execution error: {str(e)}")

    def log_data_access(self, user, query, timestamp=None):
        """
        Log access to data for auditing purposes.

        Args:
        - user (User): User object who accessed the data.
        - query (str): Description of the query or action performed.
        - timestamp (datetime, optional): Timestamp of the data access event. Defaults to the current time if not provided.

        Saves the access event in the QueryLog model and logs the event details in JSON format.

        Raises:
        - Exception: If logging the data access fails, an error message is logged.
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
            self.logger.info(json.dumps(log_dict))
        except Exception as e:
            self.logger.error(f"Failed to log data access: {str(e)}")

    async def log_async(self, log_func, *args, **kwargs):
        """
        Log asynchronously to avoid blocking operations.

        Args:
        - log_func (callable): Logging function to be executed asynchronously.
        - *args: Positional arguments to pass to the logging function.
        - **kwargs: Keyword arguments to pass to the logging function.

        Uses asyncio to run the logging function in a non-blocking manner.

        Raises:
        - Exception: If asynchronous logging fails, an error message is logged.
        """
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, log_func, *args, **kwargs)
        except Exception as e:
            self.logger.error(f"Failed to log asynchronously: {str(e)}")

    def log_performance_metrics(self, metrics):
        """
        Log performance metrics for monitoring and analysis.

        Args:
        - metrics (dict): Dictionary containing performance metrics to log.

        Adds a timestamp to the metrics and logs them in JSON format.

        Raises:
        - Exception: If logging performance metrics fails, an error message is logged.
        """
        try:
            metrics['timestamp'] = timezone.now().isoformat()
            self.logger.info(json.dumps(metrics))
        except Exception as e:
            self.logger.error(f"Failed to log performance metrics: {str(e)}")

    def log_security_event(self, event_type, user, details):
        """
        Log security-related events for auditing and alerting.

        Args:
        - event_type (str): Type of the security event (e.g., 'authentication', 'authorization').
        - user (User, optional): User object related to the event. Defaults to 'Anonymous' if not provided.
        - details (str): Additional details about the event.

        Logs security events in JSON format, including a timestamp.

        Raises:
        - Exception: If logging security events fails, an error message is logged.
        """
        try:
            log_entry = {
                'event_type': event_type,
                'user': user.username if user else 'Anonymous',
                'details': details,
                'timestamp': timezone.now().isoformat()
            }
            self.logger.warning(json.dumps(log_entry))
        except Exception as e:
            self.logger.error(f"Failed to log security event: {str(e)}")

    def batch_log(self, entries):
        """
        Log multiple entries in a batch to reduce I/O operations.

        Args:
        - entries (list): List of log entries to be logged.

        Each entry is logged in JSON format.

        Raises:
        - Exception: If batching logs fails, an error message is logged.
        """
        try:
            for entry in entries:
                self.logger.info(json.dumps(entry))
        except Exception as e:
            self.logger.error(f"Failed to batch log entries: {str(e)}")
