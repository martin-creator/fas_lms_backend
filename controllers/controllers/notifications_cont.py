from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from notifications.models import Notification, NotificationTemplate, NotificationSettings, NotificationReadStatus, NotificationType
from activity.models import Reaction, Share
from profiles.models import UserProfile
from django.core.mail import send_mail

class NotificationServicesController:
    def __init__(self):
        pass

    def create_notification(self, recipient, notification_type, content_object=None, content='', url='', priority=0):
        """
        Creates a new notification for a recipient.
        """
        notification = Notification.objects.create(
            recipient=recipient,
            content_type=content_object.content_type if content_object else None,
            object_id=content_object.id if content_object else None,
            content_object=content_object,
            content=content,
            url=url,
            notification_type=notification_type,
            priority=priority
        )
        self.send_notification(notification)
        return notification

    def send_notification(self, notification):
        """
        Sends notifications based on the delivery preferences of the recipient.
        """
        recipient = notification.recipient
        if self.is_notification_enabled(recipient, notification.notification_type):
            # Example: Implement sending logic (e.g., email, in-app notification, push notification)
            if notification.notification_type.type_name == 'message':
                # Example: Send email notification for messages
                send_mail(
                    f'New Message from {notification.sender.username}',
                    notification.content,
                    settings.EMAIL_HOST_USER,
                    [recipient.email],
                    fail_silently=False,
                )
            elif notification.notification_type.type_name == 'post':
                # Example: Send in-app notification for new posts
                pass  # Implement in-app notification logic
            elif notification.notification_type.type_name == 'reaction':
                # Example: Send push notification for reactions
                pass  # Implement push notification logic
            # Add more cases as needed

    def is_notification_enabled(self, user, notification_type):
        """
        Checks if a specific notification type is enabled for a user.
        """
        try:
            settings = NotificationSettings.objects.get(user=user, notification_type=notification_type)
            return settings.is_enabled
        except NotificationSettings.DoesNotExist:
            return False

    def mark_notification_as_read(self, user, notification_id):
        """
        Marks a notification as read for a user.
        """
        notification = get_object_or_404(Notification, id=notification_id)
        read_status, created = NotificationReadStatus.objects.get_or_create(user=user, notification=notification)
        read_status.is_read = True
        read_status.read_at = timezone.now()
        read_status.save()
        return read_status

    def get_notifications(self, user, limit=10):
        """
        Retrieves notifications for a user.
        """
        return Notification.objects.filter(recipient=user).order_by('-timestamp')[:limit]

    def get_unread_notifications_count(self, user):
        """
        Retrieves the count of unread notifications for a user.
        """
        return Notification.objects.filter(recipient=user, is_read=False).count()

    def create_notification_template(self, notification_type, template):
        """
        Creates or updates a notification template for a notification type.
        """
        template_obj, created = NotificationTemplate.objects.get_or_create(notification_type=notification_type)
        template_obj.template = template
        template_obj.save()
        return template_obj

    def get_notification_template(self, notification_type):
        """
        Retrieves the notification template for a notification type.
        """
        try:
            template = NotificationTemplate.objects.get(notification_type=notification_type)
            return template.template
        except NotificationTemplate.DoesNotExist:
            return None

    def get_notification_types(self):
        """
        Retrieves all notification types available in the system.
        """
        return NotificationType.objects.all()

    def subscribe_to_notifications(self, user, notification_types):
        """
        Subscribes a user to receive notifications of specific types.
        """
        for notification_type in notification_types:
            NotificationSettings.objects.get_or_create(user=user, notification_type=notification_type, is_enabled=True)

    def unsubscribe_from_notifications(self, user, notification_types):
        """
        Unsubscribes a user from receiving notifications of specific types.
        """
        NotificationSettings.objects.filter(user=user, notification_type__in=notification_types).delete()

    def notify_followers(self, user_profile, notification_type, content_object=None, content='', url=''):
        """
        Notifies followers of a user profile about an action.
        """
        followers = user_profile.followers.all()
        for follower in followers:
            self.create_notification(follower, notification_type, content_object, content, url)

    def notify_all_users(self, notification_type, content_object=None, content='', url=''):
        """
        Notifies all users about an action.
        """
        all_users = UserProfile.objects.all()
        for user in all_users:
            self.create_notification(user, notification_type, content_object, content, url)

    def delete_notification(self, notification_id):
        """
        Deletes a notification.
        """
        Notification.objects.filter(id=notification_id).delete()
        return True
