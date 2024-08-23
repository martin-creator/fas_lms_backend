from django.conf import settings


class CertificationsSettings:
    """
    CertificationsSettings: Manages app-specific settings for certifications.
    """

    @staticmethod
    def get_certifications_settings():
        """
        Get all certifications settings.
        """
        return settings.CERTIFICATIONS_SETTINGS

    @staticmethod
    def update_certifications_settings(certifications_settings):
        """
        Update certifications settings.
        """
        settings.CERTIFICATIONS_SETTINGS = certifications_settings
