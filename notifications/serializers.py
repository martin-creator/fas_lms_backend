# notifications/serializers.py

from rest_framework import serializers
from .models import (
    Notification, 
    NotificationType, 
    NotificationTemplate, 
    NotificationSettings, 
    NotificationReadStatus,
    UserNotificationPreference,
    NotificationSnooze,
    NotificationEngagement,
    NotificationABTest,
    NotificationLog
)

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ('id', 'type_name')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'content_type', 'object_id', 'content_object', 'content', 
            'html_content', 'url', 'timestamp', 'is_read', 'notification_type', 'delivery_method', 
            'shares', 'priority', 'created_at', 'updated_at'
        )

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ('id', 'notification_type', 'template')

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ('id', 'user', 'notification_type', 'is_enabled', 'channel_preferences')

class NotificationReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationReadStatus
        fields = ('id', 'user', 'notification', 'is_read', 'read_at')

class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = ('user', 'email_notifications', 'sms_notifications', 'push_notifications', 'notification_frequency')

class NotificationSnoozeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSnooze
        fields = ('user', 'start_time', 'end_time')

class NotificationEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEngagement
        fields = ('notification', 'user', 'viewed_at', 'clicked_at')

class NotificationABTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationABTest
        fields = ('test_name', 'variant', 'notification_template', 'start_date', 'end_date')

class NotificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = ('notification', 'action', 'performed_by', 'timestamp')