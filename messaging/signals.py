from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Message, ChatRoom
from notifications.models import Notification
from activity.models import Reaction, Share

from django.utils import timezone

from .utils.notification_utils import MessageUtils

@receiver(post_save, sender=Message)
def send_chat_message_notification(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat
        message = instance
        sender_user = instance.sender
        for member in chat.members.exclude(id=sender_user.id):
            MessageUtils.send_message_notification(chat, member, message)

# Signal to send notifications when a new message is sent
@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        chat_room = instance.chat
        recipients = chat_room.members.exclude(id=instance.sender.id)
        sender = instance.sender
        notification_message = f"You have a new message from {sender.username}."
        for recipient in recipients:
            Notification.objects.create(
                recipient=recipient,
                content=notification_message,
                notification_type_id=1,
                url=f"/chat/{chat_room.id}/",
                timestamp=timezone.now()
            )

# Signal to send notifications when a user is mentioned in a message
@receiver(post_save, sender=Message)
def send_mention_notification(sender, instance, created, **kwargs):
    if created:
        mentioned_users = instance.mentioned_users.all()
        sender = instance.sender
        notification_message = f"You were mentioned in a message by {sender.username}."
        for user in mentioned_users:
            Notification.objects.create(
                recipient=user,
                content=notification_message,
                notification_type_id=1,
                url=f"/chat/{instance.chat.id}/",
                timestamp=timezone.now()
            )

# Signal to update chat room details when a new message is sent
@receiver(post_save, sender=Message)
def update_chat_room(sender, instance, created, **kwargs):
    if created:
        chat_room = instance.chat
        chat_room.last_message = instance
        chat_room.save()

# Signal to send notifications when a new chat room is created
@receiver(post_save, sender=ChatRoom)
def send_chat_room_notification(sender, instance, created, **kwargs):
    if created:
        members = instance.members.all()
        notification_message = f"You have been added to a new chat room."
        for member in members:
            Notification.objects.create(
                recipient=member,
                content=notification_message,
                notification_type_id=1, 
                url=f"/chat/{instance.id}/",
                timestamp=timezone.now()
            )

# Signal to update message count when a message is deleted
@receiver(post_delete, sender=Message)
def update_message_count(sender, instance, **kwargs):
    chat_room = instance.chat
    chat_room.message_count -= 1
    chat_room.save()

# Signal to send notifications when a message is reacted to
# @receiver(post_save, sender=Reaction)
# def send_reaction_notification(sender, instance, created, **kwargs):
#     if created:
#         reacted_message = instance.message
#         if reacted_message is not None:
#             chat_room = reacted_message.chat
#             recipients = chat_room.members.exclude(id=instance.user.id)
#             sender = instance.user
#             notification_message = f"{sender.username} reacted to your message."
#             for recipient in recipients:
#                 Notification.objects.create(
#                     recipient=recipient,
#                     content=notification_message,
#                     notification_type_id=1, 
#                     url=f"/chat/{chat_room.id}/", 
#                     timestamp=timezone.now()
#                 )
#         else:
#             print("Reacted message is None")

# Signal to update reaction count when a new reaction is added
# @receiver(post_save, sender=Reaction)
# def update_reaction_count(sender, instance, created, **kwargs):
#     if created:
#         reacted_message = instance.message
#         print("Reacted message:", reacted_message)
#         if reacted_message is not None:
#             if hasattr(reacted_message, 'reaction_count'):
#                 reacted_message.reaction_count += 1
#                 reacted_message.save()
#             else:
#                 print("Reacted message does not have a reaction_count attribute")
#         else:
#             print("Reacted message is None")