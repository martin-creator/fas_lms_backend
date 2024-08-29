from django.conf import settings


class MessagingSettings:
    """
    MessagingSettings: Manages app-specific settings for messaging.
    """

    @staticmethod
    def get_messaging_settings():
        """
        Get all messaging settings.
        """
        return settings.MESSAGING_SETTINGS

    @staticmethod
    def update_messaging_settings(messaging_settings):
        """
        Update messaging settings.
        """
        settings.MESSAGING_SETTINGS = messaging_settings
