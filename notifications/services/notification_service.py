# notifications/services/notification_service.py
import logging
import random
from django.utils import timezone
from django.core.mail import send_mail
from notifications.models import (
    Notification, NotificationType, NotificationTemplate, NotificationSettings, 
    NotificationReadStatus, NotificationLog, NotificationEngagement, NotificationSnooze,
    UserNotificationPreference,
)
from notifications.serializers import (
    NotificationSerializer, NotificationTypeSerializer,
    NotificationTemplateSerializer, NotificationSettingsSerializer,
    NotificationReadStatusSerializer, UserNotificationPreferenceSerializer,
    NotificationSnoozeSerializer, NotificationEngagementSerializer,
    NotificationABTestSerializer
)
from django.utils.translation import activate, gettext as _
from django.core.exceptions import PermissionDenied
from notifications.tasks import send_bulk_notifications
from django.core.cache import cache
from notifications.metrics import increment_notifications_sent, increment_notifications_failed
from .pubsub_service import PubSubService
from .crm_integration import send_crm_alert
from .alert_system_integration import send_external_alert
from notifications.settings.config.constances import NOTIFICATION_CHANNELS
from notifications.utils.delivery_method import DeliveryMethod
from notifications.utils.permissions import PermissionChecker
from notifications.utils.notification_utils import send_notification
from notifications.utils.notification_utils import NotificationUtils

logger = logging.getLogger(__name__)

