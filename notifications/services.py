# notifications/services.py
from django.contrib.contenttypes.models import ContentType
from .models import Notification, NotificationType, NotificationSettings, NotificationReadStatus
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django_rq
from .tasks import send_email_notification, send_push_notification

class NotificationService:
    @staticmethod
    def create_notification(recipient, content, notification_type_name, url, content_object, priority=0):
        notification_type, created = NotificationType.objects.get_or_create(type_name=notification_type_name)
        content_type = ContentType.objects.get_for_model(content_object)

        if not NotificationService.is_notification_enabled(recipient, notification_type):
            return None

        notification = Notification.objects.create(
            recipient=recipient,
            content=content,
            notification_type=notification_type,
            url=url,
            content_object=content_object,
            content_type=content_type,
            object_id=content_object.id,
            priority=priority,
        )
        NotificationService.send_notification(notification)
        return notification

    @staticmethod
    def send_notification(notification):
        # Asynchronous task dispatch
        django_rq.enqueue(send_email_notification, notification.id)
        django_rq.enqueue(send_push_notification, notification.id)
        NotificationService.send_websocket_notification(notification)

    @staticmethod
    def send_websocket_notification(notification):
        channel_layer = get_channel_layer()
        group_name = f"notifications_{notification.recipient.username}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'send_notification',
                'notification': {
                    'type': notification.notification_type.type_name,
                    'content': notification.content,
                    'url': notification.url,
                    'timestamp': str(notification.timestamp),
                }
            }
        )

    @staticmethod
    def mark_as_read(notification, user):
        read_status, created = NotificationReadStatus.objects.get_or_create(
            notification=notification,
            user=user
        )
        if not read_status.is_read:
            read_status.is_read = True
            read_status.read_at = timezone.now()
            read_status.save()

    @staticmethod
    def mark_all_as_read(user):
        unread_notifications = Notification.objects.filter(recipient=user, is_read=False)
        for notification in unread_notifications:
            NotificationService.mark_as_read(notification, user)

    @staticmethod
    def get_unread_notifications(user):
        return Notification.objects.filter(recipient=user, is_read=False)

    @staticmethod
    def create_default_notification_settings(user):
        default_settings = NotificationType.objects.all()
        for notification_type in default_settings:
            NotificationSettings.objects.get_or_create(
                user=user,
                notification_type=notification_type,
                defaults={'is_enabled': True}
            )

    @staticmethod
    def update_notification_settings(user, notification_type_name, is_enabled, channel_preferences=None):
        notification_type, created = NotificationType.objects.get_or_create(type_name=notification_type_name)
        settings, created = NotificationSettings.objects.get_or_create(
            user=user,
            notification_type=notification_type,
            defaults={'is_enabled': is_enabled, 'channel_preferences': channel_preferences or {}}
        )
        settings.is_enabled = is_enabled
        if channel_preferences:
            settings.channel_preferences = channel_preferences
        settings.save()

    @staticmethod
    def is_notification_enabled(user, notification_type):
        try:
            setting = NotificationSettings.objects.get(user=user, notification_type=notification_type)
            return setting.is_enabled
        except NotificationSettings.DoesNotExist:
            return True

    @staticmethod
    def get_notifications(user, limit=10):
        return Notification.objects.filter(recipient=user).order_by('-timestamp')[:limit]
