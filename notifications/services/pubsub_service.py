# notifications/utils/pubsub_service.py

import redis
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import django_rq
from django.core.mail import send_mail
import logging
from .models import Notification

logger = logging.getLogger(__name__)

class PubSubService:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def publish_notification(self, channel, notification):
        """
        Publish the notification to a Redis channel.

        Args:
        - channel (str): The Redis channel name.
        - notification (Notification): The notification object.
        """
        try:
            notification_data = {
                'user': notification.recipient.username,
                'type': notification.notification_type.type_name,
                'content': notification.decrypt_content(),
                'url': notification.url,
                'timestamp': notification.timestamp.isoformat(),
            }
            self.redis_client.publish(channel, json.dumps(notification_data))
            logger.info(f"Notification published to Redis channel {channel}")
        except Exception as e:
            logger.error(f"Error publishing to Redis: {e}")

    @staticmethod
    def send_websocket_notification(notification):
        """
        Send a WebSocket notification.

        Args:
        - notification (Notification): The notification object.
        """
        try:
            channel_layer = get_channel_layer()
            notification_data = {
                'type': notification.notification_type.type_name,
                'content': notification.decrypt_content(),
                'url': notification.url,
                'timestamp': notification.timestamp.isoformat(),
            }
            async_to_sync(channel_layer.group_send)(
                f"notifications_{notification.recipient.username}",
                {
                    'type': 'send_notification',
                    'notification': notification_data
                }
            )
            logger.info(f"WebSocket notification sent to notifications_{notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending WebSocket notification: {e}")

    @staticmethod
    def send_notification(notification):
        """
        Send a notification through various channels.

        Args:
        - notification (Notification): The notification object.
        """
        try:
            # Enqueue email, SMS, and push notification tasks to be processed asynchronously
            django_rq.enqueue(PubSubService.send_email_notification, notification)
            django_rq.enqueue(PubSubService.send_sms_notification, notification)
            django_rq.enqueue(PubSubService.send_push_notification, notification.id)
            
            # Send in-app notification directly
            PubSubService.send_in_app_notification(notification)
            
            # Publish to Redis and send WebSocket notification
            PubSubService().publish_notification('notifications', notification)
            PubSubService.send_websocket_notification(notification)
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
        - notification_id (int): The ID of the notification object.
        """
        try:
            notification = Notification.objects.get(id=notification_id)
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
            # Save the notification to the database
            notification = Notification.objects.create(
                recipient=notification.recipient,
                notification_type=notification.notification_type,
                content=notification.content,
                url=notification.url,
                timestamp=notification.timestamp,
            )
            # Trigger WebSocket notification after saving to the database
            PubSubService.send_websocket_notification(notification)
            logger.info(f"In-app notification sent to {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending in-app notification: {e}")
