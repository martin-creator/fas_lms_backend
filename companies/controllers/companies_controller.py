from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from events.models import Event, EventRegistration, EventFeedback
from events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from events.settings.event_settings import EventSettings
from events.querying.event_query import EventQuery
from events.utils import DateTimeUtils, UserUtils
from events.reports.event_report import EventReport
from events.services.event_services import EventService



class EventController:
    
    def __init__(self):
        self.event_query = EventQuery()
        self.event_report = EventReport()
        self.event_settings = EventSettings()
        self.user_utils = UserUtils()
        self.date_time_utils = DateTimeUtils()
        self.event_service = EventService()

    
    def get_all_events(self):
        """
        Get all events.
        """
        return self.event_service.get_events
    

    def get_event(self, event_id):
        """
        Get a specific event.
        """
        return self.event_service.get_event(event_id)
    
    def create_event(self, event_data):
        """
        Create a new event.
        """
        return self.event_service.create_event(event_data)
    
    def update_event(self, event_id, event_data):
        """
        Update an event.
        """
        return self.event_service.update_event(event_id, event_data)
    
    def delete_event(self, event_id):
        """
        Delete an event.
        """
        return self.event_service.delete_event(event_id)
    
    def delete_all_events(self):
        """
        Delete all events.
        """
        return self.event_service.delete_all_events()
    
    def register_for_event(self, event_id, user_id):
        """
        Register for an event.
        """
        return self.event_service.register_for_event(event_id, user_id)
    
    def unregister_from_event(self, event_id, user_id):
        """
        Unregister from an event.
        """
        return self.event_service.unregister_from_event(event_id, user_id)
    
    def provide_event_feedback(self, event_id, user_id, feedback_data):
        """
        Provide feedback for an event.
        """
        return self.event_service.provide_event_feedback(event_id, user_id, feedback_data)
    
    def get_event_attendees(self, event_id):
        """
        Get all attendees for an event.
        """
        return self.event_service.get_event_attendees(event_id)
    
    def get_event_registrations(self, event_id):
        """
        Get all registrations for an event.
        """
        return self.event_service.get_event_registrations(event_id)
    
    def get_event_feedbacks(self, event_id):
        """
        Get all feedbacks for an event.
        """
        return self.event_service.get_event_feedbacks(event_id)
    

