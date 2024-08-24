from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from jobs.models import JobListing, JobApplication, JobNotification
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer
from jobs.settings.jobs_settings import JobsSettings
from jobs.querying.jobs_query import JobQuery
from jobs.utils import DateTimeUtils, UserUtils
from jobs.reports.jobs_report import JobReport
from jobs.services.jobs_services import JobService



class JobController:
        
        def __init__(self):
            self.job_query = JobQuery()
            self.job_report = JobReport()
            self.job_settings = JobsSettings()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
            self.job_service = JobService()
    
    
        def get_all_jobs(self):
            """
            Get all jobs.
            """
            return self.job_service.get_jobs()
    
    
        def get_job_by_id(self, job_id):
            """
            Get a specific job.
            """
            return self.job_service.get_job(job_id)
    
    
        def create_job(self, job_data):
            """
            Create a new job.
            """
            return self.job_service.create_job(job_data)
        
    
        def update_job(self, job_id, job_data):
            """
            Update a job.
            """
            return self.job_service.update_job(job_id, job_data)
        
    
        def delete_job(self, job_id):
            """
            Delete a job.
            """
            return self.job_service.delete_job(job_id)
        
    
        def delete_all_jobs(self):
            """
            Delete all jobs.
            """
            return self.job_service.delete_all_jobs()
        
    
        def get_job_applications(self, job_id):
            """
            Get all applications for a specific job.
            """
            return self.job_service.get_job_applications(job_id)
        
    
        def get_job_application_by_id(self, application_id):
            """
            Get a specific job application.
            """
            return self.job_service.get_job_application(application_id)
        
    
        def get_job_application_by_applicant(self, applicant_id):
            """
            Get all job applications for a specific applicant.
            """
            return self.job_service.get_job_application_by_applicant(applicant_id)
        
    
        def get_jobs_by_company(self, company_id):
            """
            Get all jobs for a specific company.
            """
            return self.job_service.get_jobs_by_company(company_id)
        

        def create_job_application(self, application_data):
            """
            Create a new job application.
            """
            return self.job_service.create_job_application(application_data)
        

        def update_job_application(self, application_id, application_data):
            """
            Update a job application.
            """
            return self.job_service.update_job_application(application_id, application_data)
        

        def delete_job_application(self, application_id):
            """
            Delete a job application.
            """
            return self.job_service.delete_job_application(application_id)
        

        def get_job_notifications(self, job_id):
            """
            Get all notifications for a specific job.
            """
            return self.job_service.get_job_notifications(job_id)
        

        def get_job_notification_by_id(self, notification_id):
            """
            Get a specific job notification.
            """
            return self.job_service.get_job_notification(notification_id)
        

        def get_job_notification_by_user(self, user_id):
            """
            Get all notifications for a specific user.
            """
            return self.job_service.get_job_notification_by_user(user_id)
        

        def create_job_notification(self, notification_data):
            """
            Create a new job notification.
            """
            return self.job_service.create_job_notification(notification_data)
        

        def update_job_notification(self, notification_id, notification_data):
            """
            Update a job notification.
            """
            return self.job_service.update_job_notification(notification_id, notification_data)
        

        def delete_job_notification(self, notification_id):
            """
            Delete a job notification.
            """
            return self.job_service.delete_job_notification(notification_id)
        

        def delete_all_job_notifications(self):
            """
            Delete all job notifications.
            """
            return self.job_service.delete_all_job_notifications()
        

        def get_interviews(self):
            """
            Get all interviews.
            """
            return self.job_service.get_interviews()
        

        def get_interview_by_id(self, interview_id):
            """
            Get a specific interview.
            """
            return self.job_service.get_interview(interview_id)
        

        def get_interviews_by_job(self, job_id):
            """
            Get all interviews for a specific job.
            """
            return self.job_service.get_interviews_by_job(job_id)
        

        def get_interviews_by_job_application(self, application_id):
            """
            Get all interviews for a specific job application.
            """
            return self.job_service.get_interviews_by_job_application(application_id)
        

        def create_interview(self, interview_data):
            """
            Create a new interview.
            """
            return self.job_service.create_interview(interview_data)
        

        def update_interview(self, interview_id, interview_data):
            """
            Update an interview.
            """
            return self.job_service.update_interview(interview_id, interview_data)
        

        def delete_interview(self, interview_id):
            """
            Delete an interview.
            """
            return self.job_service.delete_interview(interview_id)
        

        def delete_all_interviews(self):
            """
            Delete all interviews.
            """
            return self.job_service.delete_all_interviews()
        

        def generate_job_application_report(self, job_id):
            """
            Generate a report for a specific job application.
            """
            return self.job_service.generate_job_application_report(job_id)
        

        def generate_job_summary(self):
            """
            Generate a summary report for all jobs.
            """
            return self.job_service.generate_job_summary()
        

        def get_interviews_by_job(self, job_id):
            """
            Get all interviews for a specific job.
            """
            return self.job_service.get_interviews_by_job(job_id)
        

        def get_interviews_by_job_application(self, application_id):
            """
            Get all interviews for a specific job application.
            """
            return self.job_service.get_interviews_by_job_application(application_id)
        


        



