from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, ChatRoom, ChatRoomNotification
from notifications.models import Notification
from activity.models import Reaction, Share
from messaging.utils.notification_utils import MessageNotificationUtils
from django.utils import timezone
from messaging.utils.message_utils import MessageUtils
import logging

logger = logging.getLogger(__name__)




@receiver(post_save, sender=Message)
def handle_message_updates(sender, instance, created, **kwargs):
    """
    Handles all notifications and updates when a new message is created.
    """
    if created:
        chat_room = instance.chat_room
        sender_user = instance.sender
        message = instance
        
        # Notify all members of the chat room except the sender
        for member in chat_room.members.exclude(id=sender_user.id):
            notification_message = f"New message from {sender_user.username} in {chat_room.name or 'a chat room'}"
            ChatRoomNotification.create_notification(
                chat_room=chat_room,
                user_profile=member.profile,
                message=notification_message
            )
        
        # Notify mentioned users
        mentioned_users = instance.mentioned_users.all()
        mention_message = f"You were mentioned in a message by {sender_user.username}."
        for user in mentioned_users:
            ChatRoomNotification.create_notification(
                chat_room=chat_room,
                user_profile=user.profile,
                message=mention_message
            )

        # Update the chat room with the last message
        chat_room.last_message = message
        chat_room.save()

        # Log the message creation
        logger.info(f'Message created in chat {chat_room.id} by user {sender_user.id}')

@receiver(post_delete, sender=Message)
def update_message_count(sender, instance, **kwargs):
    """
    Updates the message count in the chat room when a message is deleted.
    """
    chat_room = instance.chat_room
    chat_room.message_count -= 1
    chat_room.save()

@receiver(post_save, sender=Reaction)
def send_reaction_notification(sender, instance, created, **kwargs):
    """
    Sends a notification when a reaction is created.
    """
    if created:
        reacted_message = instance.content_object
        if reacted_message:
            chat_room = reacted_message.chat_room
            recipients = chat_room.members.exclude(id=instance.user.id)
            sender = instance.user
            notification_message = f"{sender.username} reacted to your message."
            for recipient in recipients:
                ChatRoomNotification.create_notification(
                    chat_room=chat_room,
                    user_profile=recipient.profile,
                    message=notification_message
                )
        else:
            logger.warning("Reacted message is None")

@receiver(post_save, sender=Share)
def send_share_notification(sender, instance, created, **kwargs):
    """
    Sends a notification when content is shared.
    """
    if created:
        shared_content = instance.content_object
        if shared_content:
            chat_room = shared_content.chat_room
            recipients = instance.shared_to.all()
            sender = instance.user
            notification_message = f"{sender.username} shared content with you."
            for recipient in recipients:
                ChatRoomNotification.create_notification(
                    chat_room=chat_room,
                    user_profile=recipient.profile,
                    message=notification_message
                )
        else:
            logger.warning("Shared content is None")