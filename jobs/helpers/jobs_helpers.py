from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from jobs.models import JobListing, JobApplication, JobNotification
# from profiles.models import UserProfile
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class JobHelpers:
    
        @staticmethod
        def process_job_data(data):
            """
            Process job data before saving it to the database.
            """
            title = data.get('title')
            description = data.get('description')
            company_id = data.get('company_id')
            location = data.get('location')
            closing_date = data.get('closing_date')
            is_active = data.get('is_active')
            salary = data.get('salary')
            requirements = data.get('requirements')
            responsibilities = data.get('responsibilities')
            employment_type = data.get('employment_type')
            experience_level = data.get('experience_level')
            program_type = data.get('program_type')
            program_duration = data.get('program_duration')
            skills_required = data.get('skills_required')
            applications = data.get('applications')
            notifications = data.get('notifications')
            tags = data.get('tags')


            job = JobListing(
                title=title,
                description=description,
                company_id=company_id,
                location=location,
                closing_date=closing_date,
                is_active=is_active,
                salary=salary,
                requirements=requirements,
                responsibilities=responsibilities,
                employment_type=employment_type,
                experience_level=experience_level,
                program_type=program_type,
                program_duration=program_duration,
                skills_required=skills_required,
                applications=applications,
                notifications=notifications,
                tags=tags
            )

            return job, skills_required, applications, notifications, tags
        

        @staticmethod
        def process_job_data_update(job_id, data):
            """
            Process job data before updating it in the database.
            """
            
            job = JobListing.objects.get(id=job_id)
            
            title = data.get('title')
            description = data.get('description')
            company_id = data.get('company_id')
            location = data.get('location')
            closing_date = data.get('closing_date')
            is_active = data.get('is_active')
            salary = data.get('salary')
            requirements = data.get('requirements')
            responsibilities = data.get('responsibilities')
            employment_type = data.get('employment_type')
            experience_level = data.get('experience_level')
            program_type = data.get('program_type')
            program_duration = data.get('program_duration')
            skills_required = data.get('skills_required')
            applications = data.get('applications')
            notifications = data.get('notifications')
            tags = data.get('tags')

            if title is not None:
                job.title = title

            if description is not None:
                job.description = description

            if company_id is not None:
                job.company_id = company_id

            if location is not None:
                job.location = location

            if closing_date is not None:
                job.closing_date = closing_date

            if is_active is not None:
                job.is_active = is_active

            if salary is not None:
                job.salary = salary

            if requirements is not None:
                job.requirements = requirements

            if responsibilities is not None:
                job.responsibilities = responsibilities

            if employment_type is not None:
                job.employment_type = employment_type

            if experience_level is not None:
                job.experience_level = experience_level

            if program_type is not None:
                job.program_type = program_type

            if program_duration is not None:
                job.program_duration = program_duration

            if skills_required is not None:
                job.skills_required.set(skills_required)

            if applications is not None:
                job.applications.set(applications)

            if notifications is not None:
                job.notifications.set(notifications)

            if tags is not None:
                job.tags.set(tags)

            return job, skills_required, applications, notifications, tags
        


        @staticmethod
        def process_job_application_data(data):
            """
            Process job application data before saving it to the database.
            """
            job_listing_id = data.get('job_listing_id')
            applicant_id = data.get('applicant_id')
            resume = data.get('resume')
            cover_letter = data.get('cover_letter')
            status = data.get('status')

            if not job_listing_id:
                raise ValidationError('Job Listing ID is required.')
            
            if not applicant_id:
                raise ValidationError('Applicant ID is required.')
            
            job_listing = JobListing.objects.filter(id=job_listing_id)
            applicant = User.objects.filter(id=applicant_id)

            job_application = JobApplication(
                job_listing=job_listing,
                applicant=applicant,
                resume=resume,
                cover_letter=cover_letter,
                status=status
            )

            return job_application
        

        @staticmethod
        def process_job_application_data_update(application_id, data):
            """
            Process job application data before updating it in the database.
            """
            job_listing_id = data.get('job_listing_id')
            applicant_id = data.get('applicant_id')
            resume = data.get('resume')
            cover_letter = data.get('cover_letter')
            status = data.get('status')

            if not application_id:
                raise ValidationError('Application ID is required.')
            
            job_application = JobApplication.objects.filter(id=application_id)

            if job_listing_id is not None:
                job_application.job_listing = job_listing_id

            if applicant_id is not None:
                job_application.applicant = applicant_id

            if resume is not None:
                job_application.resume = resume

            if cover_letter is not None:
                job_application.cover_letter = cover_letter

            if status is not None:
                job_application.status = status

            return job_application
        

        @staticmethod
        def process_job_notification_data(data):
            """
            Process job notification data before saving it to the database.
            """
            job_listing_id = data.get('job_listing_id')
            user_id = data.get('user_id')

            if not job_listing_id:
                raise ValidationError('Job Listing ID is required.')
            
            if not user_id:
                raise ValidationError('User ID is required.')
            
            job_listing = JobListing.objects.filter(id=job_listing_id)
            user = User.objects.filter(id=user_id)

            job_notification = JobNotification(
                job_listing=job_listing,
                user=user
            )

            return job_notification
        

        @staticmethod
        def process_job_notification_data_update(notification_id, data):
            """
            Process job notification data before updating it in the database.
            """
            job_listing_id = data.get('job_listing_id')
            user_id = data.get('user_id')

            if not notification_id:
                raise ValidationError('Notification ID is required.')
            
            job_notification = JobNotification.objects.filter(id=notification_id)

            if job_listing_id is not None:
                job_notification.job_listing = job_listing_id

            if user_id is not None:
                job_notification.user = user_id

            return job_notification
        