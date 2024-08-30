from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from messaging.settings.messaging_settings import MessagingSettings
from messaging.querying.messaging_query import MessagingQuery
from messaging.helpers.messaging_helpers import MessagingHelpers
from messaging.reports.messaging_report import MessagingReport



# class ChatRoom(models.Model):
#     roomId = ShortUUIDField()
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms', db_index=True)
#     name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def add_member(self, user):
#         if user not in self.members.all():
#             self.members.add(user)
            
#     def remove_member(self, user):
#         if user in self.members.all():
#             self.members.remove(user)

#     def get_unread_messages_count(self, user):
#         return self.contained_messages.filter(is_read=False, sender=user).count()

#     def get_last_message(self):
#         return self.contained_messages.order_by('timestamp').last()

#     def __str__(self):
#         return self.name if self.name else self.roomId

# class Message(models.Model):
#     TEXT = 'text'
#     IMAGE = 'image'
#     VIDEO = 'video'
#     AUDIO = 'audio'
#     FILE = 'file'

#     MESSAGE_TYPE_CHOICES = [
#         (TEXT, 'Text Message'),
#         (IMAGE, 'Image Message'),
#         (VIDEO, 'Video Message'),
#         (AUDIO, 'Audio Message'),
#         (FILE, 'File Attachment'),
#     ]
    
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='contained_messages', db_index=True)
#     sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages_in_chat', db_index=True)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)
#     message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
#     attachments = GenericRelation(Attachment, related_name='attached_to_messages')
#     parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply_messages')
#     is_edited = models.BooleanField(default=False)
#     is_deleted = models.BooleanField(default=False)
#     reactions = GenericRelation(Reaction, related_name='reacted_to_messages')
#     shares = GenericRelation(Share, related_name='shared_messages')
    
    
#     def __str__(self):
#         return f"{self.sender.username}: {self.get_preview()}"

#     def mark_as_read(self):
#         self.is_read = True
#         self.save(update_fields=['is_read'])

#     def edit_message(self, new_content):
#         self.content = new_content
#         self.is_edited = True
#         self.save(update_fields=['content', 'is_edited'])
        
#     def delete_message(self):
#         self.is_deleted = True
#         self.content = 'This message was deleted'
#         self.save(update_fields=['is_deleted', 'content'])

#     def get_reply_chain(self):
#         replies = []
#         current = self
#         while current:
#             replies.append(current)
#             current = current.parent_message
#         return replies
    
#     def has_attachments(self):
#         return self.attachments.exists()

#     def get_preview(self):
#         """Provides a preview of the message content based on type."""
#         if self.message_type == self.TEXT:
#             return self.content[:20] if self.content else "No preview"
#         elif self.message_type in [self.IMAGE, self.VIDEO, self.AUDIO, self.FILE]:
#             return f"{self.message_type.capitalize()} message"
#         return "Unknown message type"
    
#     def get_reactions_summary(self):
#         summary = {}
#         for choice in dict(Reaction.REACTION_CHOICES).keys():
#             summary[choice] = self.reactions.filter(type=choice).count()
#         return summary

#     def get_content(self):
#         """Returns the content based on message type."""
#         if self.message_type == self.TEXT:
#             return self.content
#         elif self.message_type == self.IMAGE:
#             return self.attachments.filter(attachment_type=Attachment.PHOTO).first().file.url if self.attachments.filter(attachment_type=Attachment.PHOTO).exists() else None
#         elif self.message_type == self.VIDEO:
#             return self.attachments.filter(attachment_type=Attachment.VIDEO).first().file.url if self.attachments.filter(attachment_type=Attachment.VIDEO).exists() else None
#         elif self.message_type == self.AUDIO:
#             return self.attachments.filter(attachment_type=Attachment.AUDIO).first().file.url if self.attachments.filter(attachment_type=Attachment.AUDIO).exists() else None
#         elif self.message_type == self.FILE:
#             return self.attachments.filter(attachment_type=Attachment.DOCUMENT).first().file.url if self.attachments.filter(attachment_type=Attachment.DOCUMENT).exists() else None
#         return None
    
# class ChatRoomNotification(models.Model):
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='notifications_for_chat', db_index=True)
#     user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications_in_chat_rooms', db_index=True)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     read = models.BooleanField(default=False)

#     def __str__(self):
#         return f'{self.user_profile.user.username} received a notification for {self.chat_room.name}'
    
#     def mark_as_read(self):
#         self.read = True
#         self.save(update_fields=['read'])

#     @classmethod
#     def create_notification(cls, chat_room, user_profile, message):
#         return cls.objects.create(chat_room=chat_room, user_profile=user_profile, message=message)

#     @classmethod
#     def get_unread_notifications(cls, chat_room, user_profile):
#         return cls.objects.filter(chat_room=chat_room, user_profile=user_profile, read=False)



# Generate CRUD services for all the models in the messaging app.
# Include all the class methods for each model into the services


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
    
    