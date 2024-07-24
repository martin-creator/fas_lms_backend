from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from profiles.models import UserProfile
from django.contrib.auth import get_user_model
from .services import NotificationService

User = get_user_model()


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        NotificationService.send_notification_service(instance)

@receiver(post_save, sender=User)
def create_default_notification_settings(sender, instance, created, **kwargs):
    if created:
        NotificationService.update_notification_settings(instance)