from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from messaging.settings.messaging_settings import MessagingSettings
from messaging.querying.messaging_query import MessagingQuery
from messaging.helpers.messaging_helpers import MessagingHelpers
from messaging.reports.messaging_report import MessagingReport



class MessagingService:
    # Message services
    @staticmethod
    def get_messages():
        """
        Get all messages.
        """
        messages = MessagingQuery.get_messages()
        return messages
    
    @staticmethod
    def get_message(message_id):
        """
        Get a specific message.
        """
        message = MessagingQuery.get_message(message_id)
        return message
    

    @staticmethod
    def create_message(message_data):
        """
        Create a new message.
        """
        message = MessagingHelpers.process_message_data(message_data)
        message.save()

        serializer = MessageSerializer(message)

        return serializer.data
    

    @staticmethod
    def update_message(message_id, message_data):
        """
        Update a message.
        """
        message = MessagingHelpers.process_message_data_update(message_id, message_data)
        message.save()

        serializer = MessageSerializer(message)

        return serializer.data
    

    @staticmethod
    def delete_message(message_id):
        """
        Delete a message.
        """
        message = MessagingQuery.get_message(message_id)
        message.delete()

        return True
    

    @staticmethod
    def get_messages_by_chat(chat_id):
        """
        Get all messages in a specific chat.
        """
        messages = MessagingQuery.get_messages_by_chat(chat_id)
        return messages
    
    @staticmethod
    def get_messages_by_sender(sender_id):
        """
        Get all messages sent by a specific user.
        """
        messages = MessagingQuery.get_messages_by_sender(sender_id)
        return messages
    
    @staticmethod
    def mark_message_as_read(message_id):
        """
        Mark a message as read.
        """
        message = MessagingQuery.get_message(message_id)
        message.mark_as_read()

        return True
    

    @staticmethod
    def edit_message(message_id, new_content):
        """
        Edit a message.
        """
        message = MessagingQuery.get_message(message_id)
        message.edit_message(new_content)

        return True
    
    @staticmethod
    def delete_message(message_id):
        """
        Delete a message.
        """
        message = MessagingQuery.get_message(message_id)
        message.delete_message()

        return True
    

    @staticmethod
    def get_reply_chain(message_id):
        """
        Get the reply chain for a specific message.
        """
        message = MessagingQuery.get_message(message_id)
        replies = message.get_reply_chain()

        return replies
    

    @staticmethod
    def get_preview(message_id):
        """
        Get a preview of a message.
        """
        message = MessagingQuery.get_message(message_id)
        preview = message.get_preview()

        return preview
    

    @staticmethod
    def get_reactions_summary(message_id):
        """
        Get a summary of reactions for a specific message.
        """
        message = MessagingQuery.get_message(message_id)
        summary = message.get_reactions_summary()

        return summary
    

    @staticmethod
    def get_content(message_id):
        """
        Get the content of a message.
        """
        message = MessagingQuery.get_message(message_id)
        content = message.get_content()

        return content
    


    # ChatRoom services
    @staticmethod
    def get_chat_rooms():
        """
        Get all chat rooms.
        """
        chat_rooms = MessagingQuery.get_chat_rooms()
        return chat_rooms
    

    @staticmethod
    def get_chat_room(chat_id):
        """
        Get a specific chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        return chat_room
    

    @staticmethod
    def create_chat_room(chat_room_data):
        """
        Create a new chat room.
        """
        chat_room = MessagingHelpers.process_chat_room_data(chat_room_data)
        chat_room.save()

        serializer = ChatRoomSerializer(chat_room)

        return serializer.data
    

    @staticmethod
    def update_chat_room(chat_id, chat_room_data):
        """
        Update a chat room.
        """
        chat_room = MessagingHelpers.process_chat_room_data_update(chat_id, chat_room_data)
        chat_room.save()

        serializer = ChatRoomSerializer(chat_room)

        return serializer.data
    

    @staticmethod
    def delete_chat_room(chat_id):
        """
        Delete a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        chat_room.delete()

        return True
    

    @staticmethod
    def add_member_to_chat_room(chat_id, user_id):
        """
        Add a member to a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        chat_room.add_member(user)

        return True
    

    @staticmethod
    def remove_member_from_chat_room(chat_id, user_id):
        """
        Remove a member from a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        chat_room.remove_member(user)

        return True
    

    @staticmethod
    def get_unread_messages_count(chat_id, user_id):
        """
        Get the count of unread messages for a user in a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        count = chat_room.get_unread_messages_count(user)

        return count
    

    @staticmethod
    def get_last_message(chat_id):
        """
        Get the last message in a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        last_message = chat_room.get_last_message()

        return last_message
    

    @staticmethod
    def get_chat_room_notifications(chat_id, user_id):
        """
        Get all notifications for a user in a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        notifications = MessagingQuery.get_chat_room_notifications(chat_room, user)

        return notifications
    

    @staticmethod
    def mark_chat_room_notification_as_read(notification_id):
        """
        Mark a chat room notification as read.
        """
        notification = MessagingQuery.get_chat_room_notification(notification_id)
        notification.mark_as_read()

        return True
    

    @staticmethod
    def create_chat_room_notification(chat_id, user_id, message):
        """
        Create a new notification for a user in a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        notification = ChatRoomNotification.create_notification(chat_room, user, message)

        return True
    

    @staticmethod
    def get_unread_notifications(chat_id, user_id):
        """
        Get all unread notifications for a user in a chat room.
        """
        chat_room = MessagingQuery.get_chat_room(chat_id)
        user = MessagingQuery.get_user(user_id)

        notifications = ChatRoomNotification.get_unread_notifications(chat_room, user)

        return notifications
    

    @staticmethod
    def get_chat_room_messages(chat_id):
        """
        Get all messages in a chat room.
        """
        messages = MessagingQuery.get_chat_room_messages(chat_id)
        return messages
    

    @staticmethod
    def get_chat_room_members(chat_id):
        """
        Get all members in a chat room.
        """
        members = MessagingQuery.get_chat_room_members(chat_id)
        return members
    

    @staticmethod
    def get_chat_room_messages_count(chat_id):
        """
        Get the count of messages in a chat room.
        """
        count = MessagingQuery.get_chat_room_messages_count(chat_id)
        return count
    

    @staticmethod
    def get_chat_room_unread_messages_count(chat_id):
        """
        Get the count of unread messages in a chat room.
        """
        count = MessagingQuery.get_chat_room_unread_messages_count(chat_id)
        return count
    
    