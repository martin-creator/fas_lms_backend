# notifications/tasks.py
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification, NotificationReadStatus, NotificationLog
from profiles.models import UserProfile
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
from django.utils import timezone
import logging

# Set up logging
logger = logging.getLogger(__name__)

def send_email_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        send_mail(
            subject='New Notification',
            message=notification.content,
            from_email='noreply@example.com',
            recipient_list=[notification.recipient.email],
        )
    except ObjectDoesNotExist:
        logger.error(f"Notification with ID {notification_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send email notification: {e}")


@shared_task
def send_notification_task(notification_id):
    """
    Task to send a notification asynchronously.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        # Perform notification sending logic here (replace with actual implementation)
        # Example:
        notification_sent = f"Notification sent to {notification.recipient.username}"
        print(notification_sent)
    except Notification.DoesNotExist:
        # Handle case where notification doesn't exist
        pass
    except Exception as e:
        # Handle any other exceptions
        pass


@shared_task
def log_notification_action_task(notification_id, action):
    """
    Task to log a notification action asynchronously.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        # Fetch the user profile associated with the recipient
        performed_by_profile = UserProfile.objects.get(user=notification.recipient)
        
        # Create a notification log entry
        NotificationLog.objects.create(
            notification=notification,
            action=action,
            performed_by=performed_by_profile.user if performed_by_profile else None,
            timestamp=timezone.now()
        )
    except Notification.DoesNotExist:
        # Handle case where notification doesn't exist
        pass
    except UserProfile.DoesNotExist:
        # Handle case where user profile doesn't exist
        pass
    except Exception as e:
        # Handle any other exceptions
        pass


@shared_task
def archive_old_notifications_task():
    """
    Task to archive old notifications that are no longer needed.
    """
    threshold_date = timezone.now() - timezone.timedelta(days=365)  # Example: 1 year retention
    Notification.objects.filter(timestamp__lt=threshold_date).update(is_archived=True)


@shared_task
def send_bulk_notifications(user_ids, notification_data):
    """
    Task to send bulk notifications to multiple users asynchronously.
    
    Args:
    - user_ids (list): List of user IDs to send notifications to.
    - notification_data (dict): Dictionary containing notification data.
      Example: {'content': 'Notification content', 'notification_type': 'type_name', ...}
    """
    try:
        # Fetch user profiles for the given user IDs
        user_profiles = UserProfile.objects.filter(user_id__in=user_ids)
        
        # Create and send notifications to each user
        for profile in user_profiles:
            notification_data['recipient'] = profile.user
            Notification.objects.create(**notification_data)
        
        # Optionally, trigger the actual sending of notifications here
        # Depending on your application's design, you might send notifications directly or queue another task
        
    except Exception as e:
        # Handle any exceptions
        pass


@shared_task
def mark_notifications_as_read_task(user_id, notification_ids):
    """
    Task to mark notifications as read for a specific user asynchronously.
    
    Args:
    - user_id (int): ID of the user whose notifications are to be marked as read.
    - notification_ids (list): List of notification IDs to mark as read.
    """
    try:
        notifications = Notification.objects.filter(id__in=notification_ids, recipient_id=user_id)
        notifications.update(is_read=True, read_at=timezone.now())
        
        # Optionally, update read status in NotificationReadStatus model
        for notification in notifications:
            NotificationReadStatus.objects.update_or_create(
                user_id=user_id,
                notification_id=notification.id,
                defaults={'is_read': True, 'read_at': timezone.now()}
            )
        
    except Exception as e:
        # Handle any exceptions
        pass


# Additional tasks can be added as needed for specific notification-related operations.