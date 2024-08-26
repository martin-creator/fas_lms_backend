from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.querying.posts_querysets import PostQuerySet, CommentQuerySet
from posts.reports.posts_report import PostReport
from posts.settings.posts_settings import PostsSettings
from posts.utils import UserUtils, DateTimeUtils
from posts.services.posts_services import PostService



class PostController:
        
        def __init__(self):
            self.post_query = PostQuerySet()
            self.comment_query = CommentQuerySet()
            self.post_report = PostReport()
            self.post_settings = PostsSettings()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
            self.post_service = PostService()
    
    
        def get_all_posts(self):
            """
            Get all posts.
            """
            return self.post_service.get_posts()
    
    
        def get_post_by_id(self, post_id):
            """
            Get a specific post.
            """
            return self.post_service.get_post(post_id)
    
    
        def create_post(self, post_data):
            """
            Create a new post.
            """
            return self.post_service.create_post(post_data)
        
    
        def update_post(self, post_id, post_data):
            """
            Update a post.
            """
            return self.post_service.update_post(post_id, post_data)
        
    
        def delete_post(self, post_id):
            """
            Delete a post.
            """
            return self.post_service.delete_post(post_id)
        
    
        def pin_post(self, post_id):
            """
            Pin a post.
            """
            return self.post_service.pin_post(post_id)
        
    
        def unpin_post(self, post_id):
            """
            Unpin a post.
            """
            return self.post_service.unpin_post(post_id)
        
    
        def report_post(self, post_id):
            """
            Report a post.
            """
            return self.post_service.report_post(post_id)
        
    
        def resolve_report_post(self, post_id):
            """
            Resolve report for a post.
            """
            return self.post_service.resolve_report_post(post_id)
        
    
        def get_posts_by_author(self, author):
            """
            Get posts by a specific author.
            """
            return self.post_service.get_posts_by_author(author)
        
    
        def get_posts_by_group(self, group):
            """
            Get posts by a specific group.
            """
            return self.post_service.get_posts_by_group(group)
        
    
        def get_posts_by_tag(self, tag_name):
            """
            Get posts by a specific tag.
            """
            return self.post_service.get_posts_by_tag(tag_name)
        
    
        def get_recent_comments(self, limit=5):
            """
            Get recent comments for posts.
            """
            return self.post_service.get_recent_comments(limit)
        
    
        def get_posts_by_tag_report(self):
            """
            Get a report for all posts by tag.
            """
            return self.post_service.get_posts_by_tag_report()
        

        def get_reported_posts(self):
            """
            Get all reported posts.
            """
            return self.post_service.get_reported_posts()
        

        def get_archived_posts(self):
            """
            Get all archived posts.
            """
            return self.post_service.get_archived_posts()
        

        def get_active_posts(self):
            """
            Get all active posts.
            """
            return self.post_service.get_active_posts()
        

        def archive_posts(self, post_ids):
            """
            Archive multiple posts.
            """
            return self.post_service.archive_posts(post_ids)
        

        def restore_posts(self, post_ids):
            """
            Restore multiple posts.
            """
            return self.post_service.restore_posts(post_ids)
        

        def get_related_posts(self, post):
            """
            Get posts related to a specific post.
            """
            return self.post_service.get_related_posts(post)
        

        def get_popular_tags(self, limit=20):
            """
            Get popular tags.
            """
            return self.post_service.get_popular_tags(limit)
        

        def get_sorted_posts(self, field_name='created_at', descending=False):

            """
            Get sorted posts.
            """
            return self.post_service.get_sorted_posts(field_name=field_name, descending=descending)
        

        def get_public_posts(self):

            """
            Get all public posts.
            """
            return self.post_service.get_public_posts()
        

        def archive_post(self, post_id):
                
                """
                Archive a specific post.
                """
                return self.post_service.archive_post(post_id)
        

        def unarchive_post(self, post_id):
            """
            Unarchive a specific post.
            """
            return self.post_service.unarchive_post(post_id)
        

        def toggle_visibility_post(self, post_id):
            """
            Toggle visibility for a specific post.
            """
            return self.post_service.toggle_visibility_post(post_id)
        

        def add_tags_to_post(self, post_id, tag_names):
            """
            Add tags to a specific post.
            """
            return self.post_service.add_tags_to_post(post_id, tag_names)
        

        def remove_tags_from_post(self, post_id, tag_names):
            """
            Remove tags from a specific post.
            """
            return self.post_service.remove_tags_from_post(post_id, tag_names)
        

        def get_reactions_count(self, post_id):
            """
            Get reactions count for a specific post.
            """
            return self.post_service.get_reactions_count(post_id)
        

        def get_comments_count(self, post_id):
            """
            Get comments count for a specific post.
            """
            return self.post_service.get_comments_count(post_id)
        

        def get_shares_count(self, post_id):
            """
            Get shares count for a specific post.
            """
            return self.post_service.get_shares_count(post_id)
        

        def add_attachments_to_post(self, post_id, attachment_ids):
            """
            Add attachments to a specific post.
            """
            return self.post_service.add_attachments_to_post(post_id, attachment_ids)
        

        def remove_attachments_from_post(self, post_id, attachment_ids):
            """
            Remove attachments from a specific post.
            """
            return self.post_service.remove_attachments_from_post(post_id, attachment_ids)
        

        def create_comment(self, comment_data):
            """
            Create a new comment.
            """
            return self.post_service.create_comment(comment_data)
        

        def get_comment_by_id(self, comment_id):
            """
            Get a specific comment.
            """
            return self.post_service.get_comment(comment_id)
        

        def update_comment(self, comment_id, comment_data):
            """
            Update a comment.
            """
            return self.post_service.update_comment(comment_id, comment_data)
        

        def delete_comment(self, comment_id):
            """
            Delete a comment.
            """
            return self.post_service.delete_comment(comment_id)
        

        def delete_comment_with_replies(self, comment_id):
            """
            Delete a comment and its replies.
            """
            return self.post_service.delete_comment_with_replies(comment_id)
        

        def report_comment(self, comment_id):
            """
            Report a comment.
            """
            return self.post_service.report_comment(comment_id)
        

        def resolve_report_comment(self, comment_id):
            """
            Resolve report for a comment.
            """
            return self.post_service.resolve_report_comment(comment_id)
        

        def get_comments(self):
            """
            Get all comments.
            """
            return self.post_service.get_comments()
        

        def archive_comment(self, comment_id):
            """
            Archive a comment.
            """
            return self.post_service.archive_comment(comment_id)
        

        def unarchive_comment(self, comment_id):
            """
            Unarchive a comment.
            """
            return self.post_service.unarchive_comment(comment_id)
        

        def toggle_visibility_comment(self, comment_id):
            """
            Toggle visibility for a comment.
            """
            return self.post_service.toggle_visibility_comment(comment_id)
        

        def add_attachments_to_comment(self, comment_id, attachment_ids):
            """
            Add attachments to a comment.
            """
            return self.post_service.add_attachments_to_comment(comment_id, attachment_ids)
        

        def remove_attachments_from_comment(self, comment_id, attachment_ids):
            """
            Remove attachments from a comment.
            """
            return self.post_service.remove_attachments_from_comment(comment_id, attachment_ids)
        

        def get_comments_by_author(self, author):
            """
            Get comments by a specific author.
            """
            return self.comment_query.by_author(author)
        

        def get_comments_by_post(self, post_id):
            """
            Get comments by a specific post.
            """
            return self.comment_query.by_post(post_id)
        


