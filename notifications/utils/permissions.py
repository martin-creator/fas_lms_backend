import logging
from django.core.exceptions import PermissionDenied



logger = logging.getLogger(__name__)

class PermissionChecker:
    """
    Service for managing notifications within the application.
    """

    @staticmethod
    def user_can_manage_notifications(user):
        """
        Check if the user has permission to manage notifications.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('notifications.can_manage_notifications')

    @staticmethod
    def user_can_view_notifications(user):
        """
        Check if the user has permission to view notifications.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('notifications.can_view_notifications')

    @staticmethod
    def check_permission_for_action(user, action):
        """
        Check if the user has permission to perform the specified action on a notification.

        Args:
            user (User): The user performing the action.
            action (str): The action to perform (e.g., 'update_priority', 'add_share', 'update_html_content').

        Raises:
            PermissionDenied: If the user does not have permission for the action.
        """
        if action in ['update_priority', 'add_share', 'update_html_content', 'update_delivery_method', 'update_severity', 'update_notification_type']:
            if not PermissionChecker.user_can_manage_notifications(user):
                raise PermissionDenied(f"You do not have permission to {action.replace('_', ' ')}.")
        elif action == 'view_notification':
            if not PermissionChecker.user_can_view_notifications(user):
                raise PermissionDenied("You do not have permission to view the notification.")
        else:
            raise ValueError(f"Unknown action: {action}")

