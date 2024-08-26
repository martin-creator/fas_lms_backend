from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.settings.posts_settings import PostsSettings
from posts.helpers.posts_helpers import PostHelpers
from posts.utils import UserUtils, DateTimeUtils
from posts.reports.posts_report import PostReport


# class PostQuerySet(models.QuerySet):
    
#     def filter_complex(self, **kwargs):
#         qs = self
#         if 'is_pinned' in kwargs:
#             qs = qs.filter(pinned=kwargs['is_pinned'])
#         if 'is_reported' in kwargs:
#             qs = qs.filter(reported=kwargs['is_reported'])
#         if 'is_archived' in kwargs:
#             qs = qs.filter(archived_at__isnull=not kwargs['is_archived'])
#         return qs

#     def sort_by(self, field_name, descending=False):
#         order_by_field = f'-{field_name}' if descending else field_name
#         return self.order_by(order_by_field)
    
#     def public(self):
#         """Filter posts that are public."""
#         return self.filter(visibility='public')
    
#     def private(self):
#         """Filter posts that are private."""
#         return self.filter(visibility='private')
    
#     def archived(self):
#         return self.filter(archived_at__isnull=False)

#     def active(self):
#         return self.filter(archived_at__isnull=True)
    
#     def by_author(self, author):
#         """Filter posts by a specific author."""
#         return self.filter(author=author)

#     def by_group(self, group):
#         """Filter posts by a specific group."""
#         return self.filter(group=group)

#     def with_reaction_counts(self):
#         """Annotate posts with the count of reactions."""
#         return self.annotate(reactions_count=Count('reactions'))
    
#     def get_reactions_count(self):
#         cache_key = f'post_{self.id}_reactions_count'
#         count = cache.get(cache_key)
#         if count is None:
#             count = self.reactions.count()
#             cache.set(cache_key, count, 60 * 15)  # Cache for 15 minutes
#         return count

#     def with_comment_counts(self):
#         """Annotate posts with the count of comments."""
#         return self.annotate(comments_count=Count('comments'))

#     def with_share_counts(self):
#         """Annotate posts with the count of shares."""
#         return self.annotate(shares_count=Count('shares'))

#     def related_posts(self, post):
#         """Get related posts by categories."""
#         return self.filter(categories__in=post.categories.all()).exclude(id=post.id).distinct()

#     def recent_comments(self, limit=5):
#         """Get recent comments for posts."""
#         return self.annotate(
#             recent_comments=Count('comments', filter=Q(comments__created_at__gte=models.functions.Now()))
#         ).order_by('-recent_comments')[:limit]
        
#     def tag_cloud(self, limit=20):
#         return self.annotate(tag_count=Count('tags')).order_by('-tag_count')[:limit]

#     def pinned_first(self):
#         return self.order_by('-pinned', '-created_at')
    
#     def by_tag(self, tag_name):
#         return self.filter(tags__name__icontains=tag_name)

#     def popular_tags(self, limit=10):
#         return self.annotate(tag_count=models.Count('tags')).order_by('-tag_count')[:limit]
    
#     def reported(self):
#         return self.filter(reported=True)
        
#     def search(self, query):
#         return self.filter(
#             models.Q(content__icontains=query) |
#             models.Q(tags__name__icontains=query) |
#             models.Q(author__username__icontains=query)
#         )


# class CommentQuerySet(models.QuerySet):
    
#     def public(self):
#         """Filter comments that are public."""
#         return self.filter(visibility='public')
    
#     def private(self):
#         """Filter comments that are private."""
#         return self.filter(visibility='private')
    
#     def by_author(self, author):
#         """Filter comments by a specific author."""
#         return self.filter(author=author)

#     def by_post(self, post):
#         """Filter comments for a specific post."""
#         return self.filter(post=post)

#     def with_reaction_counts(self):
#         """Annotate comments with the count of reactions."""
#         return self.annotate(reactions_count=Count('reactions'))

#     def recent(self, limit=5):
#         """Get the most recent comments."""
#         return self.order_by('-created_at')[:limit]
    
#     def search(self, query):
#         return self.filter(
#             models.Q(content__icontains=query) |
#             models.Q(author__username__icontains=query)
#         )


