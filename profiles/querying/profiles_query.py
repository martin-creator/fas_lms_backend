from django.db.models import Count, Q
from profiles.models import User, UserProfile, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from profiles.serializers import UserSerializer, UserProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer 
from django.utils import timezone


class ProfileQuery:
    @staticmethod
    def get_users():
        """
        Get all users.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    @staticmethod
    def get_user(user_id):
        """
        Get a specific user.
        """
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return serializer.data
    
    @staticmethod
    def get_profiles():
        """
        Get all user profiles.
        """
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data

    @staticmethod
    def get_user_profile(profile_id):
        """
        Get a specific user profile.
        """
        profile = UserProfile.objects.get(id=profile_id)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    @staticmethod
    def get_user_profile_by_user(user_id):
        """
        Get a specific user profile by user.
        """
        profile = UserProfile.objects.get(user_id=user_id)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    @staticmethod
    def get_user_profile_by_username(username):
        """
        Get a specific user profile by username.
        """
        profile = UserProfile.objects.get(user__username=username)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    @staticmethod
    def get_user_profile_by_email(email):
        """
        Get a specific user profile by email.
        """
        profile = UserProfile.objects.get(user__email=email)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    @staticmethod
    def get_user_profile_by_phone(phone):
        """
        Get a specific user profile by phone.
        """
        profile = UserProfile.objects.get(phone=phone)
        serializer = UserProfileSerializer(profile)
        return serializer.data

    @staticmethod
    def get_user_profile_by_location(location):
        """
        Get all user profiles in a specific location.
        """
        profiles = UserProfile.objects.filter(location=location)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data

    @staticmethod
    def get_user_profile_by_industry(industry):
        """
        Get all user profiles in a specific industry.
        """
        profiles = UserProfile.objects.filter(industry=industry)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data

    @staticmethod
    def get_user_profile_by_skill(skill):
        """
        Get all user profiles with a specific skill.
        """
        profiles = UserProfile.objects.filter(skills__name=skill)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data

    @staticmethod
    def get_user_profile_by_experience(experience):
        """
        Get all user profiles with a specific experience.
        """
        profiles = UserProfile.objects.filter(experiences__title=experience)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    

    @staticmethod
    def get_user_profile_by_education(education):
        """
        Get all user profiles with a specific education.
        """
        profiles = UserProfile.objects.filter(educations__institution=education)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    
    @staticmethod
    def get_user_profile_by_achievement(achievement):
        """
        Get all user profiles with a specific achievement.
        """
        profiles = UserProfile.objects.filter(achievements__title=achievement)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    

    @staticmethod
    def get_user_profile_by_portfolio(portfolio):
        """
        Get all user profiles with a specific portfolio.
        """
        profiles = UserProfile.objects.filter(portfolios__project_name=portfolio)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    

    @staticmethod
    def get_user_profile_by_endorsement(endorsement):
        """
        Get all user profiles with a specific endorsement.
        """
        profiles = UserProfile.objects.filter(endorsements__skill=endorsement)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    

    @staticmethod
    def get_user_profile_by_endorser(endorser):
        """
        Get all user profiles with a specific endorser.
        """
        profiles = UserProfile.objects.filter(endorsements__endorser=endorser)
        serializer = UserProfileSerializer(profiles, many=True)
        return serializer.data
    

    # Skill methods
    @staticmethod
    def get_skills():
        """
        Get all skills.
        """
        skills = Skill.objects.all()
        serializer = SkillSerializer(skills, many=True)
        return serializer.data
    

    @staticmethod
    def get_skill(skill_id):
        """
        Get a specific skill.
        """
        skill = Skill.objects.get(id=skill_id)
        serializer = SkillSerializer(skill)
        return serializer.data
    

    @staticmethod
    def get_skill_by_name(name):
        """
        Get a specific skill by name.
        """
        skill = Skill.objects.get(name=name)
        serializer = SkillSerializer(skill)
        return serializer.data
    

    @staticmethod
    def get_by_user (user_id):
        """
        Get all skills by user.
        """
        skills = Skill.objects.filter(user_id=user_id)
        serializer = SkillSerializer(skills, many=True)
        return serializer.data
    

    # Experience methods
    @staticmethod
    def get_experiences():
        """
        Get all experiences.
        """
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return serializer.data
    

    @staticmethod
    def get_experience(experience_id):
        """
        Get a specific experience.
        """
        experience = Experience.objects.get(id=experience_id)
        serializer = ExperienceSerializer(experience)
        return serializer.data
    

    @staticmethod
    def get_experience_by_title(title):
        """
        Get a specific experience by title.
        """
        experience = Experience.objects.get(title=title)
        serializer = ExperienceSerializer(experience)
        return serializer.data
    

    @staticmethod
    def get_experience_by_company(company):
        """
        Get a specific experience by company.
        """
        experience = Experience.objects.get(company=company)
        serializer = ExperienceSerializer(experience)
        return serializer.data
    

    @staticmethod
    def get_experience_by_user(user_id):
        """
        Get all experiences by user.
        """
        experiences = Experience.objects.filter(user_id=user_id)
        serializer = ExperienceSerializer(experiences, many=True)
        return serializer.data
    

    # Education methods
    @staticmethod
    def get_educations():
        """
        Get all educations.
        """
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return serializer.data
    

    @staticmethod
    def get_education(education_id):
        """
        Get a specific education.
        """
        education = Education.objects.get(id=education_id)
        serializer = EducationSerializer(education)
        return serializer.data
    

    @staticmethod
    def get_education_by_institution(institution):
        """
        Get a specific education by institution.
        """
        education = Education.objects.get(institution=institution)
        serializer = EducationSerializer(education)
        return serializer.data
    

    @staticmethod
    def get_education_by_degree(degree):
        """
        Get a specific education by degree.
        """
        education = Education.objects.get(degree=degree)
        serializer = EducationSerializer(education)
        return serializer.data
    

    @staticmethod
    def get_education_by_field_of_study(field_of_study):
        """
        Get a specific education by field of study.
        """
        education = Education.objects.get(field_of_study=field_of_study)
        serializer = EducationSerializer(education)
        return serializer.data
    

    @staticmethod
    def get_education_by_user(user_id):
        """
        Get all educations by user.
        """
        educations = Education.objects.filter(user_id=user_id)
        serializer = EducationSerializer(educations, many=True)
        return serializer.data
    

    # Endorsement methods
    @staticmethod
    def get_endorsements():
        """
        Get all endorsements.
        """
        endorsements = Endorsement.objects.all()
        serializer = EndorsementSerializer(endorsements, many=True)
        return serializer.data
    

    @staticmethod
    def get_endorsement(endorsement_id):
        """
        Get a specific endorsement.
        """
        endorsement = Endorsement.objects.get(id=endorsement_id)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    @staticmethod
    def get_endorsement_by_skill(skill):
        """
        Get a specific endorsement by skill.
        """
        endorsement = Endorsement.objects.get(skill=skill)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    @staticmethod
    def get_endorsement_by_endorser(endorser):
        """
        Get a specific endorsement by endorser.
        """
        endorsement = Endorsement.objects.get(endorser=endorser)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    @staticmethod
    def get_endorsement_by_endorsed_user(endorsed_user):
        """
        Get a specific endorsement by endorsed user.
        """
        endorsement = Endorsement.objects.get(endorsed_user=endorsed_user)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    @staticmethod
    def get_endorsement_by_endorsed_user_and_skill(endorsed_user, skill):
        """
        Get a specific endorsement by endorsed user and skill.
        """
        endorsement = Endorsement.objects.get(endorsed_user=endorsed_user, skill=skill)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    @staticmethod
    def get_endorsement_by_endorser_and_skill(endorser, skill):
        """
        Get a specific endorsement by endorser and skill.
        """
        endorsement = Endorsement.objects.get(endorser=endorser, skill=skill)
        serializer = EndorsementSerializer(endorsement)
        return serializer.data
    

    # Achievement methods
    @staticmethod
    def get_achievements():
        """
        Get all achievements.
        """
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(achievements, many=True)
        return serializer.data
    

    @staticmethod
    def get_achievement(achievement_id):
        """
        Get a specific achievement.
        """
        achievement = Achievement.objects.get(id=achievement_id)
        serializer = AchievementSerializer(achievement)
        return serializer.data
    

    @staticmethod
    def get_achievement_by_title(title):
        """
        Get a specific achievement by title.
        """
        achievement = Achievement.objects.get(title=title)
        serializer = AchievementSerializer(achievement)
        return serializer.data
    

    @staticmethod
    def get_achievement_by_user(user_id):
        """
        Get all achievements by user.
        """
        achievements = Achievement.objects.filter(user_id=user_id)
        serializer = AchievementSerializer(achievements, many=True)
        return serializer.data
    

    # Portfolio methods
    @staticmethod
    def get_portfolios():
        """
        Get all portfolios.
        """
        portfolios = Portfolio.objects.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data
    

    @staticmethod
    def get_portfolio(portfolio_id):
        """
        Get a specific portfolio.
        """
        portfolio = Portfolio.objects.get(id=portfolio_id)
        serializer = PortfolioSerializer(portfolio)
        return serializer.data
    

    @staticmethod
    def get_portfolio_by_project_name(project_name):
        """
        Get a specific portfolio by project name.
        """
        portfolio = Portfolio.objects.get(project_name=project_name)
        serializer = PortfolioSerializer(portfolio)
        return serializer.data
    

    @staticmethod
    def get_portfolio_by_user(user_id):
        """
        Get all portfolios by user.
        """
        portfolios = Portfolio.objects.filter(user_id=user_id)
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data
    

