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
from profiles.models import UserProfile
from notifications.reports.notification_report import (
    generate_user_notification_report,
    generate_notification_summary
)
from notifications.querying.notification_query import (
    get_notifications_by_user,
    search_notifications
)
from notifications.utils import (
    format_notification_content,
    # validate_notification_data,
    process_notification_data
)
from notifications.helpers.notification_helpers import (
    process_notification_data,
    validate_notification_permissions,
    send_push_notification
)
# from notifications.settings import (
#     get_notification_settings,
#     update_notification_settings
# )
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
        return send_notification(data)

                
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
    def get_notification(notification_id):
        """
        Retrieve a specific notification by its ID.

        Args:
        - notification_id (int): ID of the notification to retrieve.

        Returns:
        - dict: Serialized data of the notification.
        """
        notification = Notification.objects.get(id=notification_id)
        serializer = NotificationSerializer(notification)
        return serializer.data

    @staticmethod
    def update_notification(notification_id, data):
        """
        Update a notification.

        Args:
        - notification_id (int): ID of the notification to update.
        - data (dict): Updated data for the notification.

        Returns:
        - dict: Serialized data of the updated notification.
        """
        notification = Notification.objects.get(id=notification_id)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            updated_notification = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

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
            cache_key = f"notification_settings_{user_id}"
            cache.set(cache_key, updated_settings, timeout=3600)
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
        cache_key = f"notification_settings_{user_id}"
        settings = cache.get(cache_key)
        if not settings:
            settings = NotificationSettings.objects.get(user_id=user_id)
            cache.set(cache_key, settings, timeout=3600)
        return settings
        
    @staticmethod
    def get_unread_notifications_count(user):
        """
        Retrieves the count of unread notifications for a user.
    
        Args:
        - user (User): The user for whom to count unread notifications.
    
        Returns:
        - dict: A dictionary containing the count of unread notifications.
        """
        count = Notification.objects.filter(recipient=user, is_read=False).count()
        return {'unread_count': count}
        
    @staticmethod
    def create_notification_template(notification_type, template):
        """
        Creates or updates a notification template for a notification type.
    
        Args:
        - notification_type (NotificationType): The notification type for which to create/update the template.
        - template (str): The template content.
    
        Returns:
        - dict: Serialized data of the created or updated NotificationTemplate object.
        """
        template_obj, created = NotificationTemplate.objects.get_or_create(notification_type=notification_type)
        template_obj.template = template
        template_obj.save()
        
        serializer = NotificationTemplateSerializer(template_obj)
        return serializer.data
    
    @staticmethod
    def update_notification_template(template_id, data):
        """
        Update a notification template.

        Args:
            template_id (int): ID of the template to update.
            data (dict): Updated data for the template.

        Returns:
            dict: Serialized data of the updated template.

        Raises:
            ValueError: If the template data is invalid.
        """
        template = NotificationTemplate.objects.get(id=template_id)
        serializer = NotificationTemplateSerializer(template, data=data)
        if serializer.is_valid():
            updated_template = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)
        
    @staticmethod
    def get_notification_template(notification_type):
        """
        Retrieves the notification template for a notification type.
    
        Args:
        - notification_type (NotificationType): The notification type for which to retrieve the template.
    
        Returns:
        - dict: Serialized data of the notification template, or None if not found.
        """
        try:
            template = NotificationTemplate.objects.get(notification_type=notification_type)
            serializer = NotificationTemplateSerializer(template)
            return serializer.data
        except NotificationTemplate.DoesNotExist:
            return None
            
    @staticmethod
    def get_notification_types():
        """
        Retrieves all notification types available in the system.
    
        Returns:
        - list: A list of serialized NotificationType objects.
        """
        notification_types = NotificationType.objects.all()
        serializer = NotificationTypeSerializer(notification_types, many=True)
        return serializer.data
        
    @staticmethod
    def create_notification_type(data):
        """
        Create a new notification type.

        Args:
            data (dict): Data for the new notification type.

        Returns:
            NotificationType: The created NotificationType object.

        Raises:
            ValueError: If the notification type data is invalid.
        """
        serializer = NotificationTypeSerializer(data=data)
        if serializer.is_valid():
            notification_type = serializer.save()
            return notification_type
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def update_notification_type(notification_type_id, data):
        """
        Update a notification type.

        Args:
            notification_type_id (int): ID of the notification type to update.
            data (dict): Updated data for the notification type.

        Returns:
            dict: Serialized data of the updated notification type.

        Raises:
            ValueError: If the notification type data is invalid.
        """
        notification_type = NotificationType.objects.get(id=notification_type_id)
        serializer = NotificationTypeSerializer(notification_type, data=data)
        if serializer.is_valid():
            updated_notification_type = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def delete_notification_type(notification_type_id):
        """
        Delete a notification type.

        Args:
            notification_type_id (int): ID of the notification type to delete.
        """
        NotificationType.objects.filter(id=notification_type_id).delete()

    @staticmethod
    def subscribe_to_notifications(user, notification_types):
        """
        Subscribes a user to receive notifications of specific types.
    
        Args:
        - user (User): The user to subscribe.
        - notification_types (list): A list of NotificationType objects to subscribe to.
    
        Returns:
        - list: A list of serialized NotificationSettings objects.
        """
        subscribed_settings = []
        for notification_type in notification_types:
            setting, created = NotificationSettings.objects.get_or_create(user=user, notification_type=notification_type, defaults={'is_enabled': True})
            serializer = NotificationSettingsSerializer(setting)
            subscribed_settings.append(serializer.data)
        return subscribed_settings
        
    @staticmethod
    def unsubscribe_from_notifications(user, notification_types):
        """
        Unsubscribes a user from receiving notifications of specific types.
    
        Args:
        - user (User): The user to unsubscribe.
        - notification_types (list): A list of NotificationType objects to unsubscribe from.
    
        Returns:
        - list: A list of serialized NotificationSettings objects that were deleted.
        """
        settings_to_delete = NotificationSettings.objects.filter(user=user, notification_type__in=notification_types)
        serialized_settings = NotificationSettingsSerializer(settings_to_delete, many=True).data
        settings_to_delete.delete()
        return serialized_settings
        
    @staticmethod
    def notify_followers(user_profile, notification_type, content_object=None, content='', url=''):
        """
        Notifies followers of a user profile about an action.
    
        Args:
        - user_profile (UserProfile): The user profile whose followers are to be notified.
        - notification_type (NotificationType): The type of notification to create.
        - content_object (Model): The content object related to the notification.
        - content (str): The notification content.
        - url (str): The URL related to the notification.
    
        Returns:
        - list: A list of serialized Notification objects.
        """
        followers = user_profile.followers.all()
        notifications = []
        for follower in followers:
            notification_data = {
                'recipient': follower.id,
                'notification_type': notification_type.id,
                'content_object': content_object.id if content_object else None,
                'content': content,
                'url': url,
                'is_read': False
            }
            serializer = NotificationSerializer(data=notification_data)
            if serializer.is_valid():
                notification = serializer.save()
                notifications.append(serializer.data)
            else:
                raise ValueError(serializer.errors)
        return notifications
        
    @staticmethod
    def notify_all_users(notification_type, content_object=None, content='', url=''):
        """
        Notifies all users about an action.
    
        Args:
        - notification_type (NotificationType): The type of notification to create.
        - content_object (Model): The content object related to the notification.
        - content (str): The notification content.
        - url (str): The URL related to the notification.
    
        Returns:
        - list: A list of serialized Notification objects.
        """
        all_users = UserProfile.objects.all()
        notifications = []
        for user in all_users:
            notification_data = {
                'recipient': user.id,
                'notification_type': notification_type.id,
                'content_object': content_object.id if content_object else None,
                'content': content,
                'url': url,
                'is_read': False
            }
            serializer = NotificationSerializer(data=notification_data)
            if serializer.is_valid():
                notification = serializer.save()
                notifications.append(serializer.data)
            else:
                raise ValueError(serializer.errors)
        return notifications
        
    @staticmethod
    def get_user_preferences(user):
        preferences = UserNotificationPreference.objects.filter(user=user)
        serializer = UserNotificationPreferenceSerializer(preferences, many=True)
        return serializer.data
        
    @staticmethod
    def update_user_preferences(user, preferences_data):
        for preference in preferences_data:
            pref_obj, created = UserNotificationPreference.objects.update_or_create(
                user=user,
                notification_type=preference['notification_type'],
                defaults={'is_enabled': preference['is_enabled'], 'frequency': preference['frequency']}
            )
        return NotificationService.get_user_preferences(user)
        
    @staticmethod
    def snooze_notifications(user, start_time, end_time):
        NotificationSnooze.objects.create(user=user, start_time=start_time, end_time=end_time)
        
    @staticmethod
    def snooze_notification(notification_id, snooze_until):
        """
        Snooze a notification until a specified time.

        Args:
            notification_id (int): ID of the notification to snooze.
            snooze_until (datetime): The time until which to snooze the notification.
        """
        notification = Notification.objects.get(id=notification_id)
        NotificationSnooze.objects.update_or_create(
            notification=notification,
            defaults={'snooze_until': snooze_until}
        )
    
    @staticmethod
    def is_user_snoozed(user):
        snooze = NotificationSnooze.objects.filter(user=user, start_time__lte=timezone.now(), end_time__gte=timezone.now()).first()
        return snooze is not None
                
    @staticmethod
    def get_snoozed_notifications(user):
        """
        Retrieve all snoozed notifications for a user.

        Args:
            user (User): The user whose snoozed notifications to retrieve.

        Returns:
            list: A list of serialized snoozed notifications.
        """
        snoozed_notifications = NotificationSnooze.objects.filter(
            notification__recipient=user,
            snooze_until__gt=timezone.now()
        ).select_related('notification')
        serializer = NotificationSerializer(
            [snooze.notification for snooze in snoozed_notifications], 
            many=True
        )
        return serializer.data
    
    @staticmethod
    def log_notification_engagement(notification_id, engagement_data):
        """
        Log engagement data for a notification.

        Args:
            notification_id (int): ID of the notification.
            engagement_data (dict): Data about the engagement (e.g., clicks, views).

        Returns:
            NotificationEngagement: The logged NotificationEngagement object.
        """
        notification = Notification.objects.get(id=notification_id)
        engagement, created = NotificationEngagement.objects.update_or_create(
            notification=notification,
            defaults=engagement_data
        )
        return engagement

    @staticmethod
    def record_engagement(notification_id, user_id, action):
        engagement, created = NotificationEngagement.objects.get_or_create(
            notification_id=notification_id,
            user_id=user_id
        )
        if action == 'view':
            engagement.viewed_at = timezone.now()
        elif action == 'click':
            engagement.clicked_at = timezone.now()
        engagement.save()
        
    @staticmethod
    def log_notification_event(notification_id, event_type, event_details):
        """
        Log an event for a notification.

        Args:
            notification_id (int): ID of the notification.
            event_type (str): Type of the event (e.g., sent, read).
            event_details (dict): Additional details about the event.

        Returns:
            NotificationLog: The created NotificationLog object.
        """
        notification = Notification.objects.get(id=notification_id)
        log = NotificationLog.objects.create(
            notification=notification,
            event_type=event_type,
            event_details=event_details
        )
        return log
        
    @staticmethod
    def assign_user_to_test(user):
        return 'variant_a' if random.choice([True, False]) else 'variant_b'

    @staticmethod
    def analyze_ab_test_results(test_name):
        # Implement analysis logic
        pass
            
    @staticmethod
    def send_test_notification(data):
        test_group = assign_user_to_test(data['recipient'])
        template = get_template_for_test_group(test_group)
        send_rich_notification({
            'recipient': data['recipient'],
            'content': template.content,
            'html_content': template.html_content,
            'media_url': template.media_url,
            'delivery_method': data['delivery_method']
        })
        
    @staticmethod
    def send_test_multi_notification(data):
        user = UserProfile.objects.get(id=data['recipient'])
        activate(user.preferred_language)
        data['content'] = _(data['content'])
        data['html_content'] = _(data['html_content'])
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            # Delivery logic
            if data['delivery_method'] == 'push':
                send_push_notification(user, data['content'])
            elif data['delivery_method'] == 'email':
                NotificationService.send_email_notification(user, _("Notification"), data['content'])
            elif data['delivery_method'] == 'sms':
                NotificationService.send_sms_notification(user, data['content'])
            return notification
        else:
            raise ValueError(serializer.errors)
            
    @staticmethod
    def log_notification_action(notification, action, user):
        NotificationLog.objects.create(notification=notification, action=action, performed_by=user)