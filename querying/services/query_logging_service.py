# services/query_logging_service.py
from utils.logging import Logger

class QueryLoggingService:
    def __init__(self):
        self.logger = Logger()

    def log_execution(self, query_name, executed_by, execution_time):
        """
        Log query execution details.
        """
        self.logger.log_query_execution(query_name, executed_by, execution_time)
    
    def log_error(self, query_name, error_message):
        """
        Log query execution error details.
        """
        self.logger.handle_query_execution_error(query_name, error_message)