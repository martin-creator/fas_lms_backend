from django.conf import settings


class JobsSettings:
    """
    JobsSettings: Manages app-specific settings for jobs.
    """

    @staticmethod
    def get_jobs_settings():
        """
        Get all job settings.
        """
        return settings.JOBS_SETTINGS

    @staticmethod
    def update_jobs_settings(jobs_settings):
        """
        Update job settings.
        """
        settings.JOBS_SETTINGS = jobs_settings
