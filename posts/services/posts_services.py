from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.settings.posts_settings import PostsSettings
from posts.helpers.posts_helpers import PostHelpers
from posts.utils import UserUtils, DateTimeUtils
from posts.reports.posts_report import PostReport


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
    

# Comments


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
    

    
