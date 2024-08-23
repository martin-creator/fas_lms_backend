from django.conf import settings


class CompanySettings:
    """
    CompanySettings: Manages app-specific settings for companies.
    """

    @staticmethod
    def get_company_settings():
        """
        Get all company settings.
        """
        return settings.COMPANY_SETTINGS

    @staticmethod
    def update_company_settings(company_settings):
        """
        Update company settings.
        """
        settings.COMPANY_SETTINGS = company_settings