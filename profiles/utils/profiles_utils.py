from profiles.models import UserProfile, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils import timezone

class ProfileUtils:
    
    @staticmethod
    def create_profile(user, bio='', headline='', location='', is_private=False):
        """
        Create a UserProfile instance for a given user.
        """
        try:
            profile = UserProfile.objects.create(
                user=user,
                bio=bio,
                headline=headline,
                location=location,
                is_private=is_private,
                joined_date=timezone.now()
            )
            return profile
        except IntegrityError as e:
            raise e

    @staticmethod
    def get_profile(user):
        """
        Retrieve a UserProfile instance for a given user.
        """
        try:
            return UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            raise ObjectDoesNotExist("Profile does not exist for this user.")

    @staticmethod
    def update_profile(user, **kwargs):
        """
        Update the UserProfile instance for a given user with provided fields.
        """
        profile = ProfileUtils.get_profile(user)
        for key, value in kwargs.items():
            setattr(profile, key, value)
        profile.save()
        return profile

    @staticmethod
    def delete_profile(user):
        """
        Delete the UserProfile instance for a given user.
        """
        profile = ProfileUtils.get_profile(user)
        profile.delete()
        return True

    @staticmethod
    def add_skill(user, skill_name, proficiency):
        """
        Add a skill to the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        skill, created = Skill.objects.get_or_create(name=skill_name, proficiency=proficiency)
        profile.skills.add(skill)
        return skill

    @staticmethod
    def remove_skill(user, skill_name):
        """
        Remove a skill from the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            skill = Skill.objects.get(name=skill_name)
            profile.skills.remove(skill)
            return True
        except Skill.DoesNotExist:
            raise ObjectDoesNotExist("Skill does not exist.")

    @staticmethod
    def add_experience(user, title, company, description, start_date, end_date=None, is_current=False):
        """
        Add an experience to the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        experience = Experience.objects.create(
            user=profile,
            title=title,
            company=company,
            description=description,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )
        return experience

    @staticmethod
    def remove_experience(user, experience_id):
        """
        Remove an experience from the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            experience = Experience.objects.get(id=experience_id, user=profile)
            experience.delete()
            return True
        except Experience.DoesNotExist:
            raise ObjectDoesNotExist("Experience does not exist.")

    @staticmethod
    def add_education(user, institution, degree, field_of_study, start_date, end_date=None, is_current=False):
        """
        Add an education to the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        education = Education.objects.create(
            user=profile,
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )
        return education

    @staticmethod
    def remove_education(user, education_id):
        """
        Remove an education from the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            education = Education.objects.get(id=education_id, user=profile)
            education.delete()
            return True
        except Education.DoesNotExist:
            raise ObjectDoesNotExist("Education does not exist.")

    @staticmethod
    def endorse_skill(user, skill_name, endorsed_by):
        """
        Endorse a skill for the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            skill = Skill.objects.get(name=skill_name)
            endorsement = Endorsement.objects.create(
                skill=skill,
                endorsed_by=endorsed_by.profile,
                endorsed_user=profile
            )
            return endorsement
        except Skill.DoesNotExist:
            raise ObjectDoesNotExist("Skill does not exist.")

    @staticmethod
    def add_achievement(user, title, description, date_achieved):
        """
        Add an achievement to the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        achievement = Achievement.objects.create(
            user=profile,
            title=title,
            description=description,
            date_achieved=date_achieved
        )
        return achievement

    @staticmethod
    def remove_achievement(user, achievement_id):
        """
        Remove an achievement from the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            achievement = Achievement.objects.get(id=achievement_id, user=profile)
            achievement.delete()
            return True
        except Achievement.DoesNotExist:
            raise ObjectDoesNotExist("Achievement does not exist.")

    @staticmethod
    def add_portfolio(user, project_name, description, project_url):
        """
        Add a portfolio project to the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        portfolio = Portfolio.objects.create(
            user=profile,
            project_name=project_name,
            description=description,
            project_url=project_url
        )
        return portfolio

    @staticmethod
    def remove_portfolio(user, portfolio_id):
        """
        Remove a portfolio project from the UserProfile instance.
        """
        profile = ProfileUtils.get_profile(user)
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id, user=profile)
            portfolio.delete()
            return True
        except Portfolio.DoesNotExist:
            raise ObjectDoesNotExist("Portfolio project does not exist.")
