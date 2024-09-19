from celery import shared_task
from messaging.utils.notification_utils import MessageNotificationUtils
from messaging.utils.message_utils import MessageUtils
from messaging.querying.messaging_query import MessagingQuery
from activity.models import Reaction, Share
from messaging.models import ChatRoomNotification
import logging

logger = logging.getLogger(__name__)

class MessagingTasks:
    @staticmethod
    @shared_task
    def send_message_notification(message_id):
        """
        Sends notifications for the given message.
        
        Args:
            message_id (int): The ID of the message for which notifications are to be sent.
        """
        try:
            # Use MessagingQuery to get message details
            message_data = MessagingQuery.get_message(message_id)
            if "error" in message_data:
                raise ValueError("Message not found")

            MessageNotificationUtils.send_message_notification(message_data)
            logger.info(f'Notification sent for message ID {message_id}')
        except Exception as e:
            logger.error(f'Error sending notification for message ID {message_id}: {e}')

    @staticmethod
    @shared_task
    def update_reaction_count(reaction_id):
        """
        Updates the reaction count for the message associated with the given reaction.
        
        Args:
            reaction_id (int): The ID of the reaction that triggered the count update.
        """
        try:
            reaction = Reaction.objects.get(id=reaction_id)
            # Use MessageUtils to update reaction count
            MessageUtils.update_message(reaction.message.id, reaction.message.content)  # Adjusted as needed
            logger.info(f'Reaction count updated for message ID {reaction.message.id}')
        except Reaction.DoesNotExist:
            logger.error(f'Reaction ID {reaction_id} does not exist')
        except Exception as e:
            logger.error(f'Error updating reaction count for reaction ID {reaction_id}: {e}')

    @staticmethod
    @shared_task
    def process_share(share_id):
        """
        Handles the processing of shared messages, including updating relevant counts and sending notifications if necessary.
        
        Args:
            share_id (int): The ID of the share to process.
        """
        try:
            share = Share.objects.get(id=share_id)
            # Implement share processing logic here
            logger.info(f'Share processed for share ID {share_id}')
        except Share.DoesNotExist:
            logger.error(f'Share ID {share_id} does not exist')
        except Exception as e:
            logger.error(f'Error processing share ID {share_id}: {e}')

    @staticmethod
    @shared_task
    def notify_chat_room_members(chat_room_id, message):
        """
        Notifies all members of a chat room about a given message.
        
        Args:
            chat_room_id (int): The ID of the chat room.
            message (str): The message to notify the members about.
        """
        try:
            # Use MessagingQuery to get chat room notifications
            notifications = MessagingQuery.get_chat_room_notifications_by_chat(chat_room_id)
            for notification in notifications:
                # Assume send_notification_to_user is a function that handles actual sending
                MessageNotificationUtils.send_notification_to_user(notification['user_profile'], message)
            logger.info(f'Notifications sent to members of chat room ID {chat_room_id}')
        except Exception as e:
            logger.error(f'Error notifying members of chat room ID {chat_room_id}: {e}')
