import logging
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from chat.models import Message, ChatRoom
from profiles.models import UserProfile
from chat.serializers import MessageSerializer
from .message_notification_utils import MessageNotificationUtils

logger = logging.getLogger(__name__)

class MessageUtils:

    @staticmethod
    def create_message(chat_id, sender_id, content):
        try:
            chat = ChatRoom.objects.get(id=chat_id)
            sender = UserProfile.objects.get(id=sender_id)

            # Check permissions
            if not PermissionChecker.user_can_send_message(sender, chat):
                raise PermissionDenied("You do not have permission to send messages in this chat.")

            message = Message(chat=chat, sender=sender, content=content, created_at=timezone.now())
            message.save()

            # Send notification to other chat members
            MessageNotificationUtils.send_message_notification(message)

            logger.info(f'Message created in chat {chat_id} by user {sender_id}')
            return message
        except Exception as e:
            logger.error(f"Failed to create message: {e}")
            raise

    @staticmethod
    def update_message(message_id, content):
        try:
            message = Message.objects.get(id=message_id)
            message.content = content
            message.save()

            logger.info(f'Message {message_id} updated')
            return message
        except Message.DoesNotExist:
            logger.error(f"Message {message_id} not found")
            raise ValueError("Message not found")
        except Exception as e:
            logger.error(f"Failed to update message: {e}")
            raise

    @staticmethod
    def delete_message(message_id):
        try:
            message = Message.objects.get(id=message_id)
            message.delete()

            logger.info(f'Message {message_id} deleted')
        except Message.DoesNotExist:
            logger.error(f"Message {message_id} not found")
            raise ValueError("Message not found")
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
            raise

    @staticmethod
    def get_message(message_id):
        try:
            message = Message.objects.get(id=message_id)
            return MessageSerializer(message).data
        except Message.DoesNotExist:
            logger.error(f"Message {message_id} not found")
            raise ValueError("Message not found")
        except Exception as e:
            logger.error(f"Failed to retrieve message: {e}")
            raise

    @staticmethod
    def get_messages_for_chat(chat_id):
        try:
            messages = Message.objects.filter(chat_id=chat_id).order_by('created_at')
            return MessageSerializer(messages, many=True).data
        except Exception as e:
            logger.error(f"Failed to retrieve messages for chat {chat_id}: {e}")
            raise

    @staticmethod
    def mark_message_as_read(message_id, recipient_id):
        try:
            message = Message.objects.get(id=message_id)
            recipient = UserProfile.objects.get(id=recipient_id)

            # Assuming a read receipt model exists
            message.read_by.add(recipient)
            message.save()

            # Send read receipt notification
            MessageNotificationUtils.send_message_read_receipt_notification(message, recipient)

            logger.info(f'Message {message_id} marked as read by user {recipient_id}')
        except Message.DoesNotExist:
            logger.error(f"Message {message_id} not found")
            raise ValueError("Message not found")
        except UserProfile.DoesNotExist:
            logger.error(f"User {recipient_id} not found")
            raise ValueError("User not found")
        except Exception as e:
            logger.error(f"Failed to mark message as read: {e}")
            raise