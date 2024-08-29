from django.db import models
from django.db.models import Count, Q
from django.core.cache import cache

class PostQuerySet(models.QuerySet):
    
    def filter_complex(self, **kwargs):
        qs = self
        if 'is_pinned' in kwargs:
            qs = qs.filter(pinned=kwargs['is_pinned'])
        if 'is_reported' in kwargs:
            qs = qs.filter(reported=kwargs['is_reported'])
        if 'is_archived' in kwargs:
            qs = qs.filter(archived_at__isnull=not kwargs['is_archived'])
        return qs

    def sort_by(self, field_name, descending=False):
        order_by_field = f'-{field_name}' if descending else field_name
        return self.order_by(order_by_field)
    
    def public(self):
        """Filter posts that are public."""
        return self.filter(visibility='public')
    
    def private(self):
        """Filter posts that are private."""
        return self.filter(visibility='private')
    
    def archived(self):
        return self.filter(archived_at__isnull=False)

    def active(self):
        return self.filter(archived_at__isnull=True)
    
    def by_author(self, author):
        """Filter posts by a specific author."""
        return self.filter(author=author)

    def by_group(self, group):
        """Filter posts by a specific group."""
        return self.filter(group=group)

    def with_reaction_counts(self):
        """Annotate posts with the count of reactions."""
        return self.annotate(reactions_count=Count('reactions'))
    
    def get_reactions_count(self):
        cache_key = f'post_{self.id}_reactions_count'
        count = cache.get(cache_key)
        if count is None:
            count = self.reactions.count()
            cache.set(cache_key, count, 60 * 15)  # Cache for 15 minutes
        return count

    def with_comment_counts(self):
        """Annotate posts with the count of comments."""
        return self.annotate(comments_count=Count('comments'))

    def with_share_counts(self):
        """Annotate posts with the count of shares."""
        return self.annotate(shares_count=Count('shares'))

    def related_posts(self, post):
        """Get related posts by categories."""
        return self.filter(categories__in=post.categories.all()).exclude(id=post.id).distinct()

    def recent_comments(self, limit=5):
        """Get recent comments for posts."""
        return self.annotate(
            recent_comments=Count('comments', filter=Q(comments__created_at__gte=models.functions.Now()))
        ).order_by('-recent_comments')[:limit]
        
    def tag_cloud(self, limit=20):
        return self.annotate(tag_count=Count('tags')).order_by('-tag_count')[:limit]

    def pinned_first(self):
        return self.order_by('-pinned', '-created_at')
    
    def by_tag(self, tag_name):
        return self.filter(tags__name__icontains=tag_name)

    def popular_tags(self, limit=10):
        return self.annotate(tag_count=models.Count('tags')).order_by('-tag_count')[:limit]
    
    def reported(self):
        return self.filter(reported=True)
        
    def search(self, query):
        return self.filter(
            models.Q(content__icontains=query) |
            models.Q(tags__name__icontains=query) |
            models.Q(author__username__icontains=query)
        )


class CommentQuerySet(models.QuerySet):
    
    def public(self):
        """Filter comments that are public."""
        return self.filter(visibility='public')
    
    def private(self):
        """Filter comments that are private."""
        return self.filter(visibility='private')
    
    def by_author(self, author):
        """Filter comments by a specific author."""
        return self.filter(author=author)

    def by_post(self, post):
        """Filter comments for a specific post."""
        return self.filter(post=post)

    def with_reaction_counts(self):
        """Annotate comments with the count of reactions."""
        return self.annotate(reactions_count=Count('reactions'))

    def recent(self, limit=5):
        """Get the most recent comments."""
        return self.order_by('-created_at')[:limit]
    
    def search(self, query):
        return self.filter(
            models.Q(content__icontains=query) |
            models.Q(author__username__icontains=query)
        )

