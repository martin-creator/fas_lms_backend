from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from messaging.querying.messaging_query import MessagingQuery


class MessagingReport:
    
        @staticmethod
        def get_messages_report():
            """
            Get a report for all messages.
            """
            messages = MessagingQuery.get_messages()
            return messages
        
        @staticmethod
        def get_message_report(message_id):
            """
            Get a report for a specific message.
            """
            message = MessagingQuery.get_message(message_id)
            return message
        
        @staticmethod
        def get_messages_by_chat_report(chat_id):
            """
            Get a report for all messages in a specific chat.
            """
            messages = MessagingQuery.get_messages_by_chat(chat_id)
            return messages
        
        @staticmethod
        def get_messages_by_sender_report(sender_id):
            """
            Get a report for all messages sent by a specific user.
            """
            messages = MessagingQuery.get_messages_by_sender(sender_id)
            return messages
        
        @staticmethod
        def get_messages_by_content_report(content):
            """
            Get a report for all messages with a specific content.
            """
            messages = MessagingQuery.get_messages_by_content(content)
            return messages
        
        @staticmethod
        def get_chat_rooms_report():
            """
            Get a report for all chat rooms.
            """
            chat_rooms = MessagingQuery.get_chat_rooms()
            return chat_rooms
        
