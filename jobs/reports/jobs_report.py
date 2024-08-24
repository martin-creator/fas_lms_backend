from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from jobs.models import JobApplication, JobNotification, JobListing
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer
from jobs.utils import DateTimeUtils, UserUtils
from jobs.querying.jobs_query import JobQuery


class JobReport:
    @staticmethod
    def generate_job_application_report(job_id):
        """
        Generate a report for a specific job application.
        """
        job = JobQuery.get_job(job_id)
        applications = JobQuery.get_job_applications(job_id)
        notifications = JobQuery.get_job_notifications(job_id)

        job_report = {
            'job': job,
            'applications': applications,
            'notifications': notifications
        }

        return job_report

    @staticmethod
    def generate_job_summary():
        """
        Generate a summary report for all jobs.
        """
        jobs = JobQuery.get_jobs()

        job_summary = {
            'total_jobs': len(jobs),
            'total_applications': JobApplication.objects.count(),
            'total_notifications': JobNotification.objects.count()
        }

        return job_summary
    
    