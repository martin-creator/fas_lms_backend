# notifications/utils/delivery_method.py

import json
import logging
from enum import Enum
from django.core.mail import send_mail
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis

logger = logging.getLogger(__name__)

class DeliveryMethod(Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"
    
    @staticmethod
    def notify(notification):
        method = notification.delivery_method
        if method == DeliveryMethod.EMAIL.name:
            DeliveryMethod.send_email_notification(notification)
        elif method == DeliveryMethod.SMS.name:
            DeliveryMethod.send_sms_notification(notification)
        elif method == DeliveryMethod.PUSH.name:
            DeliveryMethod.send_push_notification(notification)
        elif method == DeliveryMethod.IN_APP.name:
            DeliveryMethod.send_in_app_notification(notification)
            
        redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Adjust settings as needed
        channel_name = 'notifications'
        notification_data = {
            'user': notification.recipient.username,  # Adjust to match your notification structure
            'type': notification.notification_type.type_name,
            'content': notification.decrypt_content(),
            'url': notification.url,
            'timestamp': notification.timestamp.isoformat(),
        }
        redis_client.publish(channel_name, json.dumps(notification_data))

        # Also send to WebSocket if needed
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{notification.recipient.username}",
            {
                'type': 'send_notification',
                'notification': notification_data
            }
        )


    @staticmethod
    def send_email_notification(notification):
        """
        Send an email notification.

        Args:
        - notification (Notification): The notification object containing email details.
        """
        try:
            user_email = notification.recipient.email
            send_mail(
                notification.notification_type.type_name,
                notification.content,
                'no-reply@myapp.com',
                [user_email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {user_email}")
        except Exception as e:
            logger.error(f"Error sending email: {e}")

    @staticmethod
    def send_sms_notification(notification):
        """
        Send an SMS notification.

        Args:
        - notification (Notification): The notification object containing SMS details.
        """
        try:
            user_phone = notification.recipient.phone_number
            # Implement SMS sending logic here
            # Example: sms_client.send_message(user_phone, notification.content)
            logger.info(f"SMS sent to {user_phone}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

    @staticmethod
    def send_push_notification(notification):
        """
        Send a push notification.

        Args:
        - notification (Notification): The notification object containing push details.
        """
        try:
            # Implement push notification sending logic here
            # Example: push_service.send_message(notification.recipient, notification.content)
            logger.info(f"Push notification sent to {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")

    @staticmethod
    def send_in_app_notification(notification):
        """
        Send an in-app notification.

        Args:
        - notification (Notification): The notification object containing in-app details.
        """
        try:
            # Implement in-app notification logic here
            logger.info(f"In-app notification sent to {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending in-app notification: {e}")
