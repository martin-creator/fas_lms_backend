from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from companies.models import Company, CompanyUpdate
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from companies.settings.companies_settings import CompanySettings
from companies.querying.companies_query import CompanyQuery
from companies.helpers.companies_helpers import CompanyHelpers
from companies.utils import UserUtils, DateTimeUtils
from companies.reports.companies_report import CompanyReport


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







#     @staticmethod
#     def get_event(event_id):
#         """
#         Get a specific event.
#         """
#         event = EventQuery.get_event(event_id)
#         return event

#     @staticmethod
#     def create_event(event_data):
#         """
#         Create a new event.
#         """

#         event, event_tags = EventQuery.process_event_data(event_data)
#         event.save()

#         if event_tags:
#             event.tags.set(event_tags)

#         serializer = EventSerializer(event)

#         return serializer.data
    

#     @staticmethod
#     def update_event(event_id, event_data):
#         """
#         Update an event.
#         """

#         # event = EventQuery.get_event(event_id)
#         event, event_tags = EventQuery.process_event_update_data(event_id, event_data)
#         event.save()

#         if event_tags:
#             event.tags.set(event_tags)

#         serializer = EventSerializer(event)

#         return serializer.data
    

#     @staticmethod
#     def delete_event(event_id):
#         """
#         Delete an event.
#         """
#         event = EventQuery.get_event(event_id)
#         event.delete()

#         return True
    
    
#     @staticmethod
#     def delete_all_events():
#         """
#         Delete all events.
#         """
#         events = EventQuery.get_events()
#         events.delete()

#         return True
    

#     @staticmethod
#     def get_event_report(event_id):
#         """
#         Get a report for a specific event.
#         """
#         event = EventQuery.get_event(event_id)
#         report = EventReport.get_event_report(event)

#         return report
    

#     @staticmethod
#     def get_attendee_report(attendee_id):
#         """
#         Get a report for a specific attendee.
#         """
#         attendee = UserUtils.get_current_user(attendee_id)
#         report = EventReport.get_attendee_report(attendee)

#         return report
    
#     @staticmethod
#     def register_for_event(event_id, attendee_id):
#         """
#         Register for an event.
#         """
#         event = EventQuery.get_event(event_id)
#         attendee = UserUtils.get_current_user(attendee_id)

#         registration = EventRegistration(event=event, attendee=attendee)
#         registration.save()

#         return True


#     @staticmethod
#     def unregister_from_event(event_id, attendee_id):
#         """
#         Unregister from an event.
#         """
#         registration = EventQuery.get_event_registration(event_id, attendee_id)
#         registration.delete()

#         return True
    

#     @staticmethod
#     def provide_event_feedback(event_id, attendee_id, feedback_data):
#         """
#         Provide feedback for an event.
#         """
#         event = EventQuery.get_event(event_id)
#         attendee = UserUtils.get_current_user(attendee_id)

#         feedback = EventFeedback(event=event, attendee=attendee, **feedback_data)
#         feedback.save()

#         return True

    
#     @staticmethod
#     def get_events_by_organizer(organizer_id):
#         """
#         Get all events organized by a specific organizer.
#         """
#         events = EventQuery.get_events_by_organizer(organizer_id)
#         return events
    

#     @staticmethod
#     def get_events_by_attendee(attendee_id):
#         """
#         Get all events attended by a specific attendee.
#         """
#         events = EventQuery.get_events_by_attendee(attendee_id)
#         return events
    

#     @staticmethod   
#     def get_event_attendees(event_id):
#         """
#         Get all attendees for an event.
#         """
#         attendees = EventQuery.get_event_attendees(event_id)
#         return attendees


#     @staticmethod
#     def get_event_registrations(event_id):
#         """
#         Get all registrations for a specific event.
#         """
#         registrations = EventQuery.get_event_registrations(event_id)
#         return registrations
    

#     @staticmethod
#     def get_event_feedbacks(event_id):
#         """
#         Get all feedbacks for a specific event.
#         """
#         feedbacks = EventQuery.get_event_feedbacks(event_id)
#         return feedbacks
    

#     @staticmethod
#     def get_events_monthly_report():
#         """
#         Get a monthly report for all events.
#         """
#         report = EventReport.get_events_monthly_report()
#         return report
    

    
    
    

    

    


        