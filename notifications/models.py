from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from activity.models import Reaction, Share
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from django_cryptography.fields import encrypt
from django.utils.translation import gettext_lazy as _


NOTIFICATION_PRIORITY = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
    (4, 'Critical'),
]

DEFAULT_NOTIFICATION_TYPE = [
    ('job_application', 'Job Application'),
    ('job_listing', 'Job Listing'),
    ('message', 'Message'),
    ('follow', 'Follow'),
    ('connection', 'Connection'),
    ('reaction', 'Reaction'),
    ('post', 'Posts'),
    ('share', 'Share'),
    ('tag', 'Tag'),
    ('comment', 'Comment'),
    ('endorsement', 'Endorsement'),
    ('skill', 'Skill'),
    ('experience', 'Experience'),
    ('education', 'Education'),
    ('group', 'Group'),
]

class NotificationType(models.Model):
    PREDEFINED_TYPES = DEFAULT_NOTIFICATION_TYPE
    type_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.type_name

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = encrypt(models.TextField())
    html_content = models.TextField(blank=True, null=True)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    language = models.CharField(
        max_length=10, 
        default='en', 
        choices=[('en', _('English')), ('es', _('Spanish')), ('fr', _('French'))])
    delivery_method = models.CharField(
        max_length=10,
        choices=[('push', 'Push'), ('email', 'Email'), ('sms', 'SMS')]
    )
    shares = models.ManyToManyField(Share, related_name='notifications_shares', blank=True)
    priority = models.IntegerField(choices=NOTIFICATION_PRIORITY, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ("can_manage_notifications", "Can manage notifications"),
            ("can_view_notifications", "Can view notifications"),
        ]

    def __str__(self):
        return f"{self.notification_type.type_name} Notification for {self.recipient.username}"
        
    def delete_old_notifications():
        threshold_date = timezone.now() - timedelta(days=365)  # Example: 1 year retention
        Notification.objects.filter(sent_at__lt=threshold_date).delete()

class NotificationTemplate(models.Model):
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    template = models.TextField()

    def __str__(self):
        return self.notification_type.type_name

class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    channel_preferences = models.JSONField(default=dict)  # Stores user preferences for channels (email, SMS, push, etc.)

    class Meta:
        unique_together = ('user', 'notification_type')

    def __str__(self):
        return f"{self.user.user.username}'s Notification Settings"

class NotificationReadStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.user.username} read status for {self.notification}"
        
        
class UserNotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    notification_frequency = models.CharField(
        max_length=20,
        choices=[
            ('instant', 'Instant'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly')
        ],
        default='instant'
    )
    
    def __str__(self):
        return f"{self.user.username}'s Notification Preferences"
    
class NotificationSnooze(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return f"Snooze for {self.user.username} from {self.start_time} to {self.end_time}"
    
class NotificationEngagement(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Engagement for {self.user.username} on {self.notification}"
    
class NotificationABTest(models.Model):
    test_name = models.CharField(max_length=100)
    variant = models.CharField(max_length=50)
    notification_template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    def __str__(self):
        return f"A/B Test {self.test_name} - Variant {self.variant}"


class NotificationLog(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Action: {self.action} on Notification {self.notification.id} by {self.performed_by.username if self.performed_by else 'Unknown'} at {self.timestamp}"