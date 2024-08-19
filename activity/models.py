from django.db import models
from django.conf import settings
from shortuuidfield import ShortUUIDField
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from taggit.managers import TaggableManager
import logging

logger = logging.getLogger(__name__)

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    
    def get_related_objects(self):
        related_objects = []
        for related_name in self._meta.related_objects:
            related_manager = getattr(self, related_name.get_accessor_name())
            related_objects.extend(related_manager.all())
        return related_objects

    def __str__(self):
        return self.name
    

    
class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    shared_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='received_shares')
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'shared_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    # def clean(self):
    #     if self.user in self.shared_to.all():
    #         raise ValidationError("Users cannot share content with themselves.")
    #     super().clean()
        
    def get_share_details(self):
        return f"Shared by {self.user.username} on {self.shared_at}, content: {self.content_object}, shared with {self.shared_to.all()}"

    def __str__(self):
        return f"{self.user.username} shared {self.content_object} with {self.shared_to.count()} users"

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('heart', 'Heart'),
        ('laugh', 'Laugh'),
        ('wow', 'Wow'),
        ('sad', 'Sad'),
        ('insight', 'Insight')
    ]
    type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self.content_object is None:
            logger.error(f"Reaction content_object is None for Reaction ID: {self.id}")
        super().save(*args, **kwargs)
        
    def get_reactions_summary(self):
        summary = {}
        for choice in dict(self.REACTION_CHOICES).keys():
            summary[choice] = self.objects.filter(type=choice, content_type=self.content_type, object_id=self.object_id).count()
        return summary

    def __str__(self):
        return f"{self.user.username} reacted with {self.type} to {self.content_object}"
    
class Attachment(models.Model):
    PHOTO = 'photo'
    DOCUMENT = 'document'
    VIDEO = 'video'
    AUDIO = 'audio'
    OTHER = 'other'

    ATTACHMENT_TYPE_CHOICES = [
        (PHOTO, 'Photo'),
        (DOCUMENT, 'Document'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
        (OTHER, 'Other'),
    ]

    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES, default=PHOTO)
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    share = GenericRelation(Share, related_name='shares_attachments')
    

    def get_attachment_url(self):
        if self.file:
            return self.file.url
        return None
    
    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return f"Attachment for {self.content_object}"
    
    
class Thread(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
    subject = models.CharField(max_length=255)
    last_message_at = models.DateTimeField()
    
    def get_last_message(self):
        return self.messages.order_by('created_at').last()
    
    def add_participant(self, user):
        if user not in self.participants.all():
            self.participants.add(user)

    def __str__(self):
        return self.subject
    
    
class UserActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField()
    categories = models.ManyToManyField(Category, related_name='user_activity_categories')
    
    @classmethod
    def log_activity(cls, user, activity_type, details, categories=None):
        activity = cls.objects.create(user=user, activity_type=activity_type, details=details)
        if categories:
            activity.categories.set(categories)
        return activity

    def __str__(self):
        return f"{self.user.username} - {self.activity_type}"
    
    
class UserStatistics(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    connections_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    engagement_rate = models.FloatField(default=0.0)
    
    def update_statistics(self, new_connections=None, new_posts=None, new_engagement=None):
        if new_connections is not None:
            self.connections_count += new_connections
        if new_posts is not None:
            self.posts_count += new_posts
        if new_engagement is not None:
            self.engagement_rate = (self.engagement_rate + new_engagement) / 2
        self.save()

    def __str__(self):
        return f"Statistics for {self.user.username}"
    
    
class MarketingCampaign(models.Model):
    campaign_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    target_audience = models.TextField()
    categories = models.ManyToManyField(Category, related_name='marketing_categories')
    attachments = GenericRelation(Attachment)
    
    def is_active(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date

    def add_attachment(self, attachment):
        self.attachments.add(attachment)
    
    def __str__(self):
        return self.campaign_name
    
    
class LearningService(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='learning_service_categories')
    resources = models.URLField()
    attachments = GenericRelation(Attachment)

    def get_related_resources(self):
        return self.resources

    def add_category(self, category):
        self.categories.add(category)
    
    def __str__(self):
        return self.service_name
    
    
class Analytics(models.Model):
    activity_type = models.CharField(max_length=50)
    engagement_rate = models.FloatField(default=0.0)
    trending_topics = models.TextField()
    categories = models.ManyToManyField(Category, related_name='analytics_categories')
    
    def update_engagement_rate(self, new_rate):
        self.engagement_rate = (self.engagement_rate + new_rate) / 2
        self.save()
        
    def add_trending_topic(self, topic):
        self.trending_topics += f", {topic}"
        self.save()

    def __str__(self):
        return self.activity_type