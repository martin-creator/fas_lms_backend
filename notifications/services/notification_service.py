# notifications/services/notification_service.py

from django.utils import timezone
from notifications.models import Notification, NotificationType, NotificationTemplate, NotificationSettings, NotificationReadStatus
from notifications.reports.notification_report import (
    generate_user_notification_report,
    generate_notification_summary
)
from notifications.querying.notification_query import (
    get_notifications_by_user,
    search_notifications
)
from notifications.utils.notification_utils import (
    format_notification_data,
    validate_notification_data
)
from notifications.helpers.notification_helpers import (
    process_notification_data,
    validate_notification_permissions,
    send_push_notification
)
from notifications.settings.notification_settings import (
    get_notification_settings,
    update_notification_settings
)
from notifications.serializers import (
    NotificationSerializer,
    NotificationTypeSerializer,
    NotificationTemplateSerializer,
    NotificationSettingsSerializer,
    NotificationReadStatusSerializer
)

class NotificationService:

    @staticmethod
    def send_notification(data):
        """
        Send a notification to a user.

        Args:
        - data (dict): Data for creating the notification.

        Returns:
        - Notification: The created Notification object.
        """
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            # Send push notification as an example
            if data.get('notification_type') == 'push':
                send_push_notification(data['recipient'], data['content'])
            return notification
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def mark_notification_as_read(notification_id):
        """
        Mark a notification as read.

        Args:
        - notification_id (int): ID of the notification to mark as read.
        """
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete a notification.

        Args:
        - notification_id (int): ID of the notification to delete.
        """
        Notification.objects.filter(id=notification_id).delete()

    @staticmethod
    def get_user_notifications(user_id):
        """
        Get all notifications for a specific user.

        Args:
        - user_id (int): ID of the user to retrieve notifications for.

        Returns:
        - QuerySet: A queryset of notifications for the user.
        """
        notifications = get_notifications_by_user(user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data

    @staticmethod
    def generate_user_report(user_id):
        """
        Generate a notification report for a specific user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - dict: The user notification report.
        """
        return generate_user_notification_report(user_id)

    @staticmethod
    def generate_summary_report():
        """
        Generate a summary report of notifications.

        Returns:
        - dict: The notification summary report.
        """
        return generate_notification_summary()

    @staticmethod
    def update_notification_settings(user_id, settings_data):
        """
        Update notification settings for a user.

        Args:
        - user_id (int): ID of the user.
        - settings_data (dict): Dictionary containing the settings to update.

        Returns:
        - dict: The updated settings.
        """
        settings, created = NotificationSettings.objects.get_or_create(user_id=user_id)
        serializer = NotificationSettingsSerializer(settings, data=settings_data)
        if serializer.is_valid():
            updated_settings = serializer.save()
            return updated_settings
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def get_notification_settings(user_id):
        """
        Get notification settings for a user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - dict: The user's notification settings.
        """
        settings = NotificationSettings.objects.get(user_id=user_id)
        serializer = NotificationSettingsSerializer(settings)
        return serializer.data