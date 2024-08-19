from celery import shared_task

from notifications.models import NotificationType
from .models import UserActivity
import logging

logger = logging.getLogger(__name__)

@shared_task
def create_user_activity_task(user_id, activity_type, details):
    try:
        UserActivity.objects.create(
            user_id=user_id,
            activity_type=activity_type,
            details=details
        )
    except Exception as e:
        logger.error(f"Error creating user activity: {e}")

@shared_task
def create_notification_task(recipient_id, content, notification_type_id, url):
    from notifications.utils.notification_utils import NotificationUtils
    try:
        notification_type = NotificationType.objects.get(id=notification_type_id)
        NotificationUtils.create_notification(
            recipient_id=recipient_id,
            content=content,
            notification_type=notification_type,
            url=url
        )
    except NotificationType.DoesNotExist:
        logger.error(f"NotificationType with ID {notification_type_id} does not exist.")
    except Exception as e:
        logger.error(f"Error creating notification: {e}")
