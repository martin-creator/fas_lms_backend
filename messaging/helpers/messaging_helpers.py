from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from messaging.models import ChatRoom, Message, ChatRoomNotification
# from profiles.models import UserProfile
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()



class MessagingHelpers:

    @staticmethod
    def process_chat_room_data(data):
        """
        Process chat room data before saving it to the database.
        """
        members = data.get('members')
        name = data.get('name')

        chat_room = ChatRoom(
            name=name
        )

        return chat_room, members
    


    @staticmethod
    def process_chat_room_data_update(chat_room_id, data):
        """
        Process chat room data before updating it in the database.
        """
        
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        
        name = data.get('name')
        members = data.get('members')

        if name is not None:
            chat_room.name = name

        if members is not None:
            chat_room.members.set(members)

        return chat_room, members
    

    @staticmethod
    def process_message_data(data):
        """
        Process message data before saving it to the database.
        """
        chat_room_id = data.get('chat_room_id')
        sender_id = data.get('sender_id')
        content = data.get('content')
        message_type = data.get('message_type')
        parent_message_id = data.get('parent_message_id')
        is_edited = data.get('is_edited')
        is_deleted = data.get('is_deleted')

        chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender = User.objects.get(id=sender_id)
        parent_message = None
        if parent_message_id:
            parent_message = Message.objects.get(id=parent_message_id)

        message = Message(
            chat_room=chat_room,
            sender=sender,
            content=content,
            message_type=message_type,
            parent_message=parent_message,
            is_edited=is_edited,
            is_deleted=is_deleted
        )

        return message
    

    @staticmethod
    def process_message_data_update(message_id, data):
        """
        Process message data before updating it in the database.
        """
        
        message = Message.objects.get(id=message_id)
        
        content = data.get('content')
        message_type = data.get('message_type')
        parent_message_id = data.get('parent_message_id')
        is_edited = data.get('is_edited')
        is_deleted = data.get('is_deleted')

        if content is not None:
            message.content = content

        if message_type is not None:
            message.message_type = message_type

        if parent_message_id is not None:
            message.parent_message = Message.objects.get(id=parent_message_id)

        if is_edited is not None:
            message.is_edited = is_edited

        if is_deleted is not None:
            message.is_deleted = is_deleted

        return message
    

    @staticmethod
    def process_chat_room_notification_data(data):
        """
        Process chat room notification data before saving it to the database.
        """
        chat_room_id = data.get('chat_room_id')
        user_profile_id = data.get('user_profile_id')
        message = data.get('message')
        read = data.get('read')

        chat_room = ChatRoom.objects.get(id=chat_room_id)
        user_profile = User.objects.get(id=user_profile_id)

        chat_room_notification = ChatRoomNotification(
            chat_room=chat_room,
            user_profile=user_profile,
            message=message,
            read=read
        )

        return chat_room_notification
    

    @staticmethod
    def process_chat_room_notification_data_update(notification_id, data):
        """
        Process chat room notification data before updating it in the database.
        """
        
        chat_room_notification = ChatRoomNotification.objects.get(id=notification_id)
        
        message = data.get('message')
        read = data.get('read')

        if message is not None:
            chat_room_notification.message = message

        if read is not None:
            chat_room_notification.read = read

        return chat_room_notification


    




