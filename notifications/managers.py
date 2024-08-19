# notifications/managers.py

from django.db import models
from notifications.querying.querysets import NotificationQuerySet

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def unread(self):
        return self.get_queryset().unread()

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def recent(self):
        return self.get_queryset().recent()

    def mark_all_as_read(self, user):
        return self.get_queryset().mark_all_as_read(user)

    def get_engagement_summary(self, user):
        return self.get_queryset().get_engagement_summary(user)

    def delete_old_notifications(self):
        return self.get_queryset().delete_old_notifications()

    def toggle_notification(self, user, notification_type, enable=True):
        return self.get_queryset().toggle_notification(user, notification_type, enable)

    def snooze_notifications(self, user, start_time, end_time):
        return self.get_queryset().snooze_notifications(user, start_time, end_time)

    def get_notifications_by_type(self, user, notification_type):
        return self.get_queryset().get_notifications_by_type(user, notification_type)

    def search_notifications(self, user, query):
        return self.get_queryset().search_notifications(user, query)