import logging
from messaging.models import ChatRoomNotification
from profiles.models import UserProfile

logger = logging.getLogger(__name__)

from messaging.models import ChatRoomNotification

class MessageNotificationUtils:

    @staticmethod
    def send_message_notification(message):
        """
        Sends a notification to all chat members except the sender when a new message is created.
        """
        chat_room = message.chat_room
        sender = message.sender

        # Notify all members of the chat room except the sender
        for member in chat_room.members.exclude(id=sender.id):
            notification_message = f"New message from {sender.username} in {chat_room.name or 'a chat room'}"
            ChatRoomNotification.create_notification(
                chat_room=chat_room,
                user_profile=member.profile,
                content=notification_message
            )

    @staticmethod
    def send_message_read_receipt_notification(message, recipient):
        """
        Sends a notification when a message is read by a recipient.
        """
        chat_room = message.chat_room
        sender = message.sender

        notification_message = f"{recipient.user.username} has read your message in {chat_room.name or 'a chat room'}."
        ChatRoomNotification.create_notification(
            chat_room=chat_room,
            user_profile=sender.profile,
            content=notification_message
        )