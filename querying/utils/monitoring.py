# utils/monitoring.py

import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class QueryMonitor:
    def __init__(self):
        self.query_logs = {}
        self.slow_query_threshold = timedelta(seconds=2)  # Example threshold for slow queries

    def start_query(self, query_id):
        """
        Start monitoring a query execution.
        """
        self.query_logs[query_id] = {
            'start_time': datetime.now(),
            'executions': self.query_logs.get(query_id, {}).get('executions', 0) + 1
        }
        logger.debug(f"Started monitoring query {query_id}")

    def end_query(self, query_id):
        """
        End monitoring a query execution and log the execution time.
        """
        if query_id not in self.query_logs:
            logger.warning(f"Query {query_id} not found in query logs.")
            return

        start_time = self.query_logs[query_id]['start_time']
        end_time = datetime.now()
        execution_time = end_time - start_time

        self.query_logs[query_id]['last_execution_time'] = execution_time

        if execution_time > self.slow_query_threshold:
            logger.warning(f"Query {query_id} is slow: {execution_time.total_seconds()} seconds")

        logger.debug(f"Query {query_id} execution time: {execution_time.total_seconds()} seconds")

    def record(self, query_id, result):
        """
        Record the result of a query execution.
        """
        self.end_query(query_id)
        logger.info(f"Query {query_id} executed with result: {result}")

    def get_query_stats(self, query_id):
        """
        Get statistics for a specific query.
        """
        if query_id in self.query_logs:
            return self.query_logs[query_id]
        else:
            logger.warning(f"No statistics found for query {query_id}")
            return {}

    def get_slow_queries(self):
        """
        Get a list of queries that are considered slow.
        """
        slow_queries = [
            query_id for query_id, log in self.query_logs.items()
            if log.get('last_execution_time', timedelta(0)) > self.slow_query_threshold
        ]
        return slow_queries
