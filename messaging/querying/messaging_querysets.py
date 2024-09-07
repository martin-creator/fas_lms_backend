from django.db import models
from django.db.models import Q

class ChatRoomQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(members=user)

    def unread_messages(self, user):
        return self.filter(contained_messages__is_read=False, contained_messages__sender=user)


class MessageQuerySet(models.QuerySet):
    def unread(self, user):
        return self.filter(is_read=False, sender=user)

    def in_chat_room(self, room):
        return self.filter(chat_room=room)


class ChatRoomNotificationQuerySet(models.QuerySet):
    def unread(self, user_profile):
        return self.filter(user_profile=user_profile, read=False)