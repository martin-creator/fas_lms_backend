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
