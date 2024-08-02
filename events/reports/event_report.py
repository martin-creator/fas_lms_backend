from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from events.models import Event, EventRegistration, EventFeedback
from events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from events.querying.event_query import EventQuery

class EventReport:
    @staticmethod
    def get_event_report(event):
        """
        Get a report for a specific event.
        """
        event_data = EventSerializer(event).data
        event_registrations = EventRegistration.objects.filter(event=event)
        event_data['registrations'] = EventRegistrationSerializer(event_registrations, many=True).data
        event_feedbacks = EventFeedback.objects.filter(event=event)
        event_data['feedbacks'] = EventFeedbackSerializer(event_feedbacks, many=True).data

        # return json data

        json_data = {
            'event': event_data,
            'registrations': event_data['registrations'],
            'feedbacks': event_data['feedbacks']
        }

        return json_data

    @staticmethod
    def get_attendee_report(attendee):
        """
        Get a report for a specific attendee.
        """
        attendee_data = {}
        attendee_data['events'] = EventQuery.get_events_by_attendee(attendee).count()
        attendee_data['registrations'] = EventQuery.get_event_registrations_by_attendee(attendee).count()
        attendee_data['feedbacks'] = EventQuery.get_event_feedbacks_by_attendee(attendee).count()

        return attendee_data

    @staticmethod
    def get_events_monthly_report():
        """
        Get a monthly report for all events.
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return serializer.data