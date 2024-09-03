from django.db.models import Count, Q
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from django.utils import timezone


class MessagingQuery:
    
        @staticmethod
        def get_messages():
            """
            Get all messages.
            """
            messages = Message.objects.all()
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
    
        @staticmethod
        def get_message(message_id):
            """
            Get a specific message.
            """
            message = Message.objects.get(id=message_id)
            serializer = MessageSerializer(message)
            return serializer.data
    
        @staticmethod
        def get_messages_by_chat(chat_id):
            """
            Get all messages in a specific chat.
            """
            messages = Message.objects.filter(chat_id=chat_id)
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
    
        @staticmethod
        def get_messages_by_sender(sender_id):
            """
            Get all messages sent by a specific user.
            """
            messages = Message.objects.filter(sender_id=sender_id)
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
    
        @staticmethod
        def get_messages_by_content(content):
            """
            Get all messages with a specific content.
            """
            messages = Message.objects.filter(content=content)
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
    
        @staticmethod
        def get_chat_rooms():
            """
            Get all chat rooms.
            """
            chat_rooms = ChatRoom.objects.all()
            serializer = ChatRoomSerializer(chat_rooms, many=True)
            return serializer.data
    
        @staticmethod
        def get_chat_room(chat_room_id):
            """
            Get a specific chat room.
            """
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            serializer = ChatRoomSerializer(chat_room)
            return serializer.data
    
        @staticmethod
        def get_chat_rooms_by_member(member_id):
            """
            Get all chat rooms with a specific member.
            """
            chat_rooms = ChatRoom.objects.filter(members=member_id)
            serializer = ChatRoomSerializer(chat_rooms, many=True)
            return serializer.data
    
        @staticmethod
        def get_chat_rooms_by_name(name):
            """
            Get all chat rooms with a specific name.
            """
            chat_rooms = ChatRoom.objects.filter(name=name)
            serializer = ChatRoomSerializer(chat_rooms, many=True)
            return serializer.data
    
        @staticmethod
        def get_chat_room_notifications():
            """
            Get all chat room notifications.
            """
            notifications = ChatRoomNotification.objects.all()
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer
        

        @staticmethod
        def get_chat_room_notifications_by_user(user_id):
            """
            Get all chat room notifications for a specific user.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        
        @staticmethod
        def get_chat_room_notifications_by_chat(chat_id):
            """
            Get all chat room notifications for a specific chat.
            """
            notifications = ChatRoomNotification.objects.filter(chat_id=chat_id)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        
        @staticmethod
        def get_chat_room_notifications_by_user_and_chat(user_id, chat_id):
            """
            Get all chat room notifications for a specific user and chat.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id, chat_id=chat_id)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_user_and_chat_and_type(user_id, chat_id, notification_type):
            """
            Get all chat room notifications for a specific user, chat, and type.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id, chat_id=chat_id, notification_type=notification_type)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_user_and_type(user_id, notification_type):
            """
            Get all chat room notifications for a specific user and type.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id, notification_type=notification_type)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_chat_and_type(chat_id, notification_type):
            """
            Get all chat room notifications for a specific chat and type.
            """
            notifications = ChatRoomNotification.objects.filter(chat_id=chat_id, notification_type=notification_type)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_type(notification_type):
            """
            Get all chat room notifications for a specific type.
            """
            notifications = ChatRoomNotification.objects.filter(notification_type=notification_type)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_user_and_read(user_id, read):
            """
            Get all chat room notifications for a specific user and read status.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id, read=read)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_chat_and_read(chat_id, read):
            """
            Get all chat room notifications for a specific chat and read status.
            """
            notifications = ChatRoomNotification.objects.filter(chat_id=chat_id, read=read)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notifications_by_user_and_chat_and_read(user_id, chat_id, read):
            """
            Get all chat room notifications for a specific user, chat, and read status.
            """
            notifications = ChatRoomNotification.objects.filter(user_id=user_id, chat_id=chat_id, read=read)
            serializer = ChatRoomNotificationSerializer(notifications, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_notification(notification_id):
            """
            Get a specific chat room notification.
            """
            notification = ChatRoomNotification.objects.get(id=notification_id)
            serializer = ChatRoomNotificationSerializer(notification)
            return serializer.data
        

        @staticmethod
        def get_chat_room_messages(chat_id):
            """
            Get all messages in a specific chat room.
            """
            messages = Message.objects.filter(chat_id=chat_id)
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
        

        @staticmethod
        def get_chat_room_members(chat_id):
            """
            Get all members in a specific chat room.
            """
            chat_room = ChatRoom.objects.get(id=chat_id)
            serializer = ChatRoomSerializer(chat_room)
            return serializer.data['members']
        

        @staticmethod
        def get_chat_room_messages_count(chat_id):
            """
            Get the number of messages in a specific chat room.
            """
            count = Message.objects.filter(chat_id=chat_id).count()
            return count
        

        @staticmethod
        def get_chat_room_unread_messages_count(chat_id):
            """
            Get the number of unread messages in a specific chat room.
            """
            count = Message.objects.filter(chat_id=chat_id, read=False).count()
            return count
