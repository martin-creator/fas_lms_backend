# notifications/serializers.py

from rest_framework import serializers
from activity.models import Share
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
    recipient = serializers.StringRelatedField() 
    content_object = serializers.SerializerMethodField()
    notification_type = NotificationTypeSerializer()
    shares = serializers.PrimaryKeyRelatedField(many=True, queryset=Share.objects.all(), required=False)
    
    class Meta:
        model = Notification
        fields = (
            'id', 'recipient', 'content_type', 'object_id', 'content_object', 'content',
            'html_content', 'url', 'timestamp', 'is_read', 'read_at', 'notification_type',
            'language', 'delivery_method', 'severity', 'shares', 'priority', 'created_at', 'updated_at'
        )

    def get_content_object(self, obj):
        if obj.content_object:
            return {
                'content_type': obj.content_type.model,
                'object_id': obj.object_id
            }
        return None

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ('id', 'notification_type', 'template')

class NotificationSettingsSerializer(serializers.ModelSerializer):
    notification_type = NotificationTypeSerializer()
    
    class Meta:
        model = NotificationSettings
        fields = ('id', 'user', 'notification_type', 'is_enabled', 'channel_preferences')

class NotificationReadStatusSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

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
    notification = NotificationSerializer()
    user = serializers.StringRelatedField()  

    class Meta:
        model = NotificationEngagement
        fields = ('notification', 'user', 'viewed_at', 'clicked_at', 'interaction_type')

class NotificationABTestSerializer(serializers.ModelSerializer):
    notification_template = NotificationTemplateSerializer()

    class Meta:
        model = NotificationABTest
        fields = ('test_name', 'variant', 'notification_template', 'start_date', 'end_date')

class NotificationLogSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    performed_by = serializers.StringRelatedField()  
    class Meta:
        model = NotificationLog
        fields = ('notification', 'action', 'performed_by', 'timestamp')
