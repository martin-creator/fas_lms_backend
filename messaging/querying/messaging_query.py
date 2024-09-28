from django.db.models import Count, Q
from django.utils import timezone
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer


class MessagingQuery:

    @staticmethod
    def get_messages() -> list:
        """
        Get all messages.
        """
        messages = Message.objects.all()
        return MessageSerializer(messages, many=True).data

    @staticmethod
    def get_message(message_id: int) -> dict:
        """
        Get a specific message.
        """
        try:
            message = Message.objects.get(id=message_id)
            return MessageSerializer(message).data
        except Message.DoesNotExist:
            return {"error": "Message not found"}

    @staticmethod
    def get_messages_by_chat(chat_id: int) -> list:
        """
        Get all messages in a specific chat.
        """
        messages = Message.objects.get_in_room(chat_id)
        return MessageSerializer(messages, many=True).data

    @staticmethod
    def get_messages_by_sender(sender_id: int) -> list:
        """
        Get all messages sent by a specific user.
        """
        messages = Message.objects.filter(sender_id=sender_id)
        return MessageSerializer(messages, many=True).data

    @staticmethod
    def get_messages_by_content(content: str) -> list:
        """
        Get all messages containing specific content.
        """
        messages = Message.objects.filter(content__icontains=content)
        return MessageSerializer(messages, many=True).data

    @staticmethod
    def get_chat_rooms() -> list:
        """
        Get all chat rooms.
        """
        chat_rooms = ChatRoom.objects.all()
        return ChatRoomSerializer(chat_rooms, many=True).data

    @staticmethod
    def get_chat_room(chat_room_id: int) -> dict:
        """
        Get a specific chat room.
        """
        try:
            chat_room = ChatRoom.objects.get(id=chat_room_id)
            return ChatRoomSerializer(chat_room).data
        except ChatRoom.DoesNotExist:
            return {"error": "Chat room not found"}

    @staticmethod
    def get_chat_rooms_by_member(member_id: int) -> list:
        """
        Get all chat rooms that include a specific member.
        """
        chat_rooms = ChatRoom.objects.get_user_rooms(member_id)
        return ChatRoomSerializer(chat_rooms, many=True).data

    @staticmethod
    def get_chat_rooms_by_name(name: str) -> list:
        """
        Get all chat rooms with a specific name.
        """
        chat_rooms = ChatRoom.objects.filter(name__icontains=name)
        return ChatRoomSerializer(chat_rooms, many=True).data

    @staticmethod
    def get_chat_room_notifications() -> list:
        """
        Get all chat room notifications.
        """
        notifications = ChatRoomNotification.objects.all()
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_notifications_by_user(user_id: int) -> list:
        """
        Get all chat room notifications for a specific user.
        """
        notifications = ChatRoomNotification.objects.get_unread(user_id)
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_notifications_by_chat(chat_id: int) -> list:
        """
        Get all chat room notifications for a specific chat.
        """
        notifications = ChatRoomNotification.objects.filter(chat_id=chat_id)
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_notifications_by_user_and_chat(user_id: int, chat_id: int) -> list:
        """
        Get all chat room notifications for a specific user and chat.
        """
        notifications = ChatRoomNotification.objects.filter(user_id=user_id, chat_id=chat_id)
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_notifications_by_user_and_chat_and_type(user_id: int, chat_id: int, notification_type: str) -> list:
        """
        Get all chat room notifications for a specific user, chat, and notification type.
        """
        notifications = ChatRoomNotification.objects.filter(user_id=user_id, chat_id=chat_id, notification_type=notification_type)
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_notifications_by_type(notification_type: str) -> list:
        """
        Get all chat room notifications of a specific type.
        """
        notifications = ChatRoomNotification.objects.filter(notification_type=notification_type)
        return ChatRoomNotificationSerializer(notifications, many=True).data

    @staticmethod
    def get_chat_room_messages_count(chat_id: int) -> int:
        """
        Get the count of messages in a specific chat room.
        """
        return Message.objects.get_in_room(chat_id).count()

    @staticmethod
    def get_chat_room_unread_messages_count(chat_id: int) -> int:
        """
        Get the number of unread messages in a specific chat room.
        """
        return Message.objects.get_in_room(chat_id).filter(is_read=False).count()

    @staticmethod
    def get_unread_notifications_for_user(user_profile) -> list:
        """
        Get all unread notifications for a user.
        """
        notifications = ChatRoomNotification.objects.unread(user_profile)
        return ChatRoomNotificationSerializer(notifications, many=True).data
