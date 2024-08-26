from django.db import models
from posts.querying.posts_querysets import PostQuerySet, CommentQuerySet
from datetime import timezone

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db).pinned_first()
    
    def complex_query(self, **kwargs):
        return self.get_queryset().filter_complex(**kwargs)

    def sorted_posts(self, field_name='created_at', descending=False):
        return self.get_queryset().sort_by(field_name, descending)

    def public(self):
        return self.get_queryset().public()

    def private(self):
        return self.get_queryset().private()

    def by_author(self, author):
        return self.get_queryset().by_author(author)

    def by_group(self, group):
        return self.get_queryset().by_group(group)

    def with_reaction_counts(self):
        return self.get_queryset().with_reaction_counts()

    def with_comment_counts(self):
        return self.get_queryset().with_comment_counts()

    def with_share_counts(self):
        return self.get_queryset().with_share_counts()

    def related_posts(self, post):
        return self.get_queryset().related_posts(post)

    def recent_comments(self, limit=5):
        return self.get_queryset().recent_comments(limit=limit)
    
    def batch_archive(self, post_ids):
        return self.filter(id__in=post_ids).update(archived_at=timezone.now())

    def batch_restore(self, post_ids):
        return self.filter(id__in=post_ids).update(archived_at=None)

    def sorted_posts(self, field_name='created_at', descending=False):
        return self.get_queryset().sort_by(field_name, descending)

    def popular_tags(self, limit=20):
        return self.get_queryset().tag_cloud(limit)


class CommentManager(models.Manager):
    def get_queryset(self):
        return CommentQuerySet(self.model, using=self._db)
    
    def public(self):
        return self.get_queryset().public()

    def private(self):
        return self.get_queryset().private()

    def by_author(self, author):
        return self.get_queryset().by_author(author)

    def by_post(self, post):
        return self.get_queryset().by_post(post)

    def with_reaction_counts(self):
        return self.get_queryset().with_reaction_counts()

    def recent(self, limit=5):
        return self.get_queryset().recent(limit=limit)
    
    def batch_delete(self, comment_ids):
        return self.filter(id__in=comment_ids).delete()


