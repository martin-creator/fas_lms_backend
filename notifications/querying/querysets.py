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
