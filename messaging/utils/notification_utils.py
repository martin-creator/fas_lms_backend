import logging
from messaging.models import ChatRoomNotification
from profiles.models import UserProfile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
        
    @staticmethod
    def send_notification_to_user(user_profile: UserProfile, message: str):
        """
        Sends a notification to a user.

        Args:
            user_profile (UserProfile): The profile of the user to notify.
            message (str): The message content to include in the notification.

        Raises:
            ValueError: If the user's email is not set.
        """
        if not user_profile.user.email:
            raise ValueError(f"User {user_profile.id} does not have an email address set.")

        # Compose email subject and body
        subject = "New Message Notification"
        html_message = render_to_string('email/notification_email.html', {
            'user': user_profile.user,
            'message': message,
        })
        plain_message = strip_tags(html_message)

        try:
            # Send the email
            send_mail(
                subject,
                plain_message,
                'no-reply@yourdomain.com',  # Sender email
                [user_profile.user.email],
                html_message=html_message,
            )
            print(f"Notification sent to {user_profile.user.email}")
        except Exception as e:
            print(f"Failed to send notification to {user_profile.user.email}: {e}")
            # Log the exception
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send notification to {user_profile.user.email}: {e}")
