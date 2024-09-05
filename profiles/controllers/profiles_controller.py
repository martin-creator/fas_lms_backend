from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from profiles.models import UserProfile, Follower, FollowRequest, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from profiles.serializers import UserProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from profiles.settings.profiles_settings import ProfilesSettings
from profiles.querying.profiles_query import ProfileQuery
from profiles.helpers.profiles_helpers import ProfileHelpers
from profiles.reports.profiles_report import ProfilesReport
from profiles.utils import UserUtils, DateTimeUtils
from profiles.services.profiles_services import ProfileService


class ProfileController:
    
        def __init__(self):
            self.profile_query = ProfileQuery()
            self.profile_report = ProfilesReport()
            self.profile_settings = ProfilesSettings()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
            self.profile_service = ProfileService()


        def update_user_cover_and_profile_picture(self, user_id, data):
            """
            Update a user's cover and profile picture.
            """
            return self.profile_service.update_user_cover_and_profile_picture(user_id, data)
        
    
        def get_all_profiles(self):
            """
            Get all profiles.
            """
            return self.profile_service.get_profiles()
        
        def get_profile(self, profile_id):
            """
            Get a specific profile.
            """
            return self.profile_service.get_profile(profile_id)
        
        def create_profile(self, profile_data):
            """
            Create a new profile.
            """
            return self.profile_service.create_profile(profile_data)
        
        def update_profile(self, profile_id, profile_data):
            """
            Update a profile.
            """
            return self.profile_service.update_profile(profile_id, profile_data)
        
        def delete_profile(self, profile_id):
            """
            Delete a profile.
            """
            return self.profile_service.delete_profile(profile_id)
        
        def delete_all_profiles(self):
            """
            Delete all profiles.
            """
            return self.profile_service.delete_all_profiles()
        
        def follow_profile(self, profile_id):
            """
            Follow a profile.
            """
            return self.profile_service.follow_profile(profile_id)
        
        def unfollow_profile(self, profile_id):
            """
            Unfollow a profile.
            """
            return self.profile_service.unfollow_profile(profile_id)
        
        def accept_follow_request(self, profile_id):
            """
            Accept a follow request.
            """
            return self.profile_service.accept_follow_request(profile_id)
        
        def reject_follow_request(self, profile_id):
            """
            Reject a follow request.
            """
            return self.profile_service.reject_follow_request(profile_id)
        
        def endorse_skill(self, profile_id, skill_id):
            """
            Endorse a skill.
            """
            return self.profile_service.endorse_skill(profile_id, skill_id)
        
        def add_experience(self, profile_id, experience_data):
            """
            Add an experience.
            """
            return self.profile_service.add_experience(profile_id, experience_data)
        
        def add_education(self, profile_id, education_data):
            """
            Add an education.
            """
            return self.profile_service.add_education(profile_id, education_data)
        
        def add_skill(self, profile_id, skill_data):
            """
            Add a skill.
            """
            return self.profile_service.add_skill(profile_id, skill_data)

        def add_achievement(self, profile_id, achievement_data):
            """
            Add an achievement.
            """
            return self.profile_service.add_achievement(profile_id, achievement_data)


        def add_portfolio(self, profile_id, portfolio_data):
            """
            Add a portfolio.
            """
            return self.profile_service.add_portfolio(profile_id, portfolio_data)


        def get_followers(self, profile_id):
            """
            Get all followers for a profile.
            """
            return self.profile_service.get_followers(profile_id)


        def get_experiences(self, profile_id):
            """
            Get all experiences for a profile.
            """
            return self.profile_service.get_experiences(profile_id)


        def get_experience(self, profile_id, experience_id):
            """
            Get a specific experience for a profile.
            """
            return self.profile_service.get_experience(profile_id, experience_id)


        def update_experience(self, profile_id, experience_id, experience_data):
            """
            Update an experience for a profile.
            """
            return self.profile_service.update_experience(profile_id, experience_id, experience_data)


        def delete_experience(self, profile_id, experience_id):
            """
            Delete an experience for a profile.
            """
            return self.profile_service.delete_experience(profile_id, experience_id)


        def delete_all_experiences(self, profile_id):
            """
            Delete all experiences for a profile.
            """
            return self.profile_service.delete_all_experiences(profile_id)


        def get_educations(self, profile_id):
            """
            Get all educations for a profile.
            """
            return self.profile_service.get_educations(profile_id)


        def get_education(self, profile_id, education_id):
            """
            Get a specific education for a profile.
            """
            return self.profile_service.get_education(profile_id, education_id)


        def update_education(self, profile_id, education_id, education_data):
            """
            Update an education for a profile.
            """
            return self.profile_service.update_education(profile_id, education_id, education_data)


        def delete_education(self, profile_id, education_id):
            """
            Delete an education for a profile.
            """
            return self.profile_service.delete_education(profile_id, education_id)


        def delete_all_educations(self, profile_id):
            """
            Delete all educations for a profile.
            """
            return self.profile_service.delete_all_educations(profile_id)


        def get_skills(self, profile_id):
            """
            Get all skills for a profile.
            """
            return self.profile_service.get_skills(profile_id)


        def get_skill(self, profile_id, skill_id):
            """
            Get a specific skill for a profile.
            """
            return self.profile_service.get_skill(profile_id, skill_id)


        def update_skill(self, profile_id, skill_id, skill_data):
            """
            Update a skill for a profile.
            """
            return self.profile_service.update_skill(profile_id, skill_id, skill_data)


        def delete_skill(self, profile_id, skill_id):
            """
            Delete a skill for a profile.
            """
            return self.profile_service.delete_skill(profile_id, skill_id)


        def delete_all_skills(self, profile_id):
            """
            Delete all skills for a profile.
            """
            return self.profile_service.delete_all_skills(profile_id)


        def get_achievements(self, profile_id):
            """
            Get all achievements for a profile.
            """
            return self.profile_service.get_achievements(profile_id)


        def get_achievement(self, profile_id, achievement_id):
            """
            Get a specific achievement for a profile.
            """
            return self.profile_service.get_achievement(profile_id, achievement_id)


        def update_achievement(self, profile_id, achievement_id, achievement_data):
            """
            Update an achievement for a profile.
            """
            return self.profile_service.update_achievement(profile_id, achievement_id, achievement_data)


        def delete_achievement(self, profile_id, achievement_id):
            """
            Delete an achievement for a profile.
            """
            return self.profile_service.delete_achievement(profile_id, achievement_id)


        def delete_all_achievements(self, profile_id):
            """
            Delete all achievements for a profile.
            """
            return self.profile_service.delete_all_achievements(profile_id)


        def get_portfolios(self, profile_id):
            """
            Get all portfolios for a profile.
            """
            return self.profile_service.get_portfolios(profile_id)


        def get_portfolio(self, profile_id, portfolio_id):
            """
            Get a specific portfolio for a profile.
            """
            return self.profile_service.get_portfolio(profile_id, portfolio_id)


        def update_portfolio(self, profile_id, portfolio_id, portfolio_data):
            """
            Update a portfolio for a profile.
            """
            return self.profile_service.update_portfolio(profile_id, portfolio_id, portfolio_data)


        def delete_portfolio(self, profile_id, portfolio_id):
            """
            Delete a portfolio for a profile.
            """
            return self.profile_service.delete_portfolio(profile_id, portfolio_id)


        def delete_all_portfolios(self, profile_id):
            """
            Delete all portfolios for a profile.
            """
            return self.profile_service.delete_all_portfolios(profile_id)


        def get_profile_report(self, profile_id):
            """
            Get a report for a specific profile.
            """
            return self.profile_service.get_profile_report(profile_id)
