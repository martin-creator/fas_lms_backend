# profiles/actions/profile_actions.py

from profiles.models import Follower, FollowRequest
from profiles.actions.follower_actions import FollowerActions
from profiles.actions.education_experience_actions import EducationExperienceActions
from profiles.actions.job_actions import JobActions
from profiles.utils.profiles_utils import ProfileUtils

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

    @staticmethod
    def add_achievement(request, profile):
        title = request.data.get('title')
        description = request.data.get('description')
        date_achieved = request.data.get('date_achieved')
        
        if not all([title, description, date_achieved]):
            return {'error': 'Missing required fields'}, 400

        try:
            achievement = ProfileUtils.add_achievement(
                profile.user, title, description, date_achieved
            )
            return {'status': 'Achievement added', 'achievement': achievement.id}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @staticmethod
    def remove_achievement(request, profile):
        achievement_id = request.data.get('achievement_id')
        if not achievement_id:
            return {'error': 'Achievement ID not provided'}, 400
        try:
            ProfileUtils.remove_achievement(profile.user, achievement_id)
            return {'status': 'Achievement removed'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @staticmethod
    def add_portfolio(request, profile):
        project_name = request.data.get('project_name')
        description = request.data.get('description')
        project_url = request.data.get('project_url')
        
        if not all([project_name, description, project_url]):
            return {'error': 'Missing required fields'}, 400

        try:
            portfolio = ProfileUtils.add_portfolio(
                profile.user, project_name, description, project_url
            )
            return {'status': 'Portfolio added', 'portfolio': portfolio.id}, 200
        except Exception as e:
            return {'error': str(e)}, 400

    @staticmethod
    def remove_portfolio(request, profile):
        portfolio_id = request.data.get('portfolio_id')
        if not portfolio_id:
            return {'error': 'Portfolio ID not provided'}, 400
        try:
            ProfileUtils.remove_portfolio(profile.user, portfolio_id)
            return {'status': 'Portfolio removed'}, 200
        except Exception as e:
            return {'error': str(e)}, 400