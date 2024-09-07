from django.db import models
from .querying.messaging_querysets import ChatRoomQuerySet, MessageQuerySet, ChatRoomNotificationQuerySet


class ChatRoomManager(models.Manager):
    def get_queryset(self):
        return ChatRoomQuerySet(self.model, using=self._db)

    def get_user_rooms(self, user):
        return self.get_queryset().for_user(user)
    
    
class MessageManager(models.Manager):
    def get_queryset(self):
        return MessageQuerySet(self.model, using=self._db)

    def get_unread(self, user):
        return self.get_queryset().unread(user)
    
    def get_in_room(self, room):
        return self.get_queryset().in_chat_room(room)
    
    
class ChatRoomNotificationManager(models.Manager):
    def get_queryset(self):
        return ChatRoomNotificationQuerySet(self.model, using=self._db)

    def get_unread(self, user_profile):
        return self.get_queryset().unread(user_profile)
