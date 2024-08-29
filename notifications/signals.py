from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    Notification, NotificationLog, NotificationReadStatus, 
    NotificationType, NotificationSettings, NotificationSnooze
)
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from notifications.services.notification_service import NotificationService
from datetime import timedelta, datetime
from django.utils import timezone


User = get_user_model()


# @receiver(post_save, sender=Notification)
# def send_notification(sender, instance, created, **kwargs):
#     if created:
#         data = {
#             'recipient': instance.recipient.id,
#             'notification_type': instance.notification_type,
#             'content': instance.content,
#             'timestamp': instance.timestamp,
#             # Add other relevant fields as necessary
#         }
#         NotificationService.send_notification(data

# Signal to log actions performed on notifications
@receiver(post_save, sender=Notification)
def log_notification_action(sender, instance, created, **kwargs):
    if not created:
        # Fetch the user profile associated with the user who performed the action
        performed_by_profile = UserProfile.objects.get(user=instance.recipient)

        # Create the NotificationLog entry
        NotificationLog.objects.create(
            notification=instance,
            action='updated',
            performed_by=performed_by_profile.user if performed_by_profile else None,
            timestamp=timezone.now()  # Add timestamp or other fields as needed
        )

# Signal to mark notifications as read
@receiver(post_save, sender=Notification)
def mark_notification_as_read(sender, instance, created, **kwargs):
    if not created and instance.is_read:
        instance.read_at = timezone.now()
        instance.save(update_fields=['read_at'])

        # Create or update read status
        read_status, _ = NotificationReadStatus.objects.get_or_create(user=instance.recipient, notification=instance)
        read_status.is_read = True
        read_status.read_at = timezone.now()
        read_status.save(update_fields=['is_read', 'read_at'])

# Signal to create default notification settings for a new user
@receiver(post_save, sender=User)
def create_default_notification_settings(sender, instance, created, **kwargs):
    if created:
        notification_types = NotificationType.objects.all()
        for notification_type in notification_types:
            NotificationSettings.objects.create(user=instance, notification_type=notification_type)

# Signal to update default notification settings when user profile is updated
@receiver(post_save, sender=UserProfile)
def update_notification_settings_on_profile_update(sender, instance, created, **kwargs):
    if not created:
        # Assuming UserProfile has a direct relation to User
        NotificationSettings.objects.filter(user=instance.user).update(channel_preferences=instance.channel_preferences)

# Signal to snooze notifications for a specific period
@receiver(post_save, sender=NotificationSnooze)
def snooze_notifications(sender, instance, created, **kwargs):
    if created:
        start_time = instance.start_time
        end_time = instance.end_time
        notifications = Notification.objects.filter(recipient=instance.user, timestamp__range=(start_time, end_time))
        for notification in notifications:
            notification.timestamp += timedelta(days=7)
            notification.save(update_fields=['timestamp'])

# Signal to delete related logs when a notification is deleted
@receiver(post_delete, sender=Notification)
def delete_notification_logs(sender, instance, **kwargs):
    NotificationLog.objects.filter(notification=instance).delete()

# Additional signals can be added here as needed for specific application requirements
