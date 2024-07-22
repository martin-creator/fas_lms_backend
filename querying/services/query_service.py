# services/query_service.py
from utils.query_execution import QueryExecutor

class QueryService:
    def __init__(self, user=None):
        self.executor = QueryExecutor(user=user)
    
    def execute_query(self, query_id):
        """
        Execute a query by its ID.
        """
        return self.executor.execute_query(query_id)
    
    def execute_sync_query(self, query_id):
        """
        Execute a synchronous query by its ID.
        """
        query = self.executor.get_query(query_id)
        return self.executor.execute_sync_query(query)
    
    def execute_parameterized_query(self, query, params):
        """
        Execute a parameterized query.
        """
        return self.executor.execute_parameterized_query(query, params)

    def execute_raw_sql(self, sql_query):
        """
        Execute a raw SQL query.
        """
        return self.executor.execute_query(sql_query)