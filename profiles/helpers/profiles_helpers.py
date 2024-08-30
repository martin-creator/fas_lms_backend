from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import UserProfile, User, Experience, Education, Skill, Endorsement, Achievement, Portfolio
from profiles.serializers import UserProfileSerializer, UserSerializer, ExperienceSerializer, EducationSerializer, SkillSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

class ProfileHelpers:
    @staticmethod
    def process_user_data(data):
        # add only profile and cover photo
        profile_picture = data.get('profile_picture')
        cover_photo = data.get('cover_photo')
        user = User(profile_picture=profile_picture, cover_photo=cover_photo)
        return user
    
    @staticmethod
    def process_user_data_update(user_id, data):
        user = User.objects.get(id=user_id)
        profile_picture = data.get('profile_picture')
        cover_photo = data.get('cover_photo')
        if profile_picture is not None:
            user.profile_picture = profile_picture
        if cover_photo is not None:
            user.cover_photo = cover_photo
        return user
    
    @staticmethod
    def process_user_profile_data(data):
        bio = data.get('bio')
        headline = data.get('headline')
        location = data.get('location')
        is_private = data.get('is_private')

        user_profile = UserProfile(bio=bio, headline=headline, location=location, is_private=is_private)
        return user_profile
    

    @staticmethod
    def process_user_profile_data_update(user_id, data):
        user_profile = UserProfile.objects.get(id=user_id)
        bio = data.get('bio')
        headline = data.get('headline')
        location = data.get('location')
        is_private = data.get('is_private')

        if bio is not None:
            user_profile.bio = bio
        if headline is not None:
            user_profile.headline = headline
        if location is not None:
            user_profile.location = location
        if is_private is not None:
            user_profile.is_private = is_private

        return user_profile
    

    @staticmethod
    def process_experience_data(data):
        title = data.get('title')
        company = data.get('company')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        experience = Experience(title=title, company=company, description=description, start_date=start_date, end_date=end_date, is_current=is_current)
        return experience
    

    @staticmethod
    def process_experience_data_update(experience_id, data):
        experience = Experience.objects.get(id=experience_id)
        title = data.get('title')
        company = data.get('company')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        if title is not None:
            experience.title = title
        if company is not None:
            experience.company = company
        if description is not None:
            experience.description = description
        if start_date is not None:
            experience.start_date = start_date
        if end_date is not None:
            experience.end_date = end_date
        if is_current is not None:
            experience.is_current = is_current

        return experience
    

    @staticmethod
    def process_education_data(data):
        institution = data.get('institution')
        degree = data.get('degree')
        field_of_study = data.get('field_of_study')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        education = Education(institution=institution, degree=degree, field_of_study=field_of_study, start_date=start_date, end_date=end_date, is_current=is_current)
        return education
    

    @staticmethod
    def process_education_data_update(education_id, data):
        education = Education.objects.get(id=education_id)
        institution = data.get('institution')
        degree = data.get('degree')
        field_of_study = data.get('field_of_study')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        if institution is not None:
            education.institution = institution
        if degree is not None:
            education.degree = degree
        if field_of_study is not None:
            education.field_of_study = field_of_study
        if start_date is not None:
            education.start_date = start_date
        if end_date is not None:
            education.end_date = end_date
        if is_current is not None:
            education.is_current = is_current

        return education
    

    @staticmethod
    def process_skill_data(data):
        name = data.get('name')
        proficiency = data.get('proficiency')

        skill = Skill(name=name, proficiency=proficiency)
        return skill
    

    @staticmethod
    def process_skill_data_update(skill_id, data):
        skill = Skill.objects.get(id=skill_id)
        name = data.get('name')
        proficiency = data.get('proficiency')

        if name is not None:
            skill.name = name
        if proficiency is not None:
            skill.proficiency = proficiency

        return skill
    

    @staticmethod
    def process_endorsement_data(data):
        skill = data.get('skill')
        endorsed_by = data.get('endorsed_by')
        endorsed_user = data.get('endorsed_user')

        endorsement = Endorsement(skill=skill, endorsed_by=endorsed_by, endorsed_user=endorsed_user)
        return endorsement
    

    @staticmethod
    def process_endorsement_data_update(endorsement_id, data):
        endorsement = Endorsement.objects.get(id=endorsement_id)
        skill = data.get('skill')
        endorsed_by = data.get('endorsed_by')
        endorsed_user = data.get('endorsed_user')

        if skill is not None:
            endorsement.skill = skill
        if endorsed_by is not None:
            endorsement.endorsed_by = endorsed_by
        if endorsed_user is not None:
            endorsement.endorsed_user = endorsed_user

        return endorsement
    

    @staticmethod
    def process_achievement_data(data):
        title = data.get('title')
        description = data.get('description')
        date_achieved = data.get('date_achieved')

        achievement = Achievement(title=title, description=description, date_achieved=date_achieved)
        return achievement
    

    @staticmethod
    def process_achievement_data_update(achievement_id, data):
        achievement = Achievement.objects.get(id=achievement_id)
        title = data.get('title')
        description = data.get('description')
        date_achieved = data.get('date_achieved')

        if title is not None:
            achievement.title = title
        if description is not None:
            achievement.description = description
        if date_achieved is not None:
            achievement.date_achieved = date_achieved

        return achievement
    

    @staticmethod
    def process_portfolio_data(data):
        project_name = data.get('project_name')
        description = data.get('description')
        project_url = data.get('project_url')

        portfolio = Portfolio(project_name=project_name, description=description, project_url=project_url)
        return portfolio
    

    @staticmethod
    def process_portfolio_data_update(portfolio_id, data):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        project_name = data.get('project_name')
        description = data.get('description')
        project_url = data.get('project_url')

        if project_name is not None:
            portfolio.project_name = project_name
        if description is not None:
            portfolio.description = description
        if project_url is not None:
            portfolio.project_url = project_url

        return portfolio
    

