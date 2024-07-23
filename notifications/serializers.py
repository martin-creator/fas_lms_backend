# notifications/serializers.py

from rest_framework import serializers
from .models import Notification, NotificationType, NotificationTemplate, NotificationSettings, NotificationReadStatus

class NotificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationType
        fields = ('id', 'type_name')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'content_type', 'object_id', 'content_object', 'content', 'url', 'timestamp', 'is_read', 'notification_type', 'shares', 'priority', 'created_at', 'updated_at')

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