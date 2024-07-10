from notifications.services import NotificationService
from django.utils import timezone
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings
import logging
from typing import List, Dict, Union
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from services.exceptions import NotificationException
from push_notifications.models import GCMDevice, APNSDevice

logger = logging.getLogger(__name__)

class NotificationHandler:
    @staticmethod
    def send_email_notification(subject: str, template_name: str, context: Dict[str, Union[str, int]], recipient_list: List[str], from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send an email notification using an HTML template.
        """
        try:
            html_content = render_to_string(template_name, context)
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            logger.info(f"Email notification sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending email notification to {recipient_list}: {e}")
            raise NotificationException("Failed to send email notification.")
    
    @staticmethod
    def send_push_notification(user: User, message: str):
        """
        Send a push notification to a user.
        """
        try:
            # Send to GCM (Google Cloud Messaging) Devices
            gcm_devices = GCMDevice.objects.filter(user=user)
            if gcm_devices.exists():
                gcm_devices.send_message(message)
                logger.info(f"GCM push notification sent to user: {user.username}")
            
            # Send to APNS (Apple Push Notification Service) Devices
            apns_devices = APNSDevice.objects.filter(user=user)
            if apns_devices.exists():
                apns_devices.send_message(message)
                logger.info(f"APNS push notification sent to user: {user.username}")
        except Exception as e:
            logger.error(f"Error sending push notification to user {user.username}: {e}")
            raise NotificationException("Failed to send push notification.")
    
    @staticmethod
    def send_bulk_push_notification(users: List[User], message: str):
        """
        Send bulk push notifications to multiple users.
        """
        try:
            for user in users:
                NotificationHandler.send_push_notification(user, message)
            logger.info(f"Bulk push notifications sent successfully to users.")
        except Exception as e:
            logger.error(f"Error sending bulk push notifications: {e}")
            raise NotificationException("Failed to send bulk push notifications.")
    
    @staticmethod
    def send_sms_notification(phone_number: str, message: str):
        """
        Send an SMS notification.
        """
        try:
            # Integrate with an SMS gateway provider
            # Example: Using Twilio
            from twilio.rest import Client
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            logger.info(f"SMS notification sent successfully to: {phone_number}")
        except Exception as e:
            logger.error(f"Error sending SMS notification to {phone_number}: {e}")
            raise NotificationException("Failed to send SMS notification.")
    
    @staticmethod
    def send_in_app_notification(user: User, title: str, message: str):
        """
        Send an in-app notification.
        """
        try:
            # Assuming you have an InAppNotification model
            from services.models import InAppNotification
            InAppNotification.objects.create(
                user=user,
                title=title,
                message=message
            )
            logger.info(f"In-app notification sent to user: {user.username}")
        except Exception as e:
            logger.error(f"Error sending in-app notification to user {user.username}: {e}")
            raise NotificationException("Failed to send in-app notification.")
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        """
        Validate a phone number.
        """
        import re
        phone_regex = r'^\+?1?\d{9,15}$'
        is_valid = re.match(phone_regex, phone_number) is not None
        if is_valid:
            logger.info(f"Valid phone number: {phone_number}")
        else:
            logger.error(f"Invalid phone number: {phone_number}")
        return is_valid

# Example usage:
# NotificationHandler.send_email_notification("Subject", "email_template.html", {"name": "John"}, ["recipient@example.com"])

class NotificationHandler:
    @staticmethod
    def send_notification(user, message, notification_type, content_object=None):
        NotificationService.create_notification(
            recipient=user,
            content=message,
            notification_type_name=notification_type,
            content_object=content_object,
            priority=0
        )

def send_notification(user, message, notification_type='general'):
    Notification.objects.create(
        user=user,
        message=message,
        created_at=timezone.now()
    )
    # Additionally, send an email if needed
    from utils.email_integration import send_email
    send_email(
        subject=f"Notification: {notification_type.replace('_', ' ').title()}",
        message=message,
        recipient_list=[user.email],
        fail_silently=True,
    )
