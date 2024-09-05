from django.conf import settings

class ProfilesSettings:
    """
    ProfilesSettings: Manages app-specific settings for profiles.
    """

    @staticmethod
    def get_profiles_settings():
        """
        Get all profiles settings.
        """
        return settings.PROFILES_SETTINGS

    @staticmethod
    def update_profiles_settings(profiles_settings):
        """
        Update profiles settings.
        """
        settings.PROFILES_SETTINGS = profiles_settings
