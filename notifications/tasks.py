# notifications/tasks.py
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
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
def send_bulk_notifications(notification_data_list):
    for data in notification_data_list:
        try:
            # Here, you should implement the `send_notification` function
            # which will handle sending notifications based on the `data`
            send_notification(data)
        except Exception as e:
            logger.error(f"Failed to send bulk notification: {e}")


def send_push_notification(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        # Implement push notification logic here (e.g., using Firebase Cloud Messaging)
        # Example:
        # send_fcm_notification(notification.recipient, notification.content)
    except ObjectDoesNotExist:
        logger.error(f"Notification with ID {notification_id} does not exist.")
    except Exception as e:
        logger.error(f"Failed to send push notification: {e}")


# def send_sms_notification(user, content):
#     try:
#         # Implement SMS notification logic here (e.g., using Twilio)
#         # Example:
#         # send_twilio_sms(user.phone_number, content)
#     except Exception as e:
#         logger.error(f"Failed to send SMS notification: {e}")


def send_in_app_notification(user, content):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                'type': 'chat.message',
                'message': content
            }
        )
    except Exception as e:
        logger.error(f"Failed to send in-app notification: {e}")


def send_notification(data):
    """
    Example function for sending a notification based on data provided.
    This function needs to be implemented according to your notification types and delivery methods.
    """
    # You should decide the logic for sending notifications based on the data
    # Example:
    # if data['type'] == 'email':
    #     send_email_notification(data['notification_id'])
    # elif data['type'] == 'push':
    #     send_push_notification(data['notification_id'])
    # elif data['type'] == 'sms':
    #     send_sms_notification(data['user'], data['content'])
    # elif data['type'] == 'in_app':
    #     send_in_app_notification(data['user'], data['content'])
