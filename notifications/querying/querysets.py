# notifications/querying/querysets.py

from django.db import models
from django.utils import timezone
from datetime import timedelta

class NotificationQuerySet(models.QuerySet):
    def unread(self):
        return self.filter(is_read=False)

    def by_user(self, user):
        return self.filter(recipient=user)

    def recent(self):
        return self.filter(timestamp__gte=timezone.now() - timedelta(days=30))

    def mark_all_as_read(self, user):
        return self.filter(recipient=user, is_read=False).update(is_read=True, read_at=timezone.now())

    def get_engagement_summary(self, user):
        from notifications.models import NotificationEngagement
        engagements = NotificationEngagement.objects.filter(user=user)
        return {
            'total_views': engagements.filter(interaction_type='view').count(),
            'total_clicks': engagements.filter(interaction_type='click').count()
        }

    def delete_old_notifications(self):
        threshold_date = timezone.now() - timedelta(days=365)
        return self.filter(timestamp__lt=threshold_date).delete()

    def toggle_notification(self, user, notification_type, enable=True):
        from notifications.models import NotificationSettings
        settings, created = NotificationSettings.objects.get_or_create(user=user, notification_type=notification_type)
        settings.is_enabled = enable
        settings.save(update_fields=['is_enabled'])
        return settings

    def snooze_notifications(self, user, start_time, end_time):
        from notifications.models import NotificationSnooze
        return NotificationSnooze.objects.create(user=user, start_time=start_time, end_time=end_time)

    def get_notifications_by_type(self, user, notification_type):
        return self.filter(recipient=user, notification_type=notification_type).order_by('-timestamp')

    def search_notifications(self, user, query):
        search_query = models.Q(content__icontains=query) | models.Q(html_content__icontains=query)
        return self.filter(recipient=user).filter(search_query).order_by('-timestamp')
