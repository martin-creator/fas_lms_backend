from notifications.services import NotificationService
from django.utils import timezone
from notifications.models import Notification
from django.core.mail import send_mail
from django.conf import settings

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
