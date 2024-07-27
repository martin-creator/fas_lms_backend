# profiles/actions/profile_actions.py

from profiles.models import Follower, FollowRequest
from profiles.actions.follower_actions import FollowerActions
from profiles.actions.education_experience_actions import EducationExperienceActions
from profiles.actions.job_actions import JobActions

class ProfileActions:

    @staticmethod
    def follow_profile(request, profile, user_profile):
        if user_profile.is_following(profile):
            return {'status': 'Already following'}, 400
        if profile.is_private:
            return FollowerActions.create_follow_request(user_profile, profile)
        else:
            FollowerActions.create_follower(profile, user_profile)
            return {'status': 'Followed'}, 200

    @staticmethod
    def unfollow_profile(request, profile, user_profile):
        if not user_profile.is_following(profile):
            return {'status': 'Not following'}, 400
        FollowerActions.delete_follower(profile, user_profile)
        return {'status': 'Unfollowed'}, 200

    @staticmethod
    def endorse_skill(request, profile):
        return EducationExperienceActions.endorse_skill(request, profile)

    @staticmethod
    def add_skill(request, profile):
        return EducationExperienceActions.add_skill(request, profile)

    @staticmethod
    def remove_skill(request, profile):
        return EducationExperienceActions.remove_skill(request, profile)

    @staticmethod
    def add_experience(request, profile):
        title = request.data.get('title')
        company = request.data.get('company')
        description = request.data.get('description')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        is_current = request.data.get('is_current', False)
        
        return EducationExperienceActions.add_experience(
            profile, title, company, description, start_date, end_date, is_current
        )

    @staticmethod
    def remove_experience(request, profile):
        experience_id = request.data.get('experience_id')
        if not experience_id:
            return {'error': 'Experience ID not provided'}, 400
        return EducationExperienceActions.remove_experience(profile, experience_id)

    @staticmethod
    def add_education(request, profile):
        institution = request.data.get('institution')
        degree = request.data.get('degree')
        field_of_study = request.data.get('field_of_study')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        is_current = request.data.get('is_current', False)
        
        return EducationExperienceActions.add_education(
            profile, institution, degree, field_of_study, start_date, end_date, is_current
        )

    @staticmethod
    def remove_education(request, profile):
        education_id = request.data.get('education_id')
        if not education_id:
            return {'error': 'Education ID not provided'}, 400
        return EducationExperienceActions.remove_education(profile, education_id)

    @staticmethod
    def add_job_application(request, profile):
        job_id = request.data.get('job_id')
        if not job_id:
            return {'error': 'Job ID not provided'}, 400
        return JobActions.add_job_application(profile, job_id)

    @staticmethod
    def remove_job_application(request, profile):
        job_id = request.data.get('job_id')
        if not job_id:
            return {'error': 'Job ID not provided'}, 400
        return JobActions.remove_job_application(profile, job_id)

    @staticmethod
    def add_job_listing(request, profile):
        job_id = request.data.get('job_id')
        if not job_id:
            return {'error': 'Job ID not provided'}, 400
        return JobActions.add_job_listing(profile, job_id)

    @staticmethod
    def remove_job_listing(request, profile):
        job_id = request.data.get('job_id')
        if not job_id:
            return {'error': 'Job ID not provided'}, 400
        return JobActions.remove_job_listing(profile, job_id)
