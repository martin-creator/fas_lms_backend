import redis
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django_rq
from django.core.mail import send_mail
import logging
from .models import Notification

# Set up logger
logger = logging.getLogger(__name__)

class PubSubService:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def publish_notification(self, channel, message):
        """
        Publish a notification to a Redis channel.

        Args:
        - channel (str): The channel to publish to.
        - message (dict): The message to publish.
        """
        try:
            self.redis_client.publish(channel, json.dumps(message))
            logger.info(f"Notification published to channel {channel}: {message}")
        except Exception as e:
            logger.error(f"Error publishing notification to channel {channel}: {e}")

    @staticmethod
    def send_notification(notification):
        """
        Send a notification through various channels.

        Args:
        - notification (Notification): The notification object.
        """
        try:
            django_rq.enqueue(PubSubService.send_email_notification, notification)
            django_rq.enqueue(PubSubService.send_sms_notification, notification)
            django_rq.enqueue(PubSubService.send_push_notification, notification.id)
            PubSubService.send_in_app_notification(notification)
        except Exception as e:
            logger.error(f"Error dispatching notification: {e}")

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
    def send_push_notification(notification_id):
        """
        Send a push notification.

        Args:
        - notification_id (int): The ID of the notification.
        """
        try:
            # Implement push notification logic here
            logger.info(f"Push notification sent for notification ID: {notification_id}")
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")

    @staticmethod
    def send_websocket_notification(notification):
        """
        Send a WebSocket notification.

        Args:
        - notification (Notification): The notification object.
        """
        try:
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
            logger.info(f"WebSocket notification sent to {group_name}")
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")

    @staticmethod
    def send_in_app_notification(notification):
        """
        Send an in-app notification by saving it to the database and triggering a WebSocket notification.

        Args:
        - notification (Notification): The notification object.
        """
        try:
            notification = Notification.objects.create(
                recipient=notification.recipient,
                notification_type=notification.notification_type,
                content=notification.content,
                url=notification.url,
                timestamp=notification.timestamp,
            )
            # Trigger WebSocket notification after saving to the database
            PubSubService.send_websocket_notification(notification)
            logger.info(f"In-app notification saved and WebSocket notification triggered for {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending in-app notification: {e}")