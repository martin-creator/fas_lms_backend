from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from messaging.settings.messaging_settings import MessagingSettings
from messaging.querying.messaging_query import MessagingQuery
from messaging.reports.messaging_report import MessagingReport
from messaging.services.messaging_services import MessagingService
from messaging.settings.messaging_settings import MessagingSettings



class MessagingController:
        
        def __init__(self):
            self.messaging_query = MessagingQuery()
            self.messaging_report = MessagingReport()
            self.messaging_settings = MessagingSettings()
            self.messaging_service = MessagingService()
        
        def get_all_messages(self):
            """
            Get all messages.
            """
            return self.messaging_service.get_messages()
        
        def get_message(self, message_id):
            """
            Get a specific message.
            """
            return self.messaging_service.get_message(message_id)
        
        def create_message(self, message_data):
            """
            Create a new message.
            """
            return self.messaging_service.create_message(message_data)
        
        def update_message(self, message_id, message_data):
            """
            Update a message.
            """
            return self.messaging_service.update_message(message_id, message_data)
        
        def delete_message(self, message_id):
            """
            Delete a message.
            """
            return self.messaging_service.delete_message(message_id)
        
        def get_messages_by_chat(self, chat_id):
            """
            Get all messages in a specific chat.
            """
            return self.messaging_service.get_messages_by_chat(chat_id)
        
        def get_messages_by_sender(self, sender_id):
            """
            Get all messages sent by a specific user.
            """
            return self.messaging_service.get_messages_by_sender(sender_id)
        
        def mark_message_as_read(self, message_id):
            """
            Mark a message as read.
            """
            return self.messaging_service.mark_message_as_read(message_id)
        
        def edit_message(self, message_id, new_content):
            """
            Edit a message.
            """
            return self.messaging_service.edit_message(message_id, new_content)
        
        def delete_message(self, message_id):
            """
            Delete a message.
            """
            return self.messaging_service.delete_message(message_id)
        
        def get_reply_chain(self, message_id):
            """
            Get the reply chain for a specific message.
            """
            return self.messaging_service.get_reply_chain(message_id)
        
        def get_preview(self, message_id):
            """
            Get a preview of a message.
            """
            return self.messaging_service.get_preview(message_id)
        
        def get_reactions_summary(self, message_id):
            """
            Get a summary of reactions for a specific message.
            """
            return self.messaging_service.get_reactions_summary(message_id)
        
        def get_content(self, message_id):
            """
            Get the content of a message.
            """
            return self.messaging_service.get_content
        
        def get_chat_rooms(self):
            """
            Get all chat rooms.
            """
            return self.messaging_service.get_chat_rooms
        

        def get_chat_room(self, chat_id):
            """
            Get a specific chat room.
            """
            return self.messaging_service.get_chat_room(chat_id)
        
        def create_chat_room(self, chat_room_data):
            """
            Create a new chat room.
            """
            return self.messaging_service.create_chat_room(chat_room_data)
        

        def update_chat_room(self, chat_id, chat_room_data):
            """
            Update a chat room.
            """
            return self.messaging_service.update_chat_room(chat_id, chat_room_data)
        
        
        def delete_chat_room(self, chat_id):
            """
            Delete a chat room.
            """
            return self.messaging_service.delete_chat_room(chat_id)
        
        def add_member_to_chat_room(self, chat_id, user_id):
            """
            Add a member to a chat room.
            """
            return self.messaging_service.add_member_to_chat_room(chat_id, user_id)
        

        def remove_member_from_chat_room(self, chat_id, user_id):
            """
            Remove a member from a chat room.
            """
            return self.messaging_service.remove_member_from_chat_room(chat_id, user_id)
        

        def get_unread_messages_count(self, chat_id, user_id):
            """
            Get the count of unread messages for a user in a chat room.
            """
            return self.messaging_service.get_unread_messages_count(chat_id, user_id)
        

        def get_last_message(self, chat_id):
            """
            Get the last message in a chat room.
            """
            return self.messaging_service.get_last_message(chat_id)
        

        def get_chat_room_notifications(self, chat_id, user_id):
            """
            Get all notifications for a user in a chat room.
            """
            return self.messaging_service.get_chat_room_notifications(chat_id, user_id)
        

        def mark_chat_room_notification_as_read(self, notification_id):
            """
            Mark a chat room notification as read.
            """
            return self.messaging_service.mark_chat_room_notification_as_read(notification_id)
        

        def create_chat_room_notification(self, chat_id, user_id, message):
            """
            Create a new notification for a user in a chat room.
            """
            return self.messaging_service.create_chat_room_notification(chat_id, user_id, message)
        

        def get_unread_notifications(self, chat_id, user_id):
            """
            Get all unread notifications for a user in a chat room.
            """
            return self.messaging_service.get_unread_notifications(chat_id, user_id)
        

        def get_chat_room_messages(self, chat_id):
            """
            Get all messages in a chat room.
            """
            return self.messaging_service.get_chat_room_messages(chat_id)
        

        def get_chat_room_members(self, chat_id):
            """
            Get all members in a chat room.
            """
            return self.messaging_service.get_chat_room_members(chat_id)
        

        def get_chat_room_messages_count(self, chat_id):
            """
            Get the count of messages in a chat room.
            """
            return self.messaging_service.get_chat_room_messages_count(chat_id)
        

        def get_chat_room_unread_messages_count(self, chat_id):
            """
            Get the count of unread messages in a chat room.
            """
            return self.messaging_service.get_chat_room_unread_messages_count(chat_id)
        
