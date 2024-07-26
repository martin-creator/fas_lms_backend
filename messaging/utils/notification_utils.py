import logging
from notifications.utils.notification_utils import NotificationUtils
from profiles.models import UserProfile

logger = logging.getLogger(__name__)

class MessageNotificationUtils:

    @staticmethod
    def send_message_notification(message):
        """
        Sends a notification to all participants of a chat room except the sender.
        """
        chat = message.chat
        sender = message.sender
        recipients = chat.members.exclude(id=sender.id)

        for recipient in recipients:
            notification_data = {
                'recipient': recipient.id,
                'notification_type': 'NEW_MESSAGE',
                'message': f'New message from {sender.username} in {chat.name}: {message.content}',
                'content_object': message,
                'delivery_method': 'in_app',  # Default method, can be customized
            }
            try:
                NotificationUtils.send_notification(notification_data)
                logger.info(f'Notification sent to user {recipient.id} for message {message.id}')
            except Exception as e:
                logger.error(f'Failed to send notification to user {recipient.id} for message {message.id}: {e}')

    @staticmethod
    def send_message_read_receipt_notification(message, recipient):
        """
        Sends a read receipt notification to the sender of the message.
        """
        sender = message.sender

        notification_data = {
            'recipient': sender.id,
            'notification_type': 'MESSAGE_READ_RECEIPT',
            'message': f'Your message in {message.chat.name} was read by {recipient.username}',
            'content_object': message,
            'delivery_method': 'in_app',  # Default method, can be customized
        }
        try:
            NotificationUtils.send_notification(notification_data)
            logger.info(f'Read receipt notification sent to user {sender.id} for message {message.id}')
        except Exception as e:
            logger.error(f'Failed to send read receipt notification to user {sender.id} for message {message.id}: {e}')