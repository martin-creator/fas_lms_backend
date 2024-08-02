from django.db import models
from profiles.models import UserProfile
from activity.models import Attachment, Category
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager

class Event(models.Model):
    organizer = models.ForeignKey(UserProfile, related_name='organized_events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachments = GenericRelation(Attachment)
    categories = models.ManyToManyField(Category, related_name='events_categories')
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attendees = models.ManyToManyField(UserProfile, related_name='events', blank=True)
    event_date = models.DateField()
    capacity = models.PositiveIntegerField()
    tags = TaggableManager()
    registration_required = models.BooleanField(default=True)
    max_registrations = models.PositiveIntegerField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    online_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f'{self.title} organized by {self.organizer.user.username}'

    def register_attendee(self, user):
        if self.attendees.count() < self.capacity:
            self.attendees.add(user)
            self.save()
            return True
        return False

    def is_full(self):
        return self.attendees.count() >= self.capacity