# class PostManager(models.Manager):
#     def get_queryset(self):
#         return PostQuerySet(self.model, using=self._db).pinned_first()
    
#     def complex_query(self, **kwargs):
#         return self.get_queryset().filter_complex(**kwargs)

#     def sorted_posts(self, field_name='created_at', descending=False):
#         return self.get_queryset().sort_by(field_name, descending)

#     def public(self):
#         return self.get_queryset().public()

#     def private(self):
#         return self.get_queryset().private()

#     def by_author(self, author):
#         return self.get_queryset().by_author(author)

#     def by_group(self, group):
#         return self.get_queryset().by_group(group)

#     def with_reaction_counts(self):
#         return self.get_queryset().with_reaction_counts()

#     def with_comment_counts(self):
#         return self.get_queryset().with_comment_counts()

#     def with_share_counts(self):
#         return self.get_queryset().with_share_counts()

#     def related_posts(self, post):
#         return self.get_queryset().related_posts(post)

#     def recent_comments(self, limit=5):
#         return self.get_queryset().recent_comments(limit=limit)
    
#     def batch_archive(self, post_ids):
#         return self.filter(id__in=post_ids).update(archived_at=timezone.now())

#     def batch_restore(self, post_ids):
#         return self.filter(id__in=post_ids).update(archived_at=None)

#     def sorted_posts(self, field_name='created_at', descending=False):
#         return self.get_queryset().sort_by(field_name, descending)

#     def popular_tags(self, limit=20):
#         return self.get_queryset().tag_cloud(limit)


# class CommentManager(models.Manager):
#     def get_queryset(self):
#         return CommentQuerySet(self.model, using=self._db)
    
#     def public(self):
#         return self.get_queryset().public()

#     def private(self):
#         return self.get_queryset().private()

#     def by_author(self, author):
#         return self.get_queryset().by_author(author)

#     def by_post(self, post):
#         return self.get_queryset().by_post(post)

#     def with_reaction_counts(self):
#         return self.get_queryset().with_reaction_counts()

#     def recent(self, limit=5):
#         return self.get_queryset().recent(limit=limit)
    
#     def batch_delete(self, comment_ids):
#         return self.filter(id__in=comment_ids).delete()




# class PostService:
#     @staticmethod
#     def get_sorted_posts(field_name='created_at', descending=False):
#         """
#         Get sorted posts.
#         """
#         posts = Post.objects.sorted_posts(field_name=field_name, descending=descending)
#         return PostSerializer(posts, many=True).data

#     @staticmethod
#     def get_public_posts():
#         """
#         Get all public posts.
#         """
#         posts = Post.objects.public()
#         return PostSerializer(posts, many=True).data

#     @staticmethod
#     def get_posts_by_author(author):
#         """
#         Get posts by a specific author.
#         """
#         posts = Post.objects.by_author(author)
#         return PostSerializer(posts, many=True).data

#     @staticmethod
#     def archive_posts(post_ids):
#         """
#         Archive multiple posts.
#         """
#         Post.objects.batch_archive(post_ids)
#         return True

#     @staticmethod
#     def restore_posts(post_ids):
#         """
#         Restore multiple posts.
#         """
#         Post.objects.batch_restore(post_ids)
#         return True

#     @staticmethod
#     def get_related_posts(post):
#         """
#         Get posts related to a specific post.
#         """
#         posts = Post.objects.related_posts(post)
#         return PostSerializer(posts, many=True).data

#     @staticmethod
#     def get_popular_tags(limit=20):
#         """
#         Get popular tags.
#         """
#         tags = Post.objects.popular_tags(limit=limit)
#         return tags


# class CommentService:
#     @staticmethod
#     def get_public_comments():
#         """
#         Get all public comments.
#         """
#         comments = Comment.objects.public()
#         return CommentSerializer(comments, many=True).data

#     @staticmethod
#     def get_comments_by_post(post):
#         """
#         Get comments related to a specific post.
#         """
#         comments = Comment.objects.by_post(post)
#         return CommentSerializer(comments, many=True).data

#     @staticmethod
#     def delete_comments(comment_ids):
#         """
#         Delete multiple comments.
#         """
#         Comment.objects.batch_delete(comment_ids)
#         return True


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







