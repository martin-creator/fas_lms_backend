from messaging.models import ChatRoom, Message
from django.conf import settings


class MessagingServicesController:
    def __init__(self):
        pass

    def create_chat_room(self, members, name=None):
        chat_room = ChatRoom(name=name)
        chat_room.save()
        chat_room.members.add(*members)
        return chat_room

    def send_message(self, chat_room, sender, content, message_type='text', attachments=None):
        message = Message(
            chat=chat_room,
            sender=sender,
            content=content,
            message_type=message_type,
        )
        message.save()
        if attachments:
            message.attachments.add(*attachments)
        return message

    def get_chat_history(self, chat_room):
        return Message.objects.filter(chat=chat_room).order_by('timestamp')

    def mark_message_as_read(self, message_id):
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        return message

    def delete_message(self, message_id):
        message = Message.objects.get(id=message_id)
        message.is_deleted = True
        message.save()
        return message
