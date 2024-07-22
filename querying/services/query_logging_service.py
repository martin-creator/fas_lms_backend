# services/query_logging_service.py
from utils.logging import log_query_execution, log_query_execution_error

class QueryLoggingService:
    def log_execution(self, query_name, executed_by, execution_time):
        """
        Log query execution details.
        """
        log_query_execution(query_name, executed_by, execution_time)
    
    def log_error(self, query_name, error_message):
        """
        Log query execution error details.
        """
        log_query_execution_error(query_name, error_message)