from django.db.models import Count, Q
from events.models import Event, EventRegistration, EventFeedback
from events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from django.utils import timezone

# ther serializer should be stored in serializer variable and then return the data
class EventQuery:
    @staticmethod
    def get_events():
        """
        Get all events.
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_event(event_id):
        """
        Get a specific event.
        """
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return serializer.data

    @staticmethod
    def get_event_registrations(event_id):
        """
        Get all registrations for a specific event.
        """
        registrations = EventRegistration.objects.filter(event_id=event_id)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return serializer.data

    @staticmethod
    def get_event_feedbacks(event_id):
        """
        Get all feedbacks for a specific event.
        """
        feedbacks = EventFeedback.objects.filter(event_id=event_id)
        serializer = EventFeedbackSerializer(feedbacks, many=True)
        return serializer.data

    @staticmethod
    def get_events_by_organizer(organizer_id):
        """
        Get all events organized by a specific organizer.
        """
        events = Event.objects.filter(organizer_id=organizer_id)
        serializer = EventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_events_by_attendee(attendee_id):
        """
        Get all events attended by a specific attendee.
        """
        events = Event.objects.filter(attendees=attendee_id)
        serializer = EventSerializer(events, many=True)
        return serializer.data
    
    @staticmethod
    def get_event_registrations_by_attendee(attendee_id):
        """
        Get all event registrations by a specific attendee.
        """
        registrations = EventRegistration.objects.filter(attendee_id=attendee_id)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return serializer.data
    
    @staticmethod
    def get_event_feedbacks_by_attendee(attendee_id):
        """
        Get all event feedbacks by a specific attendee.
        """
        feedbacks = EventFeedback.objects.filter(attendee_id=attendee_id)
        serializer = EventFeedbackSerializer(feedbacks, many=True)
        return serializer.data


    @staticmethod
    def get_events_by_category(category_id):
        """
        Get all events in a specific category.
        """
        events = Event.objects.filter(categories=category_id)
        serializer = EventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_events_by_tag(tag_name):
        """
        Get all events with a specific tag.
        """
        events = Event.objects.filter(tags__name=tag_name)
        serializer = EventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_upcoming_events():
        """
        Get all upcoming events.
        """
        events = Event.objects.filter(start_time__gte=timezone.now())
        serializer = EventSerializer(events, many=True)
        return serializer.data

    @staticmethod
    def get_past_events():
        """
        Get all past events.
        """
        events = Event.objects

    @staticmethod
    def delete_event(event_id):
        """
        Delete a specific event.
        """
        event = Event.objects.get(id=event_id)
        event.delete()
        return True
    
    @staticmethod
    def delete_event_registration(event_id, attendee_id):
        """
        Delete a specific event registration.
        """
        registration = EventRegistration.objects.get(event_id=event_id, attendee_id=attendee_id)
        registration.delete()
        return True
    
    @staticmethod
    def get_event_registration(event_id, attendee_id):
        """
        Get a specific event registration.
        """
        registration = EventRegistration.objects.get(event_id=event_id, attendee_id=attendee_id)
        return registration

