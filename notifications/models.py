from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField
from notifications.settings.config.constances import(
    NOTIFICATION_PRIORITY, DEFAULT_NOTIFICATION_TYPE, 
    DEFAULT_LANGUAGE_TYPES, SEVERITY_CHOICES, 
    NOTIFICATION_FREQUENCY, INTERACTION_TYPE
)
from notifications.utils.delivery_method import DeliveryMethod
from activity.models import Reaction, Share
from notifications.utils.permissions import PermissionChecker
from notifications.utils.notification_actions import ActionChecker
from .managers import NotificationManager
# from encrypted_model_fields.fields import EncryptedCharField
from cryptography.fernet import Fernet
import base64
import os


# Generate a key for encryption/decryption. This should be kept safe.
# key = base64.urlsafe_b64encode(os.urandom(32))
# cipher = Fernet(key)

# def encrypt_message(message):
#     return cipher.encrypt(message.encode()).decode()

# def decrypt_message(encrypted_message):
#     return cipher.decrypt(encrypted_message.encode()).decode()

class NotificationType(models.Model):
    """
    Model to represent different types of notifications.
    """
    PREDEFINED_TYPES = DEFAULT_NOTIFICATION_TYPE
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name

class Notification(models.Model):
    """
    Model to represent notifications sent to users.
    """
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    metadata = models.JSONField(default=dict, blank=True)
    content = models.CharField(max_length=100)
    html_content = models.TextField(blank=True, null=True)
    url = models.URLField()
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    language = models.CharField(max_length=10, default='en', choices=DEFAULT_LANGUAGE_TYPES)
    delivery_method = models.CharField(max_length=10, default='IN_APP', choices=[(tag, tag.value) for tag in DeliveryMethod])
    severity = models.CharField(max_length=10, default='info', choices=SEVERITY_CHOICES)
    shares = models.ManyToManyField(Share, related_name='notifications_shares', blank=True)
    priority = models.IntegerField(choices=NOTIFICATION_PRIORITY, default=1)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)
    objects = NotificationManager()

    class Meta:
        permissions = [
            ("can_manage_notifications", "Can manage notifications"),
            ("can_view_notifications", "Can view notifications"),
        ]

    def __str__(self):
        return f"{self.notification_type.type_name} Notification for {self.recipient.username}"

    def save(self, *args, **kwargs):
        self.content
        #     self.content = encrypt_message(self.content)
        # elif self.content:
        #     self.content = encrypt_message(self.content)
        super().save(*args, **kwargs)
        DeliveryMethod.notify(self)
        
        
    # def decrypt_content(self):
    #     return decrypt_message(self.content)

    @staticmethod
    def delete_old_notifications():
        threshold_date = timezone.now() - timedelta(days=365)  # Example: 1 year retention
        Notification.objects.filter(timestamp__lt=threshold_date).delete()
        
    def perform_action(self, user, action, *args, **kwargs):
        """
        Perform an action on the Notification instance with permission checks.

        Args:
            user (User): The user performing the action.
            action (str): The action to perform (e.g., 'update_priority', 'add_share').
            *args: Additional arguments for the action.
            **kwargs: Additional keyword arguments for the action.

        Raises:
            PermissionDenied: If the user does not have permission for the action.
            ValueError: If the action is unknown.
        """
        PermissionChecker.check_permission_for_action(user, action)
        
        action_methods = {
            'update_priority': ActionChecker.update_priority,
            'add_share': ActionChecker.add_share,
            'update_html_content': ActionChecker.update_html_content,
            'update_delivery_method': ActionChecker.update_delivery_method,
            'update_severity': ActionChecker.update_severity,
            'update_notification_type': ActionChecker.update_notification_type
        }

        action_method = action_methods.get(action)
        if action_method:
            action_method(self, *args, **kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")
        
class NotificationTemplate(models.Model):
    """
    Model to represent notification templates.
    """
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    template = models.TextField()

    def __str__(self):
        return self.notification_type.type_name

class NotificationSettings(models.Model):
    """
    Model to represent user-specific notification settings.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    channel_preferences = models.JSONField(default=dict)  # Stores user preferences for channels (email, SMS, push, etc.)

    class Meta:
        unique_together = ('user', 'notification_type')

    def __str__(self):
        return f"{self.user.username}'s Notification Settings"

class NotificationReadStatus(models.Model):
    """
    Model to represent the read status of notifications.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} read status for {self.notification}"

class UserNotificationPreference(models.Model):
    """
    Model to represent user preferences for notifications.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    notification_frequency = models.CharField(
        choices=NOTIFICATION_FREQUENCY,
        max_length=20,
        default='Immediate'
    )

    def __str__(self):
        return f"{self.user.username}'s Notification Preferences"

class NotificationSnooze(models.Model):
    """
    Model to represent the snooze period for notifications.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError(_('End time must be after start time'))

    def __str__(self):
        return f"Snooze for {self.user.username} from {self.start_time} to {self.end_time}"

class NotificationEngagement(models.Model):
    """
    Model to represent user engagement with notifications.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(default=timezone.now, null=True, blank=True, editable=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE, default='view')

    def __str__(self):
        return f"Engagement for {self.user.username} on {self.notification}"

class NotificationABTest(models.Model):
    """
    Model to represent A/B testing for notifications.
    """
    test_name = models.CharField(max_length=100)
    variant = models.CharField(max_length=50)
    notification_template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"A/B Test {self.test_name} - Variant {self.variant}"

class NotificationLog(models.Model):
    """
    Model to log actions performed on notifications.
    """
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now, null=True, blank=True, editable=False)

    def __str__(self):
        return f"Action: {self.action} on Notification {self.notification.id} by {self.performed_by.username if self.performed_by else 'Unknown'} at {self.timestamp}"