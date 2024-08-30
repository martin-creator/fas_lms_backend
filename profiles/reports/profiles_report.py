from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from profiles.models import User, UserProfile, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from profiles.serializers import UserSerializer, UserProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from profiles.querying.profiles_query import ProfileQuery


class ProfileReport:
    @staticmethod
    def get_profile_report(profile):
        """
        Get a report for a specific profile.
        """
        profile_data = UserProfileSerializer(profile).data
        profile_skills = Skill.objects.filter(user_profile=profile)
        profile_data['skills'] = SkillSerializer(profile_skills, many=True).data

        profile_experiences = Experience.objects.filter(user_profile=profile)
        profile_data['experiences'] = ExperienceSerializer(profile_experiences, many=True).data

        profile_educations = Education.objects.filter(user_profile=profile)
        profile_data['educations'] = EducationSerializer(profile_educations, many=True).data

        profile_endorsements = Endorsement.objects.filter(endorsed_user=profile)
        profile_data['endorsements'] = EndorsementSerializer(profile_endorsements, many=True).data

        profile_achievements = Achievement.objects.filter(user=profile)
        profile_data['achievements'] = AchievementSerializer(profile_achievements, many=True).data

        profile_portfolios = Portfolio.objects.filter(user=profile)
        profile_data['portfolios'] = PortfolioSerializer(profile_portfolios, many=True).data

        return profile_data

    @staticmethod
    def get_user_report(user):
        """
        Get a report for a specific user.
        """
        user_data = UserSerializer(user).data
        user_profile = ProfileQuery.get_profile_by_user(user)
        user_data['profile'] = UserProfileSerializer(user_profile).data

        return user_data

    @staticmethod
    def get_users_report():
        """
        Get a report for all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data
    
    @staticmethod
    def get_users_profile_report():
        """
        Get a profile report for all users.
        """
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    
    @staticmethod
    def get_users_skills_report():
        """
        Get a skills report for all users.
        """
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return serializer.data
    
    @staticmethod
    def get_users_experiences_report():
        """
        Get an experiences report for all users.
        """
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return serializer.data
    

    @staticmethod
    def get_users_educations_report():
        """
        Get an educations report for all users.
        """
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return serializer.data
    

    @staticmethod
    def get_users_endorsements_report():
        """
        Get an endorsements report for all users.
        """
        endorsements = Endorsement.objects.all()
        serializer = EndorsementSerializer(endorsements, many=True)
        return serializer.data
    

    @staticmethod
    def get_users_achievements_report():
        """
        Get an achievements report for all users.
        """
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(achievements, many=True)
        return serializer.data
    

    @staticmethod
    def get_users_portfolios_report():
        """
        Get a portfolios report for all users.
        """
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data

