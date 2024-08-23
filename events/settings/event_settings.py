from django.conf import settings
# ettings:

# EventSettings: Manages app-specific settings for events.
# Functions:
# get_event_settings, update_event_settings.

class EventSettings:
    """
    EventSettings: Manages app-specific settings for events.
    """

    @staticmethod
    def get_event_settings():
        """
        Get all event settings.
        """
        return settings.EVENT_SETTINGS

    @staticmethod
    def update_event_settings(event_settings):
        """
        Update event settings.
        """
        settings.EVENT_SETTINGS = event_settings