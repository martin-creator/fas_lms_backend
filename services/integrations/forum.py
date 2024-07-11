import logging
from django.db import transaction
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from posts.models import Post, Comment
from activity.models import Attachment, Category, Reaction, Share
from notifications.models import Notification, NotificationType
from notifications.services import NotificationService
from taggit.models import Tag

logger = logging.getLogger(__name__)

class ForumService:

    @staticmethod
    def create_thread(author_id: int, content: str, group_id: int = None, visibility: str = 'public', category_ids: list = [], tag_names: list = []) -> Post:
        """
        Create a new forum thread as a post.
        """
        try:
            author = User.objects.get(id=author_id)
            categories = Category.objects.filter(id__in=category_ids)
            tags = [Tag.objects.get_or_create(name=name)[0] for name in tag_names]

            post = Post.objects.create(
                author=author,
                group_id=group_id,
                content=content,
                visibility=visibility
            )
            post.categories.set(categories)
            post.tags.set(tags)
            post.save()

            # Create notification for the new thread
            NotificationService.create_notification(
                recipient=author,
                content=f'New thread created: {content[:20]}',
                notification_type_name='post',
                content_object=post
            )

            logger.info(f"Created new thread by {author.username} with content: {content[:20]}")
            return post
        except ObjectDoesNotExist as e:
            logger.error(f"Error creating thread: {e}")
            raise ValidationError("Author or Group not found.")

    @staticmethod
    def create_comment(post_id: int, author_id: int, content: str, visibility: str = 'public', parent_comment_id: int = None) -> Comment:
        """
        Create a new comment on a forum post.
        """
        try:
            post = Post.objects.get(id=post_id)
            author = User.objects.get(id=author_id)
            parent_comment = Comment.objects.get(id=parent_comment_id) if parent_comment_id else None

            comment = Comment.objects.create(
                post=post,
                author=author,
                content=content,
                visibility=visibility,
                parent_comment=parent_comment
            )

            # Notify post author and other participants
            ForumService.notify_users(post, f'New comment by {author.username}: {content[:20]}')

            logger.info(f"User {author.username} commented on post {post.id}: {content[:20]}")
            return comment
        except ObjectDoesNotExist as e:
            logger.error(f"Error creating comment: {e}")
            raise ValidationError("Post, Author, or Parent Comment not found.")

    @staticmethod
    def delete_comment(comment_id: int, user_id: int):
        """
        Soft delete a comment in a forum thread.
        """
        try:
            comment = Comment.objects.get(id=comment_id, author_id=user_id)
            comment.is_deleted = True
            comment.save()
            logger.info(f"User {comment.author.username} deleted comment {comment.id}")
        except ObjectDoesNotExist as e:
            logger.error(f"Error deleting comment: {e}")
            raise ValidationError("Comment not found or user not authorized.")

    @staticmethod
    def list_threads(group_id: int = None) -> list:
        """
        List all threads (posts) in a specific group or globally.
        """
        if group_id:
            return Post.objects.filter(group_id=group_id, parent_post__isnull=True)
        return Post.objects.filter(parent_post__isnull=True)

    @staticmethod
    def list_comments(post_id: int) -> list:
        """
        List all comments for a specific thread (post).
        """
        return Comment.objects.filter(post_id=post_id, is_deleted=False)

    @staticmethod
    def search_threads(keyword: str) -> list:
        """
        Search for threads based on a keyword.
        """
        return Post.objects.filter(content__icontains=keyword, parent_post__isnull=True)

    @staticmethod
    def search_comments(keyword: str) -> list:
        """
        Search for comments based on a keyword.
        """
        return Comment.objects.filter(content__icontains=keyword, is_deleted=False)

    @staticmethod
    def moderate_content(comment_id: int, action: str):
        """
        Moderate a comment (e.g., mark as inappropriate, delete).
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            if action == 'delete':
                comment.is_deleted = True
                comment.save()
                logger.info(f"Comment {comment_id} marked as deleted")
            elif action == 'flag':
                # Implement flagging logic here
                logger.info(f"Comment {comment_id} flagged for review")
            else:
                raise ValidationError("Invalid moderation action.")
        except ObjectDoesNotExist as e:
            logger.error(f"Error moderating content: {e}")
            raise ValidationError("Comment not found.")

    @staticmethod
    def notify_users(post: Post, message: str):
        """
        Notify users about a new comment or thread update.
        """
        users = User.objects.filter(post__comments_posts=post).distinct()
        for user in users:
            NotificationService.create_notification(
                recipient=user,
                content=message,
                notification_type_name='comment',
                content_object=post
            )
            logger.info(f"Notified user {user.username} about post {post.id}")

    @staticmethod
    @transaction.atomic
    def bulk_create_comments(post_id: int, comments_data: list):
        """
        Bulk create comments on a post.
        """
        post = Post.objects.get(id=post_id)
        comments = [Comment(post=post, content=data['content'], author_id=data['author_id']) for data in comments_data]
        Comment.objects.bulk_create(comments)
        logger.info(f"Bulk created {len(comments)} comments on post {post.id}")

    @staticmethod
    def get_thread_details(post_id: int) -> dict:
        """
        Get detailed information about a thread, including comments and users.
        """
        try:
            post = Post.objects.get(id=post_id)
            comments = post.comments_posts.filter(is_deleted=False).select_related('author')
            details = {
                'post': post,
                'comments': comments,
                'users': [comment.author for comment in comments]
            }
            return details
        except ObjectDoesNotExist as e:
            logger.error(f"Error fetching thread details: {e}")
            raise ValidationError("Post not found.")

    @staticmethod
    def add_reaction_to_post(post_id: int, user_id: int, reaction_type: str):
        """
        Add a reaction to a post.
        """
        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=user_id)
            reaction, created = Reaction.objects.get_or_create(
                post=post,
                user=user,
                type=reaction_type
            )

            if created:
                # Notify post author about the reaction
                NotificationService.create_notification(
                    recipient=post.author,
                    content=f'{user.username} reacted to your post: {reaction_type}',
                    notification_type_name='reaction',
                    content_object=post
                )

            logger.info(f"User {user.username} reacted to post {post.id} with {reaction_type}")
        except ObjectDoesNotExist as e:
            logger.error(f"Error adding reaction to post: {e}")
            raise ValidationError("Post or User not found.")

    @staticmethod
    def add_reaction_to_comment(comment_id: int, user_id: int, reaction_type: str):
        """
        Add a reaction to a comment.
        """
        try:
            comment = Comment.objects.get(id=comment_id)
            user = User.objects.get(id=user_id)
            reaction, created = Reaction.objects.get_or_create(
                comment=comment,
                user=user,
                type=reaction_type
            )

            if created:
                # Notify comment author about the reaction
                NotificationService.create_notification(
                    recipient=comment.author,
                    content=f'{user.username} reacted to your comment: {reaction_type}',
                    notification_type_name='reaction',
                    content_object=comment
                )

            logger.info(f"User {user.username} reacted to comment {comment.id} with {reaction_type}")
        except ObjectDoesNotExist as e:
            logger.error(f"Error adding reaction to comment: {e}")
            raise ValidationError("Comment or User not found.")

    @staticmethod
    def share_post(post_id: int, user_id: int, shared_to_ids: list):
        """
        Share a post with other users.
        """
        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=user_id)
            shared_to_users = User.objects.filter(id__in=shared_to_ids)

            share = Share.objects.create(
                user=user,
                content_object=post
            )
            share.shared_to.set(shared_to_users)
            share.save()

            for recipient in shared_to_users:
                NotificationService.create_notification(
                    recipient=recipient,
                    content=f'{user.username} shared a post with you.',
                    notification_type_name='share',
                    content_object=post
                )

            logger.info(f"User {user.username} shared post {post.id} with users {shared_to_ids}")
        except ObjectDoesNotExist as e:
            logger.error(f"Error sharing post: {e}")
            raise ValidationError("Post, User, or Recipients not found.")