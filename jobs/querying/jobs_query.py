from django.db.models import Count, Q
from jobs.models import JobApplication, JobNotification, JobListing, Interview
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer, InterviewSerializer
from django.utils import timezone


class JobQuery:
    @staticmethod
    def get_jobs():
        """
        Get all jobs.
        """
        jobs = JobListing.objects.all()
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_job(job_id):
        """
        Get a specific job.
        """
        job = JobListing.objects.get(id=job_id)
        serializer = JobListingSerializer(job)
        return serializer.data

    @staticmethod
    def get_job_applications(job_id):
        """
        Get all applications for a specific job.
        """
        applications = JobApplication.objects.filter(job_id=job_id)
        serializer = JobApplicationSerializer(applications, many=True)
        return serializer.data

    @staticmethod
    def get_job_notifications(job_id):
        """
        Get all notifications for a specific job.
        """
        notifications = JobNotification.objects.filter(job_id=job_id)
        serializer = JobNotificationSerializer(notifications, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_company(company_id):
        """
        Get all jobs for a specific company.
        """
        jobs = JobListing.objects.filter(company_id=company_id)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_location(location):
        """
        Get all jobs in a specific location.
        """
        jobs = JobListing.objects.filter(location=location)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_employment_type(employment_type):
        """
        Get all jobs with a specific employment type.
        """
        jobs = JobListing.objects.filter(employment_type=employment_type)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_experience_level(experience_level):
        """
        Get all jobs with a specific experience level.
        """
        jobs = JobListing.objects.filter(experience_level=experience_level)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_program_type(program_type):
        """
        Get all jobs with a specific program type.
        """
        jobs = JobListing.objects.filter(program_type=program_type)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data

    @staticmethod
    def get_jobs_by_program_duration(program_duration):
        """
        Get all jobs with a specific program duration.
        """
        jobs = JobListing.objects.filter(program_duration=program_duration)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data
    
    @staticmethod
    def get_jobs_by_skills_required(skill_id):
        """
        Get all jobs that require a specific skill.
        """
        jobs = JobListing.objects.filter(skills_required=skill_id)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data
    

    @staticmethod
    def get_jobs_by_tags(tag):
        """
        Get all jobs with a specific tag.
        """
        jobs = JobListing.objects.filter(tags__name=tag)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data
    
    @staticmethod
    def get_jobs_by_status(status):
        """
        Get all jobs with a specific status.
        """
        jobs = JobListing.objects.filter(status=status)
        serializer = JobListingSerializer(jobs, many=True)
        return serializer.data
    

    @staticmethod
    def get_job_application(application_id):
        """
        Get a specific job application.
        """
        application = JobApplication.objects.get(id=application_id)
        serializer = JobApplicationSerializer(application)
        return serializer.data
    
    @staticmethod
    def get_job_notification(notification_id):
        """
        Get a specific job notification.
        """
        notification = JobNotification.objects.get(id=notification_id)
        serializer = JobNotificationSerializer(notification)
        return serializer.data
    
    @staticmethod
    def get_job_application_by_applicant(applicant_id):
        """
        Get all job applications for a specific applicant.
        """
        applications = JobApplication.objects.filter(applicant_id=applicant_id)
        serializer = JobApplicationSerializer(applications, many=True)
        return serializer.data
    

    @staticmethod
    def get_job_notification_by_user(user_id):
        """
        Get all job notifications for a specific user.
        """
        notifications = JobNotification.objects.filter(user_id=user_id)
        serializer = JobNotificationSerializer(notifications, many=True)
        return serializer.data
    

    @staticmethod
    def delete_job(job_id):
        """
        Delete a job.
        """
        job = JobListing.objects.get(id=job_id)
        job.delete()

        return True
    
    @staticmethod
    def delete_job_application(application_id):
        """
        Delete a job application.
        """
        application = JobApplication.objects.get(id=application_id)
        application.delete()

        return True
    
    @staticmethod
    def delete_job_notification(notification_id):
        """
        Delete a job notification.
        """
        notification = JobNotification.objects.get(id=notification_id)
        notification.delete()

        return True
    
    @staticmethod
    def delete_all_jobs():
        """
        Delete all jobs.
        """
        jobs = JobListing.objects.all()
        jobs.delete()

        return True
    
    @staticmethod
    def delete_all_job_applications():
        """
        Delete all job applications.
        """
        applications = JobApplication.objects.all()
        applications.delete()

        return True
    

    @staticmethod
    def delete_all_job_notifications():
        """
        Delete all job notifications.
        """
        notifications = JobNotification.objects.all()
        notifications.delete()

        return True
    

    # interview queries
    @staticmethod
    def get_interviews_by_job_application(application_id):
        """
        Get all interviews for a specific job application.
        """
        interviews = Interview.objects.filter(job_application_id=application_id)
        serializer = InterviewSerializer(interviews, many=True)
        return serializer.data
    

    @staticmethod
    def get_interview(interview_id):
        """
        Get a specific interview.
        """
        interview = Interview.objects.get(id=interview_id)
        serializer = InterviewSerializer(interview)
        return serializer.data
    

    @staticmethod
    def delete_interview(interview_id):
        """
        Delete an interview.
        """
        interview = Interview.objects.get(id=interview_id)
        interview.delete()

        return True
    

    @staticmethod
    def delete_all_interviews():
        """
        Delete all interviews.
        """
        interviews = Interview.objects.all()
        interviews.delete()

        return True
    

    @staticmethod
    def get_interviews_by_interviewer(interviewer_id):
        """
        Get all interviews conducted by a specific interviewer.
        """
        interviews = Interview.objects.filter(interviewer_id=interviewer_id)
        serializer = InterviewSerializer(interviews, many=True)
        return serializer.data
    

    @staticmethod
    def get_interviews_by_location(location):
        """
        Get all interviews at a specific location.
        """
        interviews = Interview.objects.filter(location=location)
        serializer = InterviewSerializer(interviews, many=True)
        return serializer.data
    
