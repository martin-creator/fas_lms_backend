from django.conf import settings

class ActivitySettings:
    
    @staticmethod
    def get_activity_settings():
        """
        Retrieve activity settings.
        """
        # Example: Retrieve settings from Django settings or database
        return {
            'max_activities_per_user': getattr(settings, 'MAX_ACTIVITIES_PER_USER', 100),
            'default_activity_type': getattr(settings, 'DEFAULT_ACTIVITY_TYPE', 'general'),
        }

    @staticmethod
    def update_activity_settings(settings_data):
        """
        Update activity settings.
        """
        # Example: Update settings in Django settings or database
        for key, value in settings_data.items():
            setattr(settings, key, value)

        return True  # Return true if settings are updated successfully
