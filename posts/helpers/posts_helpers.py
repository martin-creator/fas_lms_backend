from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from posts.models import Post, Comment
# from profiles.models import UserProfile
from posts.serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


# class Post(models.Model):
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
#     group = models.ForeignKey('groups.Group', on_delete=models.CASCADE, related_name='posts', null=True, blank=True, db_index=True)
#     content = models.TextField(max_length=5000)
#     attachments = GenericRelation('activity.Attachment')
#     visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
#     categories = models.ManyToManyField('activity.Category', related_name='posts_categories')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     reactions = GenericRelation('activity.Reaction', related_name='post_reactions')
#     comments = GenericRelation('Comment', related_name='post_comments')
#     shares = GenericRelation('activity.Share', related_name='post_shares')
#     pinned = models.BooleanField(default=False, db_index=True)
#     archived_at = models.DateTimeField(null=True, blank=True, db_index=True)
#     reported = models.BooleanField(default=False, db_index=True)
#     tags = TaggableManager()
#     slug = models.SlugField(unique=True, max_length=255, null=True, blank=True, db_index=True)
#     deleted = models.BooleanField(default=False, db_index=True)
#     objects = PostManager()

#     class Meta:
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['-created_at']),
#             models.Index(fields=['author']),
#             models.Index(fields=['visibility']),
#         ]

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.content[:50])
#         super(Post, self).save(*args, **kwargs)

#     def get_absolute_url(self):
#         return reverse('post_detail', kwargs={'slug': self.slug})

#     def is_public(self):
#         return self.visibility == 'public'

#     def toggle_visibility(self):
#         self.visibility = 'private' if self.visibility == 'public' else 'public'
#         self.save()

#     def add_tags(self, *tag_names):
#         for tag_name in tag_names:
#             self.tags.add(tag_name)

#     def remove_tags(self, *tag_names):
#         for tag_name in tag_names:
#             self.tags.remove(tag_name)

#     def archive(self):
#         self.archived_at = timezone.now()
#         self.save()

#     def unarchive(self):
#         self.archived_at = None
#         self.save()

#     def report(self):
#         self.reported = True
#         self.save()

#     def resolve_report(self):
#         self.reported = False
#         self.save()

#     @classmethod
#     def bulk_archive(cls, post_ids):
#         return cls.objects.filter(id__in=post_ids).update(archived_at=timezone.now())

#     @classmethod
#     def bulk_pin(cls, post_ids, pinned=True):
#         return cls.objects.filter(id__in=post_ids).update(pinned=pinned)

#     def delete(self, *args, **kwargs):
#         self.deleted = True
#         self.save()

#     def __str__(self):
#         return self.content[:20]
    


# class Comment(models.Model):
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField(null=True, blank=True)
#     content_object = GenericForeignKey('content_type', 'object_id')
#     post = models.ForeignKey('Post', related_name='comments_posts', on_delete=models.CASCADE, db_index=True)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)
#     content = models.TextField(max_length=2000)
#     attachments = GenericRelation('activity.Attachment', related_name='comment_attachments')
#     visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', db_index=True)
#     reactions = GenericRelation('activity.Reaction', related_name='comment_reactions')
#     deleted = models.BooleanField(default=False, db_index=True)
#     objects = CommentManager()

#     class Meta:
#         ordering = ['created_at']
#         indexes = [
#             models.Index(fields=['-created_at']),
#             models.Index(fields=['author']),
#             models.Index(fields=['visibility']),
#         ]

#     def get_absolute_url(self):
#         return self.post.get_absolute_url() + f"#comment-{self.id}"

#     def get_reactions_count(self):
#         return self.reactions.count()

#     def get_replies(self):
#         return self.replies.all()

#     def is_public(self):
#         return self.visibility == 'public'

#     def toggle_visibility(self):
#         self.visibility = 'private' if self.visibility == 'public' else 'public'
#         self.save()

#     def add_attachment(self, attachment):
#         self.attachments.add(attachment)

#     def remove_attachment(self, attachment):
#         self.attachments.remove(attachment)

#     def delete_with_replies(self):
#         for reply in self.replies.all():
#             reply.delete_with_replies()
#         self.delete()

#     def delete(self, *args, **kwargs):
#         self.deleted = True
#         self.save()

#     def __str__(self):
#         return self.content[:20]




class PostHelpers:

    @staticmethod
    def process_post_data(data):
        """
        Process post data before saving it to the database.
        """
        author = data.get('author')
        group = data.get('group')
        content = data.get('content')
        visibility = data.get('visibility')
        categories = data.get('categories')
        reactions = data.get('reactions')
        comments = data.get('comments')
        shares = data.get('shares')
        pinned = data.get('pinned')
        archived_at = data.get('archived_at')
        reported = data.get('reported')
        tags = data.get('tags')
        slug = data.get('slug')
        deleted = data.get('deleted')

        post = Post(
            author=author,
            group=group,
            content=content,
            visibility=visibility,
            pinned=pinned,
            archived_at=archived_at,
            reported=reported,
            slug=slug,
            deleted=deleted
        )

        return post, categories, reactions, comments, shares, tags


    @staticmethod
    def process_post_data_update(post_id, data):
        """
        Process post data before updating it in the database.
        """
        post = Post.objects.get(id=post_id)

        author = data.get('author')
        group = data.get('group')
        content = data.get('content')
        visibility = data.get('visibility')
        categories = data.get('categories')
        reactions = data.get('reactions')
        comments = data.get('comments')
        shares = data.get('shares')
        pinned = data.get('pinned')
        archived_at = data.get('archived_at')
        reported = data.get('reported')
        tags = data.get('tags')
        slug = data.get('slug')
        deleted = data.get('deleted')

        if author is not None:
            post.author = author

        if group is not None:
            post.group = group

        if content is not None:
            post.content = content

        if visibility is not None:
            post.visibility = visibility

        if pinned is not None:
            post.pinned = pinned

        if archived_at is not None:
            post.archived_at = archived_at

        if reported is not None:
            post.reported = reported

        if slug is not None:
            post.slug = slug

        if deleted is not None:
            post.deleted = deleted

        return post, categories
    


    @staticmethod
    def process_comment_data(data):
        """
        Process comment data before saving it to the database.
        """
        content_type = data.get('content_type')
        object_id = data.get('object_id')
        post = data.get('post')
        author = data.get('author')
        content = data.get('content')
        visibility = data.get('visibility')
        parent_comment = data.get('parent_comment')
        reactions = data.get('reactions')
        deleted = data.get('deleted')

        comment = Comment(
            content_type=content_type,
            object_id=object_id,
            post=post,
            author=author,
            content=content,
            visibility=visibility,
            parent_comment=parent_comment,
            deleted=deleted
        )

        return comment, reactions
    

    @staticmethod
    def process_comment_data_update(comment_id, data):
        """
        Process comment data before updating it in the database.
        """
        comment = Comment.objects.get(id=comment_id)

        content_type = data.get('content_type')
        object_id = data.get('object_id')
        post = data.get('post')
        author = data.get('author')
        content = data.get('content')
        visibility = data.get('visibility')
        parent_comment = data.get('parent_comment')
        reactions = data.get('reactions')
        deleted = data.get('deleted')

        if content_type is not None:
            comment.content_type = content_type

        if object_id is not None:
            comment.object_id = object_id

        if post is not None:
            comment.post = post

        if author is not None:
            comment.author = author

        if content is not None:
            comment.content = content

        if visibility is not None:
            comment.visibility = visibility

        if parent_comment is not None:
            comment.parent_comment = parent_comment

        if deleted is not None:
            comment.deleted = deleted

        return comment, reactions