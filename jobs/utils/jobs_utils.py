# jobs/utils/jobs.py
from jobs.models import JobApplication, JobListing

class JobUtils:
    @staticmethod
    def apply_for_job(profile, job_id):
        job_listing = JobListing.objects.filter(id=job_id).first()
        if job_listing:
            JobApplication.objects.get_or_create(profile=profile, job_listing=job_listing)
            return job_listing
        return None

    @staticmethod
    def save_job_listing(profile, job_id):
        job_listing = JobListing.objects.filter(id=job_id).first()
        if job_listing:
            profile.job_listings.add(job_listing)
            return job_listing
        return None
