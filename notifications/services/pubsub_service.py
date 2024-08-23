# notifications/services/pubsub_service.py

import json
import logging
from django.core.mail import send_mail
from django.conf import settings
from django_rq import enqueue as django_rq_enqueue
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import redis
from django.apps import apps

# Initialize the logger
logger = logging.getLogger(__name__)

class PubSubService:
    """
    Service responsible for publishing and sending notifications
    through various channels, including real-time updates.
    """

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def publish_notification(self, channel, notification):
        """
        Publish the notification to a Redis channel.

        Args:
            channel (str): The Redis channel name.
            notification (Notification): The notification object.
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

    def send_websocket_notification(self, notification):
        """
        Send a WebSocket notification.

        Args:
            notification (Notification): The notification object.
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

    def handle_real_time_notification(self, notification):
        """
        Handle real-time notifications by publishing to Redis and sending WebSocket notifications.

        Args:
            notification (Notification): The notification object.
        """
        try:
            self.publish_notification('notifications', notification)
            self.send_websocket_notification(notification)
        except Exception as e:
            logger.error(f"Error handling real-time notification: {e}")

    def send_notification(self, notification):
        """
        Send a notification through various channels.

        Args:
            notification (Notification): The notification object.
        """
        try:
            # Enqueue email, SMS, and push notification tasks to be processed asynchronously
            django_rq_enqueue(self.send_email_notification, notification)
            django_rq_enqueue(self.send_sms_notification, notification)
            django_rq_enqueue(self.send_push_notification, notification.id)

            # Send in-app notification directly
            self.send_in_app_notification(notification)

            # Handle real-time notification
            self.handle_real_time_notification(notification)

        except Exception as e:
            logger.error(f"Error dispatching notification: {e}")
        
    def send_in_app_notification(self, notification):
        """
        Send an in-app notification.

        Args:
            notification (Notification): The notification object.
        """
        try:
            # Save the notification to the database
            notification.save()
            logger.info(f"In-app notification sent to {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending in-app notification: {e}")

    def send_email_notification(self, notification):
        """
        Send an email notification.

        Args:
            notification (Notification): The notification object.
        """
        try:
            user_email = notification.recipient.email
            send_mail(
                notification.notification_type.type_name,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )
            logger.info(f"Email sent to {user_email}")
        except Exception as e:
            logger.error(f"Error sending email: {e}")

    def send_sms_notification(self, notification):
        """
        Send an SMS notification.

        Args:
            notification (Notification): The notification object.
        """
        try:
            user_phone = notification.recipient.phone_number
            # Implement SMS sending logic here
            logger.info(f"SMS sent to {user_phone}")
        except Exception as e:
            logger.error(f"Error sending SMS: {e}")

    def send_push_notification(self, notification_id):
        """
        Send a push notification.

        Args:
            notification_id (int): The ID of the notification.
        """
        try:
            Notification = apps.get_model('notifications', 'Notification')
            notification = Notification.objects.get(id=notification_id)
            # Implement push notification sending logic here
            logger.info(f"Push notification sent to {notification.recipient.username}")
        except Exception as e:
            logger.error(f"Error sending push notification: {e}")


