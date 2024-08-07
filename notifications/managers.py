# notifications/managers.py

from django.db import models
from querying.querysets import NotificationQuerySet

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model, using=self._db)

    def unread(self):
        return self.get_queryset().unread()

    def by_user(self, user):
        return self.get_queryset().by_user(user)

    def recent(self):
        return self.get_queryset().recent()
