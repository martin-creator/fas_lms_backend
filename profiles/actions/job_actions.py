# profiles/actions/job_actions.py

from jobs.models import JobApplication, JobListing

class JobActions:

    @staticmethod
    def add_job_application(profile, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
            JobApplication.objects.create(profile=profile, job=job)
            return {'status': 'Job application added'}, 200
        except JobListing.DoesNotExist:
            return {'error': 'Job listing not found'}, 404

    @staticmethod
    def remove_job_application(profile, job_id):
        try:
            job_application = JobApplication.objects.get(profile=profile, job_id=job_id)
            job_application.delete()
            return {'status': 'Job application removed'}, 200
        except JobApplication.DoesNotExist:
            return {'error': 'Job application not found'}, 404

    @staticmethod
    def add_job_listing(profile, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
            profile.job_listings.add(job)
            return {'status': 'Job listing added'}, 200
        except JobListing.DoesNotExist:
            return {'error': 'Job listing not found'}, 404

    @staticmethod
    def remove_job_listing(profile, job_id):
        try:
            job = JobListing.objects.get(id=job_id)
            profile.job_listings.remove(job)
            return {'status': 'Job listing removed'}, 200
        except JobListing.DoesNotExist:
            return {'error': 'Job listing not found'}, 404
