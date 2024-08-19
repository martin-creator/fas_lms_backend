from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from profiles.models import UserProfile
from posts.models import Post, Comment
from .models import Category, Share, Reaction, Attachment, Thread, UserActivity, UserStatistics, MarketingCampaign, LearningService, Analytics
from typing import Any
from notifications.models import NotificationType, Notification
from .tasks import create_user_activity_task, create_notification_task
import logging
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Post)
def post_activity(sender, instance, created, **kwargs):
    notification_type = NotificationType.objects.get(type_name='post_created' if created else 'post_updated')
    action = 'post_created' if created else 'post_updated'
    content_message = f'{action.replace("_", " ").capitalize()} a post: {instance.content}'
    
    logger.info(f"Creating user activity for post: {instance.id}, Action: {action}")
    create_user_activity_task.delay(instance.author.id, action, content_message)
    
    logger.info(f"Creating notification for post: {instance.id}, Content: {content_message}")
    create_notification_task.delay(
        recipient_id=instance.author.id,
        content=f'Your post "{instance.content}" was {action.replace("_", " ")}.',
        notification_type_id=notification_type.id,
        url=f'/posts/{instance.id}/'
    )

@receiver(post_delete, sender=Post)
def post_deleted_activity(sender, instance, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='post_deleted')
    content_message = f'Deleted a post: {instance.content}'
    
    logger.info(f"Creating user activity for deleted post: {instance.id}")
    create_user_activity_task.delay(instance.author.id, 'post_deleted', content_message)
    
    logger.info(f"Creating notification for deleted post: {instance.id}, Content: {content_message}")
    create_notification_task.delay(
        recipient_id=instance.author.id,
        content=f'Your post "{instance.content}" was deleted.',
        notification_type_id=notification_type.id,
        url=f'/posts/{instance.id}/'
    )

@receiver(post_save, sender=Comment)
def comment_activity(sender, instance, created, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='comment_created' if created else 'comment_updated')
    action = 'comment_created' if created else 'comment_updated'
    content_message = f'{action.replace("_", " ").capitalize()} on a post: {instance.post.content}'
    
    logger.info(f"Creating user activity for comment: {instance.id}, Action: {action}")
    create_user_activity_task.delay(instance.author.id, action, content_message)
    
    logger.info(f"Creating notification for comment: {instance.id}, Content: {content_message}")
    create_notification_task.delay(
        recipient_id=instance.author.id,
        content=f'Your comment on the post "{instance.post.content}" was {action.replace("_", " ")}.',
        notification_type_id=notification_type.id,
        url=f'/posts/{instance.post.id}/'
    )

@receiver(post_delete, sender=Comment)
def comment_deleted_activity(sender, instance, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='comment_deleted')
    content_message = f'Deleted a comment on a post: {instance.post.content}'
    
    logger.info(f"Creating user activity for deleted comment: {instance.id}")
    create_user_activity_task.delay(instance.author.id, 'comment_deleted', content_message)
    
    logger.info(f"Creating notification for deleted comment: {instance.id}, Content: {content_message}")
    create_notification_task.delay(
        recipient_id=instance.author.id,
        content=f'Your comment on the post "{instance.post.content}" was deleted.',
        notification_type_id=notification_type.id,
        url=f'/posts/{instance.post.id}/'
    )

@receiver(post_save, sender=Reaction)
def reaction_activity(sender, instance, created, **kwargs):
    if created:
        try:
            content_object = instance.content_object
            if not content_object:
                raise ValueError("Content object is None")

            content_type = ContentType.objects.get_for_model(content_object.__class__)
            notification_type, _ = NotificationType.objects.get_or_create(type_name='reaction_created')
            recipient_id = content_object.author.id if hasattr(content_object, 'author') else None
            url = content_object.get_absolute_url() if hasattr(content_object, 'get_absolute_url') else None
            content_message = f'{instance.user} reacted to your {content_object}'

            logger.debug(f"Content Object: {content_object}, Recipient ID: {recipient_id}, URL: {url}, Content Message: {content_message}")

            if recipient_id and url and content_message:
                logger.info(f"Creating notification: User {recipient_id}, Content: {content_message}, URL: {url}")
                
                create_user_activity_task.delay(
                    instance.user.id,
                    'reaction_created',
                    f'Reacted to {content_object}'
                )
                create_notification_task.delay(
                    recipient_id=recipient_id,
                    content=content_message,
                    notification_type_id=notification_type.id,
                    url=url
                )
            else:
                logger.error(f"Failed to create notification: Missing recipient_id, url, or content_message for Reaction ID: {instance.id}")
        except Exception as e:
            logger.error(f"Error in reaction_activity signal:")

