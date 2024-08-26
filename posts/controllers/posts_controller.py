from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.querying.posts_querysets import PostQuerySet, CommentQuerySet
from posts.reports.posts_report import PostReport
from posts.settings.posts_settings import PostsSettings
from posts.utils import UserUtils, DateTimeUtils
from posts.services.posts_services import PostService


# class PostService:

#     @staticmethod
#     def create_post(data):
#         """
#         Create a new post.
#         Deafault author, title, content, visibility='public', group=None, tags=None, categories=None, pinned=False, reported=False
#         """
#         post, categories, reactions, comments, shares, tags = PostHelpers.process_post_data(data)
#         post.save()
#         post.categories.set(categories)
#         post.tags.set(tags)
#         return PostSerializer(post).data
    

#     @staticmethod
#     def get_post(post_id):
#         """
#         Get a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         return PostSerializer(post).data
    

#     @staticmethod
#     def update_post(post_id, data):
#         """
#         Update a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post, categories, reactions, comments, shares, tags = PostHelpers.process_post_data_update(post, data)
#         post.save()
#         post.categories.set(categories)
#         post.tags.set(tags)
        
#         if reactions is not None:
#             post.reactions.set(reactions)

#         if comments is not None:
#             post.comments.set(comments)

#         if shares is not None:
#             post.shares.set(shares)
        
#         return PostSerializer(post).data
    

#     @staticmethod
#     def delete_post(post_id):
#         """
#         Delete a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.delete()
#         return True
    

#     @staticmethod
#     def pin_post(post_id):
#         """
#         Pin a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.pinned = True
#         post.save()
#         return True
    

#     @staticmethod
#     def unpin_post(post_id):
#         """
#         Unpin a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.pinned = False
#         post.save()
#         return True
    

#     @staticmethod
#     def report_post(post_id):
#         """
#         Report a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.reported = True
#         post.save()
#         return True
    

#     @staticmethod
#     def resolve_report_post(post_id):
#         """
#         Resolve report for a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.reported = False
#         post.save()
#         return True
    

#     @staticmethod
#     def get_posts():
#         """
#         Get all posts.
#         """
#         posts = Post.objects.all()
#         return PostSerializer(posts, many=True).data
    

#     # archive
#     @staticmethod
#     def archive_post(post_id):
#         """
#         Archive a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.archive()
#         return True
    

#     @staticmethod
#     def unarchive_post(post_id):
#         """
#         Unarchive a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.unarchive()
#         return True
    

#     # attachments
#     @staticmethod
#     def add_attachments_to_post(post_id, attachment_ids):
#         """
#         Add attachments to a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.attachments.add(*attachment_ids)
#         return True
    

#     @staticmethod
#     def remove_attachments_from_post(post_id, attachment_ids):
#         """
#         Remove attachments from a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.attachments.remove(*attachment_ids)
#         return True
    
#     # visibility
#     @staticmethod
#     def toggle_visibility_post(post_id):
#         """
#         Toggle visibility for a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.toggle_visibility()
#         return True
    

#     @staticmethod
#     def add_tags_to_post(post_id, tag_names):
#         """
#         Add tags to a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.tags.add(*tag_names)
#         return True
    

#     @staticmethod
#     def remove_tags_from_post(post_id, tag_names):
#         """
#         Remove tags from a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         post.tags.remove(*tag_names)
#         return True
    

#     @staticmethod
#     def get_reactions_count(post_id):
#         """
#         Get reactions count for a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         return post.reactions.count()
    

#     @staticmethod
#     def get_comments_count(post_id):
#         """
#         Get comments count for a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         return post.comments.count()
    

#     @staticmethod
#     def get_shares_count(post_id):
#         """
#         Get shares count for a specific post.
#         """
#         post = Post.objects.get(id=post_id)
#         return post.shares.count()
            

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
    
#     @staticmethod
#     def get_reported_posts():
#         """
#         Get all reported posts.
#         """
#         posts = Post.objects.reported()
#         return PostSerializer(posts, many=True).data
    
#     @staticmethod
#     def get_archived_posts():
#         """
#         Get all archived posts.
#         """
#         posts = Post.objects.archived()
#         return PostSerializer(posts, many=True).data
    
#     @staticmethod
#     def get_active_posts():
#         """
#         Get all active posts.
#         """
#         posts = Post.objects.active()
#         return PostSerializer(posts, many=True).data
    
#     @staticmethod
#     def get_posts_by_group(group):
#         """
#         Get posts by a specific group.
#         """
#         posts = Post.objects.by_group(group)
#         return PostSerializer(posts, many=True).data
    
#     @staticmethod
#     def get_posts_by_tag(tag_name):
#         """
#         Get posts by a specific tag.
#         """
#         posts = Post.objects.by_tag(tag_name)
#         return PostSerializer(posts, many=True).data
    
#     @staticmethod
#     def get_recent_comments(limit=5):
#         """
#         Get recent comments for posts.
#         """
#         comments = Comment.objects.recent(limit=limit)
#         return CommentSerializer(comments, many=True).data
    
#     @staticmethod
#     def get_posts_by_tag_report():
#         """
#         Get a report for all posts by tag.
#         """
#         return PostReport.get_posts_by_tag_report()
    

# # Comments


#     @staticmethod
#     def create_comment(data):
#         """
#         Create a new comment.
#         Deafault author, title, content, visibility='public', group=None, tags=None, categories=None, pinned=False, reported=False
#         """
#         comment, reactions = PostHelpers.process_comment_data(data)
#         comment.save()
#         comment.reactions.set(reactions)
#         return CommentSerializer(comment).data
    

#     @staticmethod
#     def get_comment(comment_id):
#         """
#         Get a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         return CommentSerializer(comment).data
    

#     @staticmethod
#     def update_comment(comment_id, data):
#         """
#         Update a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment, reactions = PostHelpers.process_comment_data_update(comment, data)
#         comment.save()
#         comment.reactions.set(reactions)
#         return CommentSerializer(comment).data
    

#     @staticmethod
#     def delete_comment(comment_id):
#         """
#         Delete a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.delete()
#         return True
    

#     @staticmethod
#     def delete_comment_with_replies(comment_id):
#         """
#         Delete a specific comment and its replies.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.delete_with_replies()
#         return True
    


    

#     @staticmethod
#     def report_comment(comment_id):
#         """
#         Report a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.reported = True
#         comment.save()
#         return True
    

#     @staticmethod
#     def resolve_report_comment(comment_id):
#         """
#         Resolve report for a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.reported = False
#         comment.save()
#         return True
    

#     @staticmethod
#     def get_comments():
#         """
#         Get all comments.
#         """
#         comments = Comment.objects.all()
#         return CommentSerializer(comments, many=True).data
    

#     @staticmethod
#     def archive_comment(comment_id):
#         """
#         Archive a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.archive()
#         return True
    

#     @staticmethod
#     def unarchive_comment(comment_id):
#         """
#         Unarchive a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.unarchive()
#         return True
    

#     @staticmethod
#     def toggle_visibility_comment(comment_id):
#         """
#         Toggle visibility for a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.toggle_visibility()
#         return True
    

#     @staticmethod
#     def add_attachments_to_comment(comment_id, attachment_ids):
#         """
#         Add attachments to a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.attachments.add(*attachment_ids)
#         return True
    

#     @staticmethod
#     def remove_attachments_from_comment(comment_id, attachment_ids):
#         """
#         Remove attachments from a specific comment.
#         """
#         comment = Comment.objects.get(id=comment_id)
#         comment.attachments.remove(*attachment_ids)
#         return True
    

    




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
        


