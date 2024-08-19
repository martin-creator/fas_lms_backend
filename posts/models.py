from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from groups.models import Group
from activity.models import Attachment, Reaction, Share
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='posts', null=True, blank=True, db_index=True)
    content = models.TextField(max_length=5000)
    attachments = GenericRelation(Attachment)
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    categories = models.ManyToManyField('activity.Category', related_name='posts_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reactions = GenericRelation(Reaction, related_name='post_reactions')
    comments = GenericRelation('Comment', related_name='post_comments')
    shares = GenericRelation(Share, related_name='post_shares')
    tags = TaggableManager()

    def __str__(self):
        return self.content[:20]

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    post = models.ForeignKey(Post, related_name='comments_posts', on_delete=models.CASCADE, db_index=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
    content = models.TextField(max_length=2000)
    attachments = GenericRelation(Attachment, related_name='comment_attachments')
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', db_index=True)
    reactions = GenericRelation(Reaction, related_name='comment_reactions')

    def __str__(self):
        return self.content[:20]


