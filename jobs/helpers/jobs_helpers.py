from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from jobs.models import JobListing, JobApplication, JobNotification, Interview
# from profiles.models import UserProfile
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer, InterviewSerializer
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
        

        @staticmethod
        def process_interview_data(data):
            """
            Process interview data before saving it to the database.
            """
            job_application_id = data.get('job_application_id')
            job_listing_id = data.get('job_listing_id')
            interview_date = data.get('interview_date')
            interview_type = data.get('interview_type')
            interviewer_id = data.get('interviewer_id')
            interview_notes = data.get('interview_notes')
            meeting_link = data.get('meeting_link')
            location = data.get('location')

            if not job_application_id:
                raise ValidationError('Job Application ID is required.')
            
            if not job_listing_id:
                raise ValidationError('Job Listing ID is required.')
            
            if not interview_date:
                raise ValidationError('Interview Date is required.')
            
            if not interview_type:
                raise ValidationError('Interview Type is required.')
            
            if not interviewer_id:
                raise ValidationError('Interviewer ID is required.')
            
            job_application = JobApplication.objects.filter(id=job_application_id)
            job_listing = JobListing.objects.filter(id=job_listing_id)
            interviewer = User.objects.filter(id=interviewer_id)

            interview = Interview(
                job_application=job_application,
                job_listing=job_listing,
                interview_date=interview_date,
                interview_type=interview_type,
                interviewer=interviewer,
                interview_notes=interview_notes,
                meeting_link=meeting_link,
                location=location
            )

            return interview
        

        @staticmethod
        def process_interview_data_update(interview_id, data):
            """
            Process interview data before updating it in the database.
            """
            job_application_id = data.get('job_application_id')
            job_listing_id = data.get('job_listing_id')
            interview_date = data.get('interview_date')
            interview_type = data.get('interview_type')
            interviewer_id = data.get('interviewer_id')
            interview_notes = data.get('interview_notes')
            meeting_link = data.get('meeting_link')
            location = data.get('location')

            if not interview_id:
                raise ValidationError('Interview ID is required.')
            
            interview = Interview.objects.filter(id=interview_id)

            if job_application_id is not None:
                interview.job_application = job_application_id

            if job_listing_id is not None:
                interview.job_listing = job_listing_id

            if interview_date is not None:
                interview.interview_date = interview_date

            if interview_type is not None:
                interview.interview_type = interview_type

            if interviewer_id is not None:
                interview.interviewer = interviewer_id

            if interview_notes is not None:
                interview.interview_notes = interview_notes

            if meeting_link is not None:
                interview.meeting_link = meeting_link

            if location is not None:
                interview.location = location

            return interview
        