# class generate  comprehenisve CRUD functions for posts and comments for a social media platform
# Use the above managers to create the CRUD functions
# make sure you add all functionalities add to the managers from the query set 
# Make sure all basic CRUD functions that make a proper content creation and engagement platform are implemented


class PostService:

    @staticmethod
    def create_post(data):
        """
        Create a new post.
        Deafault author, title, content, visibility='public', group=None, tags=None, categories=None, pinned=False, reported=False
        """
        post, categories, reactions, comments, shares, tags = PostHelpers.process_post_data(data)
        post.save()
        post.categories.set(categories)
        post.tags.set(tags)
        return PostSerializer(post).data
    

    @staticmethod
    def get_post(post_id):
        """
        Get a specific post.
        """
        post = Post.objects.get(id=post_id)
        return PostSerializer(post).data
    

    @staticmethod
    def update_post(post_id, data):
        """
        Update a specific post.
        """
        post = Post.objects.get(id=post_id)
        post, categories, reactions, comments, shares, tags = PostHelpers.process_post_data_update(post, data)
        post.save()
        post.categories.set(categories)
        post.tags.set(tags)
        
        if reactions is not None:
            post.reactions.set(reactions)

        if comments is not None:
            post.comments.set(comments)

        if shares is not None:
            post.shares.set(shares)
        
        return PostSerializer(post).data
    

    @staticmethod
    def delete_post(post_id):
        """
        Delete a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.delete()
        return True
    

    @staticmethod
    def pin_post(post_id):
        """
        Pin a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.pinned = True
        post.save()
        return True
    

    @staticmethod
    def unpin_post(post_id):
        """
        Unpin a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.pinned = False
        post.save()
        return True
    

    @staticmethod
    def report_post(post_id):
        """
        Report a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.reported = True
        post.save()
        return True
    

    @staticmethod
    def resolve_report_post(post_id):
        """
        Resolve report for a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.reported = False
        post.save()
        return True
    

    @staticmethod
    def get_posts():
        """
        Get all posts.
        """
        posts = Post.objects.all()
        return PostSerializer(posts, many=True).data
    

    # archive
    @staticmethod
    def archive_post(post_id):
        """
        Archive a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.archive()
        return True
    

    @staticmethod
    def unarchive_post(post_id):
        """
        Unarchive a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.unarchive()
        return True
    

    # attachments
    @staticmethod
    def add_attachments_to_post(post_id, attachment_ids):
        """
        Add attachments to a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.attachments.add(*attachment_ids)
        return True
    

    @staticmethod
    def remove_attachments_from_post(post_id, attachment_ids):
        """
        Remove attachments from a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.attachments.remove(*attachment_ids)
        return True
    
    # visibility
    @staticmethod
    def toggle_visibility_post(post_id):
        """
        Toggle visibility for a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.toggle_visibility()
        return True
    

    @staticmethod
    def add_tags_to_post(post_id, tag_names):
        """
        Add tags to a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.tags.add(*tag_names)
        return True
    

    @staticmethod
    def remove_tags_from_post(post_id, tag_names):
        """
        Remove tags from a specific post.
        """
        post = Post.objects.get(id=post_id)
        post.tags.remove(*tag_names)
        return True
    

    @staticmethod
    def get_reactions_count(post_id):
        """
        Get reactions count for a specific post.
        """
        post = Post.objects.get(id=post_id)
        return post.reactions.count()
    

    @staticmethod
    def get_comments_count(post_id):
        """
        Get comments count for a specific post.
        """
        post = Post.objects.get(id=post_id)
        return post.comments.count()
    

    @staticmethod
    def get_shares_count(post_id):
        """
        Get shares count for a specific post.
        """
        post = Post.objects.get(id=post_id)
        return post.shares.count()
            

    @staticmethod
    def get_sorted_posts(field_name='created_at', descending=False):
        """
        Get sorted posts.
        """
        posts = Post.objects.sorted_posts(field_name=field_name, descending=descending)
        return PostSerializer(posts, many=True).data

    @staticmethod
    def get_public_posts():
        """
        Get all public posts.
        """
        posts = Post.objects.public()
        return PostSerializer(posts, many=True).data

    @staticmethod
    def get_posts_by_author(author):
        """
        Get posts by a specific author.
        """
        posts = Post.objects.by_author(author)
        return PostSerializer(posts, many=True).data

    @staticmethod
    def archive_posts(post_ids):
        """
        Archive multiple posts.
        """
        Post.objects.batch_archive(post_ids)
        return True

    @staticmethod
    def restore_posts(post_ids):
        """
        Restore multiple posts.
        """
        Post.objects.batch_restore(post_ids)
        return True

    @staticmethod
    def get_related_posts(post):
        """
        Get posts related to a specific post.
        """
        posts = Post.objects.related_posts(post)
        return PostSerializer(posts, many=True).data

    @staticmethod
    def get_popular_tags(limit=20):
        """
        Get popular tags.
        """
        tags = Post.objects.popular_tags(limit=limit)
        return tags
    
    @staticmethod
    def get_reported_posts():
        """
        Get all reported posts.
        """
        posts = Post.objects.reported()
        return PostSerializer(posts, many=True).data
    
    @staticmethod
    def get_archived_posts():
        """
        Get all archived posts.
        """
        posts = Post.objects.archived()
        return PostSerializer(posts, many=True).data
    
    @staticmethod
    def get_active_posts():
        """
        Get all active posts.
        """
        posts = Post.objects.active()
        return PostSerializer(posts, many=True).data
    
    @staticmethod
    def get_posts_by_group(group):
        """
        Get posts by a specific group.
        """
        posts = Post.objects.by_group(group)
        return PostSerializer(posts, many=True).data
    
    @staticmethod
    def get_posts_by_tag(tag_name):
        """
        Get posts by a specific tag.
        """
        posts = Post.objects.by_tag(tag_name)
        return PostSerializer(posts, many=True).data
    
    @staticmethod
    def get_recent_comments(limit=5):
        """
        Get recent comments for posts.
        """
        comments = Comment.objects.recent(limit=limit)
        return CommentSerializer(comments, many=True).data
    
    @staticmethod
    def get_posts_by_tag_report():
        """
        Get a report for all posts by tag.
        """
        return PostReport.get_posts_by_tag_report()
    


class CommentService:
    
        @staticmethod
        def create_comment(data):
            """
            Create a new comment.
            Deafault author, title, content, visibility='public', group=None, tags=None, categories=None, pinned=False, reported=False
            """
            comment, reactions = PostHelpers.process_comment_data(data)
            comment.save()
            comment.reactions.set(reactions)
            return CommentSerializer(comment).data
        
    
        @staticmethod
        def get_comment(comment_id):
            """
            Get a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            return CommentSerializer(comment).data
        
    
        @staticmethod
        def update_comment(comment_id, data):
            """
            Update a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment, reactions = PostHelpers.process_comment_data_update(comment, data)
            comment.save()
            comment.reactions.set(reactions)
            return CommentSerializer(comment).data
        
    
        @staticmethod
        def delete_comment(comment_id):
            """
            Delete a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return True
        

        @staticmethod
        def delete_comment_with_replies(comment_id):
            """
            Delete a specific comment and its replies.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.delete_with_replies()
            return True
        


        
    
        @staticmethod
        def report_comment(comment_id):
            """
            Report a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.reported = True
            comment.save()
            return True
        
    
        @staticmethod
        def resolve_report_comment(comment_id):
            """
            Resolve report for a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.reported = False
            comment.save()
            return True
        
    
        @staticmethod
        def get_comments():
            """
            Get all comments.
            """
            comments = Comment.objects.all()
            return CommentSerializer(comments, many=True).data
        
    
        @staticmethod
        def archive_comment(comment_id):
            """
            Archive a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.archive()
            return True
        
    
        @staticmethod
        def unarchive_comment(comment_id):
            """
            Unarchive a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.unarchive()
            return True
        
    
        @staticmethod
        def toggle_visibility_comment(comment_id):
            """
            Toggle visibility for a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.toggle_visibility()
            return True
        
    
        @staticmethod
        def add_attachments_to_comment(comment_id, attachment_ids):
            """
            Add attachments to a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.attachments.add(*attachment_ids)
            return True
        

        @staticmethod
        def remove_attachments_from_comment(comment_id, attachment_ids):
            """
            Remove attachments from a specific comment.
            """
            comment = Comment.objects.get(id=comment_id)
            comment.attachments.remove(*attachment_ids)
            return True
        

       
    