@receiver(post_save, sender=Share)
def share_activity(sender, instance, created, **kwargs):
    if created:
        notification_type, _ = NotificationType.objects.get_or_create(type_name='share_created')
        create_user_activity_task.delay(instance.user.id, 'content_shared', f'Shared content: {instance.content_object}')
        create_notification_task.delay(
            recipient_id=instance.user.id,
            content=f'Your share of {instance.content_object} was created.',
            notification_type_id=notification_type.id,
            url=f'/posts/{instance.post.id}/'
        )

@receiver(post_save, sender=Attachment)
def attachment_activity(sender, instance, created, **kwargs):
    if created:
        notification_type, _ = NotificationType.objects.get_or_create(type_name='attachment_added')
        create_user_activity_task.delay(instance.content_object.user.id, 'attachment_added', f'Added an attachment to {instance.content_object}')
        create_notification_task.delay(
            recipient_id=instance.content_object.user.id,
            content=f'Your attachment to {instance.content_object} was added.',
            notification_type_id=notification_type.id,
            url=f'/posts/{instance.post.id}/'
        )

@receiver(post_save, sender=Thread)
def thread_activity(sender, instance, created, **kwargs):
    if created:
        notification_type, _ = NotificationType.objects.get_or_create(type_name='thread_created')
        for participant in instance.participants.all():
            create_user_activity_task.delay(participant.id, 'thread_created', f'Joined a new thread: {instance.subject}')
            create_notification_task.delay(
                recipient_id=participant.id,
                content=f'You joined a new thread: {instance.subject}',
                notification_type_id=notification_type.id,
                url=f'/threads/{instance.id}/'
            )

@receiver(post_save, sender=UserStatistics)
def user_statistics_updated(sender, instance, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='statistics_updated')
    create_user_activity_task.delay(instance.user.id, 'statistics_updated', 'User statistics updated')
    create_notification_task.delay(
        recipient_id=instance.user.id,
        content='Your user statistics were updated.',
        notification_type_id=notification_type.id,
        url=f'/users/{instance.user.id}/statistics/'
    )

@receiver(post_save, sender=MarketingCampaign)
def marketing_campaign_activity(sender, instance, created, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='marketing_campaign_created' if created else 'marketing_campaign_updated')
    action = 'marketing_campaign_created' if created else 'marketing_campaign_updated'
    create_user_activity_task.delay(instance.user.id, action, f'{action.replace("_", " ").capitalize()} marketing campaign: {instance.campaign_name}')
    create_notification_task.delay(
        recipient_id=instance.user.id,
        content=f'Your marketing campaign "{instance.campaign_name}" was {action.replace("_", " ")}.',
        notification_type_id=notification_type.id,
        url=f'/campaigns/{instance.id}/'
    )

@receiver(post_save, sender=LearningService)
def learning_service_activity(sender, instance, created, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='learning_service_created' if created else 'learning_service_updated')
    action = 'learning_service_created' if created else 'learning_service_updated'
    create_user_activity_task.delay(instance.user.id, action, f'{action.replace("_", " ").capitalize()} learning service: {instance.service_name}')
    create_notification_task.delay(
        recipient_id=instance.user.id,
        content=f'Your learning service "{instance.service_name}" was {action.replace("_", " ")}.',
        notification_type_id=notification_type.id,
        url=f'/services/{instance.id}/'
    )

@receiver(post_save, sender=Analytics)
def analytics_activity(sender, instance, created, **kwargs):
    notification_type, _ = NotificationType.objects.get_or_create(type_name='analytics_created' if created else 'analytics_updated')
    action = 'analytics_created' if created else 'analytics_updated'
    create_user_activity_task.delay(instance.user.id, action, f'{action.replace("_", " ").capitalize()} analytics')
    create_notification_task.delay(
        recipient_id=instance.user.id,
        content=f'Your analytics were {action.replace("_", " ")}.',
        notification_type_id=notification_type.id,
        url=f'/analytics/{instance.id}/'
    )

@receiver(m2m_changed, sender=Share.shared_to.through)
def share_recipients_changed(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        notification_type, _ = NotificationType.objects.get_or_create(type_name='share_recipients_changed')
        create_user_activity_task.delay(instance.user.id, 'share_recipients_changed', f'Updated share recipients for content: {instance.content_object}')
        create_notification_task.delay(
            recipient_id=instance.user.id,
            content=f'Updated share recipients for content: {instance.content_object}',
            notification_type_id=notification_type.id,
            url=f'/shares/{instance.id}/'
        )