class NotificationService:
    """
    Service for managing notifications within the application.
    """

    @staticmethod
    def send_notification_service(data):
        """
        Send a notification service to a user.

        Args:
            data (dict): Data for creating the notification.

        Returns:
            Notification: The created Notification object.

        Raises:
            PermissionDenied: If the user does not have permission to send notifications.
            ValueError: If the notification data is invalid.
            Exception: If sending the notification fails.
        """
        return NotificationUtils.send_notification(data)

    @staticmethod
    def mark_notification_as_read(notification_id):
        """
        Mark a notification as read.

        Args:
            notification_id (int): ID of the notification to mark as read.
        """
        NotificationUtils.mark_notification_as_read(notification_id)

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete a notification.

        Args:
            notification_id (int): ID of the notification to delete.
        """
        NotificationUtils.delete_notification(notification_id)

    @staticmethod
    def get_notification(notification_id):
        """
        Retrieve a specific notification by its ID.

        Args:
            notification_id (int): ID of the notification to retrieve.

        Returns:
            dict: Serialized data of the notification.
        """
        return NotificationUtils.get_notification(notification_id)

    @staticmethod
    def update_notification(notification_id, data):
        """
        Update a notification.

        Args:
            notification_id (int): ID of the notification to update.
            data (dict): Updated data for the notification.

        Returns:
            dict: Serialized data of the updated notification.
        """
        return NotificationUtils.update_notification(notification_id, data)

    @staticmethod
    def get_user_notifications(user_id):
        """
        Get all notifications for a specific user.

        Args:
            user_id (int): ID of the user to retrieve notifications for.

        Returns:
            QuerySet: A queryset of notifications for the user.
        """
        return NotificationUtils.get_user_notifications(user_id)

    @staticmethod
    def generate_user_report(user_id):
        """
        Generate a notification report for a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            dict: The user notification report.
        """
        return NotificationUtils.generate_user_report(user_id)

    @staticmethod
    def generate_summary_report():
        """
        Generate a summary report of notifications.

        Returns:
            dict: The notification summary report.
        """
        return NotificationUtils.generate_summary_report()

    @staticmethod
    def update_notification_settings(user_id, settings_data):
        """
        Update notification settings for a user.

        Args:
            user_id (int): ID of the user.
            settings_data (dict): Data for updating the settings.

        Returns:
            dict: Serialized data of the updated settings.
        """
        return NotificationUtils.update_notification_settings(user_id, settings_data)

    @staticmethod
    def get_notification_settings(user_id):
        """
        Retrieve notification settings for a user.

        Args:
            user_id (int): ID of the user.

        Returns:
            dict: Serialized data of the notification settings.
        """
        return NotificationUtils.get_notification_settings(user_id)

    @staticmethod
    def get_unread_notifications_count(user):
        """
        Get the count of unread notifications for a user.

        Args:
            user (UserProfile): The user to get the unread count for.

        Returns:
            dict: The count of unread notifications.
        """
        return NotificationUtils.get_unread_notifications_count(user)

    @staticmethod
    def create_notification_template(notification_type, template):
        """
        Create a notification template.

        Args:
            notification_type (NotificationType): The type of notification.
            template (str): The template content.

        Returns:
            dict: Serialized data of the created template.
        """
        return NotificationUtils.create_notification_template(notification_type, template)

    @staticmethod
    def update_notification_template(template_id, data):
        """
        Update a notification template.

        Args:
            template_id (int): ID of the template to update.
            data (dict): Updated data for the template.

        Returns:
            dict: Serialized data of the updated template.
        """
        return NotificationUtils.update_notification_template(template_id, data)

    @staticmethod
    def get_notification_template(notification_type):
        """
        Retrieve a notification template by type.

        Args:
            notification_type (NotificationType): The type of notification.

        Returns:
            dict: Serialized data of the template.
        """
        return NotificationUtils.get_notification_template(notification_type)

    @staticmethod
    def get_notification_types():
        """
        Retrieve all notification types.

        Returns:
            dict: Serialized data of all notification types.
        """
        return NotificationUtils.get_notification_types()

    @staticmethod
    def create_notification_type(data):
        """
        Create a notification type.

        Args:
            data (dict): Data for the new notification type.

        Returns:
            dict: Serialized data of the created notification type.
        """
        return NotificationUtils.create_notification_type(data)

    @staticmethod
    def update_notification_type(notification_type_id, data):
        """
        Update a notification type.

        Args:
            notification_type_id (int): ID of the notification type to update.
            data (dict): Updated data for the notification type.

        Returns:
            dict: Serialized data of the updated notification type.
        """
        return NotificationUtils.update_notification_type(notification_type_id, data)

    @staticmethod
    def delete_notification_type(notification_type_id):
        """
        Delete a notification type.

        Args:
            notification_type_id (int): ID of the notification type to delete.
        """
        NotificationUtils.delete_notification_type(notification_type_id)

    @staticmethod
    def subscribe_to_notifications(user, notification_types):
        """
        Subscribe a user to specific notification types.

        Args:
            user (UserProfile): The user to subscribe.
            notification_types (list): List of notification types to subscribe to.

        Returns:
            list: Serialized data of the subscribed settings.
        """
        return NotificationUtils.subscribe_to_notifications(user, notification_types)

    @staticmethod
    def unsubscribe_from_notifications(user, notification_types):
        """
        Unsubscribe a user from specific notification types.

        Args:
            user (UserProfile): The user to unsubscribe.
            notification_types (list): List of notification types to unsubscribe from.

        Returns:
            list: Serialized data of the unsubscribed settings.
        """
        return NotificationUtils.unsubscribe_from_notifications(user, notification_types)

    @staticmethod
    def notify_followers(user_profile, notification_type, content_object=None, content='', url=''):
        """
        Notify all followers of a user.

        Args:
            user_profile (UserProfile): The user whose followers will be notified.
            notification_type (NotificationType): The type of notification.
            content_object (Object, optional): The object related to the notification.
            content (str, optional): The content of the notification.
            url (str, optional): The URL associated with the notification.

        Returns:
            list: Serialized data of the notifications.
        """
        return NotificationUtils.notify_followers(user_profile, notification_type, content_object, content, url)

    @staticmethod
    def notify_all_users(notification_type, content_object=None, content='', url=''):
        """
        Notify all users.

        Args:
            notification_type (NotificationType): The type of notification.
            content_object (Object, optional): The object related to the notification.
            content (str, optional): The content of the notification.
            url (str, optional): The URL associated with the notification.

        Returns:
            list: Serialized data of the notifications.
        """
        return NotificationUtils.notify_all_users(notification_type, content_object, content, url)

    @staticmethod
    def get_user_preferences(user):
        """
        Retrieve notification preferences for a user.

        Args:
            user (UserProfile): The user to retrieve preferences for.

        Returns:
            dict: Serialized data of the user's preferences.
        """
        return NotificationUtils.get_user_preferences(user)

    @staticmethod
    def update_user_preferences(user, preferences_data):
        """
        Update notification preferences for a user.

        Args:
            user (UserProfile): The user to update preferences for.
            preferences_data (dict): Data for updating the preferences.

        Returns:
            dict: Serialized data of the updated preferences.
        """
        return NotificationUtils.update_user_preferences(user, preferences_data)

    @staticmethod
    def snooze_notifications(user, start_time, end_time):
        """
        Snooze notifications for a user.

        Args:
            user (UserProfile): The user to snooze notifications for.
            start_time (datetime): The start time of the snooze period.
            end_time (datetime): The end time of the snooze period.
        """
        NotificationUtils.snooze_notifications(user, start_time, end_time)

    @staticmethod
    def snooze_notification(notification_id, snooze_until):
        """
        Snooze a specific notification.

        Args:
            notification_id (int): ID of the notification to snooze.
            snooze_until (datetime): The time until which to snooze the notification.
        """
        NotificationUtils.snooze_notification(notification_id, snooze_until)

    @staticmethod
    def is_user_snoozed(user):
        """
        Check if a user has snoozed notifications.

        Args:
            user (UserProfile): The user to check.

        Returns:
            bool: True if the user has snoozed notifications, False otherwise.
        """
        return NotificationUtils.is_user_snoozed(user)

    @staticmethod
    def get_snoozed_notifications(user):
        """
        Retrieve snoozed notifications for a user.

        Args:
            user (UserProfile): The user to retrieve snoozed notifications for.

        Returns:
            list: Serialized data of the snoozed notifications.
        """
        return NotificationUtils.get_snoozed_notifications(user)

    @staticmethod
    def log_notification_engagement(notification_id, engagement_type):
        """
        Log engagement for a notification.

        Args:
            notification_id (int): ID of the notification to log engagement for.
            engagement_type (str): Type of engagement to log.

        Returns:
            NotificationLog: The created log entry.
        """
        return NotificationUtils.log_notification_engagement(notification_id, engagement_type)

    @staticmethod
    def record_engagement(notification_id, engagement_type):
        """
        Record engagement for a notification.

        Args:
            notification_id (int): ID of the notification to record engagement for.
            engagement_type (str): Type of engagement to record.

        Returns:
            NotificationLog: The created log entry.
        """
        return NotificationUtils.record_engagement(notification_id, engagement_type)

    @staticmethod
    def log_notification_event(notification_id, event_type):
        """
        Log an event for a notification.

        Args:
            notification_id (int): ID of the notification to log the event for.
            event_type (str): Type of event to log.

        Returns:
            NotificationLog: The created log entry.
        """
        return NotificationUtils.log_notification_event(notification_id, event_type)

    @staticmethod
    def assign_user_to_test(user_id, test_name):
        """
        Assign a user to an A/B test group.

        Args:
            user_id (int): ID of the user.
            test_name (str): Name of the A/B test.

        Returns:
            str: The test group assigned to the user.
        """
        return NotificationUtils.assign_user_to_test(user_id, test_name)

    @staticmethod
    def analyze_ab_test_results(test_name):
        """
        Analyze the results of an A/B test.

        Args:
            test_name (str): Name of the A/B test.

        Returns:
            dict: The results of the A/B test analysis.
        """
        return NotificationUtils.analyze_ab_test_results(test_name)

    @staticmethod
    def send_test_notification(data):
        """
        Send a test notification.

        Args:
            data (dict): Data for creating the test notification.
        """
        return NotificationUtils.send_test_notification(data)

    @staticmethod
    def send_test_multi_notification(data):
        """
        Send a test multi-notification.

        Args:
            data (dict): Data for creating the test multi-notification.
        """
        return NotificationUtils.send_test_multi_notification(data)
