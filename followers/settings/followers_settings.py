from django.conf import settings


class FollowersSettings:
    """
    FollowersSettings: Manages app-specific settings for followers.
    """

    @staticmethod
    def get_followers_settings():
        """
        Get all followers settings.
        """
        return settings.FOLLOWERS_SETTINGS

    @staticmethod
    def update_followers_settings(followers_settings):
        """
        Update followers settings.
        """
        settings.FOLLOWERS_SETTINGS = followers_settings

    @staticmethod
    def get_followers_settings_value(key):
        """
        Get a specific followers setting.
        """
        return settings.FOLLOWERS_SETTINGS.get(key)

    @staticmethod
    def update_followers_settings_value(key, value):
        """
        Update a specific followers setting.
        """
        settings.FOLLOWERS_SETTINGS[key] = value

    @staticmethod
    def get_followers_settings_value_by_company(company_id, key):
        """
        Get a specific followers setting for a company.
        """
        return settings.FOLLOWERS_SETTINGS.get(company_id, {}).get(key)

    @staticmethod
    def update_followers_settings_value_by_company(company_id, key, value):
        """
        Update a specific followers setting for a company.
        """
        if company_id not in settings.FOLLOWERS_SETTINGS:
            settings.FOLLOWERS_SETTINGS[company_id] = {}
        settings.FOLLOWERS_SETTINGS[company_id][key] = value

    @staticmethod
    def get_followers_settings_value_by_user(user_id, key):
        """
        Get a specific followers setting for a user.
        """
        return settings.FOLLOWERS_SETTINGS.get(user_id, {}).get(key)

    @staticmethod
    def update_followers_settings_value_by_user(user_id, key, value):
        """
        Update a specific followers setting for a user.
        """
        if user_id not in settings.FOLLOWERS_SETTINGS:
            settings.FOLLOWERS_SETTINGS[user_id] = {}
        settings.FOLLOWERS_SETTINGS[user_id][key] = value

    @staticmethod
    def get_followers_settings_value_by_company_user(company_id, user_id, key):
        """
        Get a specific followers setting for a company user.
        """
        return settings.FOLLOWERS_SETTINGS.get(company_id, {}).get(user_id, {}).get(key)

    @staticmethod
    def update_followers_settings_value_by_company_user(company_id, user_id, key, value):
        """
        Update a specific followers setting for a company user.
        """
        if company_id not in settings.FOLLOWERS_SETTINGS:
            settings.FOLLOWERS_SETTINGS[company_id] = {}

        if user_id not in settings.FOLLOWERS_SETTINGS[company_id]:
            settings.FOLLOWERS_SETTINGS[company_id][user_id] = {}

        settings.FOLLOWERS_SETTINGS[company_id][user_id][key] = value

