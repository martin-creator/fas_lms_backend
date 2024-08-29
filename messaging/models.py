from django.db import models
from shortuuidfield import ShortUUIDField
from posts.models import Post, Comment
from jobs.models import JobListing
from groups.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from activity.models import Attachment, Reaction, Share
from profiles.models import UserProfile
from django.conf import settings

class ChatRoom(models.Model):
    roomId = ShortUUIDField()
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms', db_index=True)
    name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_member(self, user):
        if user not in self.members.all():
            self.members.add(user)
            
    def remove_member(self, user):
        if user in self.members.all():
            self.members.remove(user)

    def get_unread_messages_count(self, user):
        return self.contained_messages.filter(is_read=False, sender=user).count()

    def get_last_message(self):
        return self.contained_messages.order_by('timestamp').last()

    def __str__(self):
        return self.name if self.name else self.roomId

class Message(models.Model):
    TEXT = 'text'
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'
    FILE = 'file'

    MESSAGE_TYPE_CHOICES = [
        (TEXT, 'Text Message'),
        (IMAGE, 'Image Message'),
        (VIDEO, 'Video Message'),
        (AUDIO, 'Audio Message'),
        (FILE, 'File Attachment'),
    ]
    
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='contained_messages', db_index=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages_in_chat', db_index=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=TEXT)
    attachments = GenericRelation(Attachment, related_name='attached_to_messages')
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply_messages')
    is_edited = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    reactions = GenericRelation(Reaction, related_name='reacted_to_messages')
    shares = GenericRelation(Share, related_name='shared_messages')
    
    
    def __str__(self):
        return f"{self.sender.username}: {self.get_preview()}"

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=['is_read'])

    def edit_message(self, new_content):
        self.content = new_content
        self.is_edited = True
        self.save(update_fields=['content', 'is_edited'])
        
    def delete_message(self):
        self.is_deleted = True
        self.content = 'This message was deleted'
        self.save(update_fields=['is_deleted', 'content'])

    def get_reply_chain(self):
        replies = []
        current = self
        while current:
            replies.append(current)
            current = current.parent_message
        return replies
    
    def has_attachments(self):
        return self.attachments.exists()

    def get_preview(self):
        """Provides a preview of the message content based on type."""
        if self.message_type == self.TEXT:
            return self.content[:20] if self.content else "No preview"
        elif self.message_type in [self.IMAGE, self.VIDEO, self.AUDIO, self.FILE]:
            return f"{self.message_type.capitalize()} message"
        return "Unknown message type"
    
    def get_reactions_summary(self):
        summary = {}
        for choice in dict(Reaction.REACTION_CHOICES).keys():
            summary[choice] = self.reactions.filter(type=choice).count()
        return summary

    def get_content(self):
        """Returns the content based on message type."""
        if self.message_type == self.TEXT:
            return self.content
        elif self.message_type == self.IMAGE:
            return self.attachments.filter(attachment_type=Attachment.PHOTO).first().file.url if self.attachments.filter(attachment_type=Attachment.PHOTO).exists() else None
        elif self.message_type == self.VIDEO:
            return self.attachments.filter(attachment_type=Attachment.VIDEO).first().file.url if self.attachments.filter(attachment_type=Attachment.VIDEO).exists() else None
        elif self.message_type == self.AUDIO:
            return self.attachments.filter(attachment_type=Attachment.AUDIO).first().file.url if self.attachments.filter(attachment_type=Attachment.AUDIO).exists() else None
        elif self.message_type == self.FILE:
            return self.attachments.filter(attachment_type=Attachment.DOCUMENT).first().file.url if self.attachments.filter(attachment_type=Attachment.DOCUMENT).exists() else None
        return None
    
class ChatRoomNotification(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='notifications_for_chat', db_index=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications_in_chat_rooms', db_index=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_profile.user.username} received a notification for {self.chat_room.name}'
    
    def mark_as_read(self):
        self.read = True
        self.save(update_fields=['read'])

    @classmethod
    def create_notification(cls, chat_room, user_profile, message):
        return cls.objects.create(chat_room=chat_room, user_profile=user_profile, message=message)

    @classmethod
    def get_unread_notifications(cls, chat_room, user_profile):
        return cls.objects.filter(chat_room=chat_room, user_profile=user_profile, read=False)
