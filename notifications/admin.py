from django.contrib import admin
from .models import (
    Notification, NotificationTemplate, NotificationSettings,
    NotificationReadStatus, NotificationType, UserNotificationPreference,
    NotificationSnooze, NotificationEngagement, NotificationABTest,
    NotificationLog
)
from .forms import NotificationTypeForm, NotificationForm, NotificationTemplateForm, NotificationSettingsForm, NotificationReadStatusForm

@admin.register(NotificationType)
class NotificationTypeAdmin(admin.ModelAdmin):
    form = NotificationTypeForm
    list_display = ('type_name',)
    search_fields = ('type_name',)

@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    form = NotificationTemplateForm
    list_display = ('notification_type',)
    search_fields = ('notification_type__type_name',)

@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    form = NotificationSettingsForm
    list_display = ('user', 'notification_type', 'is_enabled')
    list_filter = ('notification_type', 'is_enabled')
    search_fields = ('user__username', 'notification_type__type_name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    list_display = ('recipient', 'notification_type', 'content_preview', 'timestamp', 'is_read')
    list_filter = ('notification_type', 'is_read', 'timestamp')
    search_fields = ('recipient__username', 'notification_type__type_name')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content'

@admin.register(NotificationReadStatus)
class NotificationReadStatusAdmin(admin.ModelAdmin):
    form = NotificationReadStatusForm
    list_display = ('user', 'notification', 'is_read', 'read_at')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'notification__notification_type__type_name')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'notification')

    def notification_type(self, obj):
        return obj.notification.notification_type.type_name

    notification_type.short_description = 'Notification Type'

@admin.register(UserNotificationPreference)
class UserNotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'sms_notifications', 'push_notifications', 'notification_frequency')
    search_fields = ('user__username',)
    list_filter = ('notification_frequency',)

@admin.register(NotificationSnooze)
class NotificationSnoozeAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_time', 'end_time')
    list_filter = ('user',)

@admin.register(NotificationEngagement)
class NotificationEngagementAdmin(admin.ModelAdmin):
    list_display = ('notification', 'user', 'viewed_at', 'clicked_at', 'interaction_type')
    list_filter = ('interaction_type', 'viewed_at', 'clicked_at')
    search_fields = ('user__username', 'notification__notification_type__type_name')

@admin.register(NotificationABTest)
class NotificationABTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'variant', 'notification_template', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'variant')
    search_fields = ('test_name', 'notification_template__notification_type__type_name')

@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ('notification', 'action', 'performed_by', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('notification__notification_type__type_name', 'performed_by__username')