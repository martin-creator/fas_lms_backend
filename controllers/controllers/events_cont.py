from events.models import Event
from profiles.models import UserProfile
from activity.models import Attachment, Category


class EventManagementController:
    def __init__(self):
        pass

    def create_event(self, organizer, title, description, location, start_time, end_time, event_date, capacity, attachments=None, categories=None, tags=None):
        event = Event(
            organizer=organizer,
            title=title,
            description=description,
            location=location,
            start_time=start_time,
            end_time=end_time,
            event_date=event_date,
            capacity=capacity,
        )
        if attachments:
            for attachment in attachments:
                event.attachments.add(attachment)
        if categories:
            event.categories.set(categories)
        if tags:
            event.tags.add(*tags)
        event.save()
        return event

    def get_event_attendees(self, event_id):
        event = Event.objects.get(id=event_id)
        return event.attendees.all()

    def register_user_for_event(self, user, event):
        event.attendees.add(user)
        event.save()
        return event

    def unregister_user_from_event(self, user, event):
        event.attendees.remove(user)
        event.save()
        return event
