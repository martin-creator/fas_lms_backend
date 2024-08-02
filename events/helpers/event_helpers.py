from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from events.models import Event, EventRegistration, EventFeedback
# from profiles.models import UserProfile
from  events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

# class Event(models.Model):
#     organizer = models.ForeignKey(UserProfile, related_name='organized_events', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     attachments = GenericRelation(Attachment)
#     categories = models.ManyToManyField(Category, related_name='events')
#     location = models.CharField(max_length=255)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     capacity = models.PositiveIntegerField()
#     attendees = models.ManyToManyField(UserProfile, related_name='events', blank=True)
#     tags = TaggableManager()
#     registration_required = models.BooleanField(default=True)
#     is_online = models.BooleanField(default=False)
#     online_link = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

class EventUtils:
    
    @staticmethod
    def process_event_data(event_data):
        """
        Process event data.
        """
        title = event_data.get('title')
        description = event_data.get('description')
        location = event_data.get('location')
        start_time = event_data.get('start_time')
        end_time = event_data.get('end_time')
        capacity = event_data.get('capacity')
        registration_required = event_data.get('registration_required')
        is_online = event_data.get('is_online')
        online_link = event_data.get('online_link')
        organizer_id = event_data.get('organizer_id')
        categories = event_data.get('categories')
        event_tags = event_data.get('tags')
        attachments = event_data.get('attachments')

        try:
            organizer = User.objects.get(id=organizer_id)
        except ObjectDoesNotExist:
            raise ValidationError('Invalid organizer ID.')
        
        event = Event(
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            capacity=capacity,
            registration_required=registration_required,
            is_online=is_online,
            online_link=online_link,
            organizer=organizer
        )

        return event,event_tags
    
    @staticmethod
    def process_event_update_data(event_id, event_data):
        """
        Process event update data.
        """
        title = event_data.get('title')
        description = event_data.get('description')
        location = event_data.get('location')
        start_time = event_data.get('start_time')
        end_time = event_data.get('end_time')
        capacity = event_data.get('capacity')
        registration_required = event_data.get('registration_required')
        is_online = event_data.get('is_online')
        online_link = event_data.get('online_link')
        organizer_id = event_data.get('organizer_id')
        categories = event_data.get('categories')
        event_tags = event_data.get('tags')
        attachments = event_data.get('attachments')
        
        event = Event.objects.get(id=event_id)

        if title is not None:
            event.title = title

        if description is not None:
            event.description = description

        if location is not None:
            event.location = location

        if start_time is not None:
            event.start_time = start_time

        if end_time is not None:
            event.end_time = end_time

        if capacity is not None:
            event.capacity = capacity

        if registration_required is not None:
            event.registration_required = registration_required

        if is_online is not None:
            event.is_online = is_online

        if online_link is not None:
            event.online_link = online_link

        if organizer is not None:
            try:
                organizer = User.objects.get(id=organizer_id)
                event.organizer = organizer
            except ObjectDoesNotExist:
                raise ValidationError('Invalid organizer ID.')
            
        return event,event_tags



