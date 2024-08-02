from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from events.models import Event, EventRegistration, EventFeedback
from events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from events.settings.event_settings import EventSettings
from events.querying.event_query import EventQuery
from events.utils import DateTimeUtils, UserUtils
from events.reports.event_report import EventReport


class EventService:

    @staticmethod
    def get_events():
        """
        Get all events.
        """
        events = EventQuery.get_events()
        return events
    

    @staticmethod
    def get_event(event_id):
        """
        Get a specific event.
        """
        event = EventQuery.get_event(event_id)
        return event

    @staticmethod
    def create_event(event_data):
        """
        Create a new event.
        """

        event, event_tags = EventQuery.process_event_data(event_data)
        event.save()

        if event_tags:
            event.tags.set(event_tags)

        serializer = EventSerializer(event)

        return serializer.data
    

    @staticmethod
    def update_event(event_id, event_data):
        """
        Update an event.
        """

        # event = EventQuery.get_event(event_id)
        event, event_tags = EventQuery.process_event_update_data(event_id, event_data)
        event.save()

        if event_tags:
            event.tags.set(event_tags)

        serializer = EventSerializer(event)

        return serializer.data
    

    @staticmethod
    def delete_event(event_id):
        """
        Delete an event.
        """
        event = EventQuery.get_event(event_id)
        event.delete()

        return True
    

    @staticmethod
    def get_event_report(event_id):
        """
        Get a report for a specific event.
        """
        event = EventQuery.get_event(event_id)
        report = EventReport.get_event_report(event)

        return report
    

    @staticmethod
    def get_attendee_report(attendee_id):
        """
        Get a report for a specific attendee.
        """
        attendee = UserUtils.get_current_user(attendee_id)
        report = EventReport.get_attendee_report(attendee)

        return report
    
    @staticmethod
    def register_for_event(event_id, attendee_id):
        """
        Register for an event.
        """
        event = EventQuery.get_event(event_id)
        attendee = UserUtils.get_current_user(attendee_id)

        registration = EventRegistration(event=event, attendee=attendee)
        registration.save()

        return True


    @staticmethod
    def unregister_from_event(event_id, attendee_id):
        """
        Unregister from an event.
        """
        registration = EventQuery.get_event_registration(event_id, attendee_id)
        registration.delete()

        return True
    

    @staticmethod
    def provide_event_feedback(event_id, attendee_id, feedback_data):
        """
        Provide feedback for an event.
        """
        event = EventQuery.get_event(event_id)
        attendee = UserUtils.get_current_user(attendee_id)

        feedback = EventFeedback(event=event, attendee=attendee, **feedback_data)
        feedback.save()

        return True

    
    @staticmethod
    def get_events_by_organizer(organizer_id):
        """
        Get all events organized by a specific organizer.
        """
        events = EventQuery.get_events_by_organizer(organizer_id)
        return events
    

    @staticmethod
    def get_events_by_attendee(attendee_id):
        """
        Get all events attended by a specific attendee.
        """
        events = EventQuery.get_events_by_attendee(attendee_id)
        return events


    @staticmethod
    def get_event_registrations(event_id):
        """
        Get all registrations for a specific event.
        """
        registrations = EventQuery.get_event_registrations(event_id)
        return registrations
    

    @staticmethod
    def get_event_feedbacks(event_id):
        """
        Get all feedbacks for a specific event.
        """
        feedbacks = EventQuery.get_event_feedbacks(event_id)
        return feedbacks
    

    @staticmethod
    def get_events_monthly_report():
        """
        Get a monthly report for all events.
        """
        report = EventReport.get_events_monthly_report()
        return report
    
    

    

    


        