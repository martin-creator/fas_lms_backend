import logging
from notifications.utils.permissions import PermissionChecker

logger = logging.getLogger(__name__)

class NotificationsValidator:
    @staticmethod
    def validate_notification_data(notification_data):
        if 'content' not in notification_data or not notification_data['content']:
            return False
        if 'recipient_id' not in notification_data or not isinstance(notification_data['recipient_id'], int):
            return False
        return True

    @staticmethod
    def handle_notification_failure(data, error_message):
        logger.error(f"Failed to send notification for user {data['recipient']}: {error_message}")

    @staticmethod
    def validate_notification_permissions(user, notification_type):
        # Use PermissionChecker to validate notification permissions
        if not PermissionChecker.user_can_view_notifications(user):
            return False
        # Add additional checks for notification_type if needed
        return True
