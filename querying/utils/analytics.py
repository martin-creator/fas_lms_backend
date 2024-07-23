# utils/analytics.py

import logging
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class UsageAnalytics:
    def __init__(self):
        self.usage_logs = defaultdict(list)

    def log_usage(self, query_id, user):
        """
        Log the usage of a query by a user.
        """
        log_entry = {
            'timestamp': datetime.now(),
            'user': user.username if user else 'anonymous'
        }
        self.usage_logs[query_id].append(log_entry)
        logger.debug(f"Logged usage for query {query_id} by user {log_entry['user']}")

    def get_usage_stats(self, query_id):
        """
        Get usage statistics for a specific query.
        """
        if query_id in self.usage_logs:
            return self.usage_logs[query_id]
        else:
            logger.warning(f"No usage statistics found for query {query_id}")
            return []

    def get_most_used_queries(self):
        """
        Get a list of the most frequently used queries.
        """
        usage_counts = {query_id: len(logs) for query_id, logs in self.usage_logs.items()}
        sorted_queries = sorted(usage_counts.items(), key=lambda item: item[1], reverse=True)
        return sorted_queries

    def get_user_activity(self, username):
        """
        Get the query activity of a specific user.
        """
        user_activity = {
            query_id: [log for log in logs if log['user'] == username]
            for query_id, logs in self.usage_logs.items()
        }
        return {query_id: logs for query_id, logs in user_activity.items() if logs}

    def generate_usage_report(self):
        """
        Generate a usage report for all queries.
        """
        report = {
            'total_queries': len(self.usage_logs),
            'most_used_queries': self.get_most_used_queries(),
            'user_activity': {username: self.get_user_activity(username) for username in self.get_all_users()}
        }
        return report

    def get_all_users(self):
        """
        Get a list of all users who have executed queries.
        """
        users = set()
        for logs in self.usage_logs.values():
            users.update(log['user'] for log in logs)
        return users
