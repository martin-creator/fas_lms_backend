# profiles/utils/profiles_utils.py
from profiles.models import Skill, Experience, Education, Endorsement
from jobs.utils.jobs import JobUtils

class ProfileUtils:
    @staticmethod
    def add_skill_to_profile(profile, skill_name):
        skill, created = Skill.objects.get_or_create(name=skill_name)
        profile.skills.add(skill)
        return skill

    @staticmethod
    def remove_skill_from_profile(profile, skill_name):
        skill = Skill.objects.filter(name=skill_name).first()
        if skill:
            profile.skills.remove(skill)
            return skill
        return None

    @staticmethod
    def add_experience_to_profile(profile, data):
        return Experience.objects.create(
            user_profile=profile,
            title=data.get('title'),
            company=data.get('company'),
            description=data.get('description'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            is_current=data.get('is_current', False)
        )

    @staticmethod
    def remove_experience_from_profile(profile, experience_id):
        experience = Experience.objects.filter(id=experience_id, user_profile=profile).first()
        if experience:
            experience.delete()
            return experience
        return None

    @staticmethod
    def add_education_to_profile(profile, data):
        return Education.objects.create(
            user_profile=profile,
            institution=data.get('institution'),
            degree=data.get('degree'),
            field_of_study=data.get('field_of_study'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            is_current=data.get('is_current', False)
        )

    @staticmethod
    def remove_education_from_profile(profile, education_id):
        education = Education.objects.filter(id=education_id, user_profile=profile).first()
        if education:
            education.delete()
            return education
        return None

    @staticmethod
    def handle_follow_request(profile, from_user_profile, action):
        if action == 'accept':
            profile.accept_follow_request(from_user_profile)
        elif action == 'reject':
            profile.reject_follow_request(from_user_profile)
        return action
