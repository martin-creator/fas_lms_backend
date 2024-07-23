# services/query_notification_service.py
from utils.logging import Logger

class QueryNotificationService:
    def __init__(self):
        self.logger = Logger()

    def notify_admins(self, message):
        """
        Notify administrators of critical errors.
        """
        self.logger.notify_admins(message)