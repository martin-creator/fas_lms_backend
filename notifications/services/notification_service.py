# notifications/services/notification_service.py

from django.utils import timezone
from notifications.models import Notification, NotificationType, NotificationTemplate, NotificationSettings, NotificationReadStatus
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
    validate_notification_data,
    process_notification_data
)
from notifications.helpers.notification_helpers import (
    process_notification_data,
    validate_notification_permissions,
    send_push_notification
)
from notifications.settings import (
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