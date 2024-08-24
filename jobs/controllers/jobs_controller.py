from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from jobs.models import JobListing, JobApplication, JobNotification
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer
from jobs.settings.jobs_settings import JobsSettings
from jobs.querying.jobs_query import JobQuery
from jobs.utils import DateTimeUtils, UserUtils
from jobs.reports.jobs_report import JobReport
from jobs.services.jobs_services import JobService



# class CompanyController:
    
#     def __init__(self):
#         self.company_query = CompanyQuery()
#         self.company_report = CompanyReport()
#         self.company_settings = CompanySettings()
#         self.user_utils = UserUtils()
#         self.date_time_utils = DateTimeUtils()
#         self.company_service = CompanyService()


#     def get_all_companies(self):
#         """
#         Get all companies.
#         """
#         return self.company_service.get_companies()


#     def get_company_by_id(self, company_id):
#         """
#         Get a specific company.
#         """
#         return self.company_service.get_company(company_id)


#     def create_company(self, company_data):
#         """
#         Create a new company.
#         """
#         return self.company_service.create_company(company_data)
    

#     def update_company(self, company_id, company_data):
#         """
#         Update a company.
#         """
#         return self.company_service.update_company(company_id, company_data)
    

#     def delete_company(self, company_id):
#         """
#         Delete a company.
#         """
#         return self.company_service.delete_company(company_id)
    

#     def delete_all_companies(self):
#         """
#         Delete all companies.
#         """
#         return self.company_service.delete_all_companies()
    

#     def get_company_updates(self, company_id):
#         """
#         Get all updates for a company.
#         """
#         return self.company_service.get_company_updates(company_id)
    

#     def get_company_update_by_id(self, update_id):
#         """
#         Get a specific company update.
#         """
#         return self.company_service.get_company_update_by_id(update_id)
    

#     def create_company_update(self, company_id, update_data):
#         """
#         Create an update for a company.
#         """
#         return self.company_service.create_company_update(company_id, update_data)
    

#     def update_company_update(self, company_id, update_id, update_data):
#         """
#         Update an update for a company.
#         """
#         return self.company_service.update_company_update(company_id, update_id, update_data)
    

#     def delete_company_update(self, update_id):
#         """
#         Delete a company update.
#         """
#         return self.company_service.delete_company_update(update_id)

