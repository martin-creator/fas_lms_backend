from jobs.models import JobListing, JobApplication, JobNotification
from django.conf import settings


class JobListingsController:
    def __init__(self):
        pass

    def create_job_listing(self, company, title, description, location, closing_date, salary=None, employment_type='', experience_level='', requirements='', responsibilities='', categories=None, skills_required=None, tags=None):
        job_listing = JobListing(
            company=company,
            title=title,
            description=description,
            location=location,
            closing_date=closing_date,
            salary=salary,
            employment_type=employment_type,
            experience_level=experience_level,
            requirements=requirements,
            responsibilities=responsibilities,
        )
        job_listing.save()
        if categories:
            job_listing.categories.set(categories)
        if skills_required:
            job_listing.skills_required.set(skills_required)
        if tags:
            job_listing.tags.set(*tags)
        return job_listing

    def apply_for_job(self, job_listing, applicant, resume, cover_letter='', attachments=None):
        job_application = JobApplication(
            job_listing=job_listing,
            applicant=applicant,
            resume=resume,
            cover_letter=cover_letter,
        )
        job_application.save()
        if attachments:
            for attachment in attachments:
                job_application.attachments.add(attachment)
        return job_application

    def update_job_application_status(self, application_id, status):
        job_application = JobApplication.objects.get(id=application_id)
        job_application.status = status
        job_application.save()
        return job_application

    def notify_user_of_job(self, job_listing, user, message=''):
        job_notification = JobNotification(
            job_listing=job_listing,
            user=user,
            message=message,
        )
        job_notification.save()
        return job_notification
