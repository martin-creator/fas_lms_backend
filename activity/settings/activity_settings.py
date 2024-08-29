from django.conf import settings



class ActivitySettings:
    """
    ActivitySettings: Manages app-specific settings for activity.
    """

    @staticmethod
    def get_activity_settings():
        """
        Get all activity settings.
        """
        return settings.ACTIVITY_SETTINGS

    @staticmethod
    def update_activity_settings(activity_settings):
        """
        Update activity settings.
        """
        settings.ACTIVITY_SETTINGS = activity_settings


