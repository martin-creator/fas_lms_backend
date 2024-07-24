# notifications/utils/notification_utils.py

import logging
from django.core.exceptions import PermissionDenied
from notifications.models import Notification
from profiles.models import UserProfile
from notifications.serializers import NotificationSerializer
from notifications.utils.delivery_method import DeliveryMethod
from notifications.metrics import increment_notifications_sent, increment_notifications_failed
from notifications.services.pubsub_service import PubSubService
from notifications.services.crm_integration import send_crm_alert
from notifications.services.alert_system_integration import send_external_alert
from notifications.settings.config.constances import NOTIFICATION_CHANNELS
from notifications.utils.permissions import PermissionChecker
from notifications.utils.notification_validation import NotificationsValidator

logger = logging.getLogger(__name__)

def send_notification(data):
    try:
        user = UserProfile.objects.get(id=data['recipient'])
        if not PermissionChecker.user_can_manage_notifications(user):
            raise PermissionDenied("You do not have permission to send notifications.")
        if not NotificationsValidator.validate_notification_permissions(user, data['notification_type']):
            raise PermissionDenied("User does not have permission to receive this notification.")

        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            delivery_method = data.get('delivery_method', DeliveryMethod.PUSH.value)
            delivery_function = getattr(DeliveryMethod, f'send_{delivery_method.lower()}_notification')
            delivery_function(notification)

            if data.get('notify_crm'):
                send_crm_alert(user.id, data['event_type'], data['event_data'])
            if data.get('notify_alert_system'):
                send_external_alert(user.id, data['alert_type'], data['message'])

            PubSubService.publish_notification('notifications', notification.content)
            increment_notifications_sent()
            return notification
        else:
            raise ValueError(serializer.errors)
    except ValueError as e:
        increment_notifications_failed()
        logger.error(f"Validation error: {e}")
        NotificationsValidator.handle_notification_failure(data, str(e))
        raise
    except PermissionDenied as e:
        logger.error(f"Permission error: {e}")
        raise
    except Exception as e:
        increment_notifications_failed()
        logger.error(f"Unexpected error: {e}")
        NotificationsValidator.handle_notification_failure(data, str(e))
        raise
