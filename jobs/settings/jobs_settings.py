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

        
# class CompanySettings:
#     """
#     CompanySettings: Manages app-specific settings for companies.
#     """

#     @staticmethod
#     def get_company_settings():
#         """
#         Get all company settings.
#         """
#         return settings.COMPANY_SETTINGS

#     @staticmethod
#     def update_company_settings(company_settings):
#         """
#         Update company settings.
#         """
#         settings.COMPANY_SETTINGS = company_settings