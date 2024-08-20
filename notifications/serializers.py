# notifications/serializers.py

from rest_framework import serializers
from activity.models import Share
from .managers import NotificationManager
from .utils.encryption import encrypt_message
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
    notification_type = serializers.PrimaryKeyRelatedField(queryset=NotificationType.objects.all())
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

    def update(self, instance, validated_data):
        """
        Update an existing Notification instance with validated data.
        """
        for attr, value in validated_data.items():
            if attr == 'content':
                instance.content = encrypt_message(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def mark_as_read(self, instance):
        """
        Mark a notification as read and update read_at timestamp.
        """
        instance.mark_as_read()
        return instance

    def resend(self, instance, delivery_method=None, content=None):
        """
        Resend a notification with optional new delivery method or content.
        """
        instance.resend(delivery_method=delivery_method, content=content)
        return instance

    def archive(self, instance):
        """
        Archive a notification.
        """
        instance.archive()
        return instance

    def get_metadata_value(self, instance, key):
        """
        Retrieve specific metadata value from a notification.
        """
        return instance.get_metadata_value(key)

    def set_metadata_value(self, instance, key, value):
        """
        Update specific metadata for a notification.
        """
        instance.set_metadata_value(key, value)
        return instance

    def update_html_content(self, instance, new_html_content):
        """
        Update HTML content of a notification.
        """
        instance.update_html_content(new_html_content)
        return instance

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ('id', 'notification_type', 'template')

class NotificationSettingsSerializer(serializers.ModelSerializer):
    notification_type = serializers.PrimaryKeyRelatedField(queryset=NotificationType.objects.all())
    
    class Meta:
        model = NotificationSettings
        fields = ('id', 'user', 'notification_type', 'is_enabled', 'channel_preferences')

    def toggle_notification(self, instance, enable=True):
        """
        Toggle notification type enablement for a user.
        """
        instance.toggle_notification(enable=enable)
        return instance

    def update_channel_preferences(self, instance, new_preferences):
        """
        Update channel preferences for a user.
        """
        instance.update_channel_preferences(new_preferences)
        return instance


class NotificationReadStatusSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = NotificationReadStatus
        fields = ('id', 'user', 'notification', 'is_read', 'read_at')

    def mark_all_as_read(self, instance, user):
        """
        Mark all notifications for a user as read.
        """
        instance.mark_all_as_read(user)
        return instance


class UserNotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotificationPreference
        fields = ('user', 'email_notifications', 'sms_notifications', 'push_notifications', 'notification_frequency')

class NotificationSnoozeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSnooze
        fields = ('user', 'start_time', 'end_time')

    def snooze_notifications(self, validated_data):
        """
        Snooze notifications for a user for a specific period.
        """
        snooze_instance = NotificationSnooze.objects.create(**validated_data)
        return snooze_instance


class NotificationEngagementSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    user = serializers.StringRelatedField()  

    class Meta:
        model = NotificationEngagement
        fields = ('notification', 'user', 'viewed_at', 'clicked_at', 'interaction_type')

    def record_click(self, instance):
        """
        Record a click interaction for a notification.
        """
        instance.record_click()
        return instance

    def get_engagement_summary(self, user):
        """
        Get engagement summary for a user.
        """
        return NotificationEngagement.get_engagement_summary(user)


class NotificationABTestSerializer(serializers.ModelSerializer):
    notification_template = serializers.PrimaryKeyRelatedField(queryset=NotificationTemplate.objects.all())

    class Meta:
        model = NotificationABTest
        fields = ('test_name', 'variant', 'notification_template', 'start_date', 'end_date')

    def is_active(self, instance):
        """
        Check if the A/B test is currently active.
        """
        return instance.is_active()

    def record_variant_performance(self, instance, metric):
        """
        Record variant performance for an A/B test.
        """
        instance.record_variant_performance(metric)
        return instance


class NotificationLogSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()
    performed_by = serializers.StringRelatedField()  

    class Meta:
        model = NotificationLog
        fields = ('notification', 'action', 'performed_by', 'timestamp')

    def log_action(self, validated_data):
        """
        Log an action performed on a notification.
        """
        log_instance = NotificationLog.objects.create(**validated_data)
        return log_instance

