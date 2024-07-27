# profiles/actions/education_experience_actions.py

from profiles.models import Experience, Education, Skill

class EducationExperienceActions:

    @staticmethod
    def add_experience(profile, title, company, description, start_date, end_date=None, is_current=False):
        experience = Experience.objects.create(
            user_profile=profile,
            title=title,
            company=company,
            description=description,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )
        return experience

    @staticmethod
    def remove_experience(profile, experience_id):
        try:
            experience = Experience.objects.get(id=experience_id, user_profile=profile)
            experience.delete()
            return {'status': 'Experience removed'}, 200
        except Experience.DoesNotExist:
            return {'error': 'Experience not found'}, 404

    @staticmethod
    def add_education(profile, institution, degree, field_of_study, start_date, end_date=None, is_current=False):
        education = Education.objects.create(
            user_profile=profile,
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )
        return education

    @staticmethod
    def remove_education(profile, education_id):
        try:
            education = Education.objects.get(id=education_id, user_profile=profile)
            education.delete()
            return {'status': 'Education removed'}, 200
        except Education.DoesNotExist:
            return {'error': 'Education not found'}, 404

    @staticmethod
    def endorse_skill(request, profile):
        skill_name = request.data.get('skill')
        if not skill_name:
            return {'error': 'Skill not provided'}, 400
        skill, created = Skill.objects.get_or_create(name=skill_name)
        profile.endorse_skill(skill, request.user.profile)
        return {'status': f'Skill {skill_name} endorsed'}, 200

    @staticmethod
    def add_skill(request, profile):
        skill_name = request.data.get('skill')
        if not skill_name:
            return {'error': 'Skill not provided'}, 400
        skill, created = Skill.objects.get_or_create(name=skill_name)
        profile.skills.add(skill)
        return {'status': f'Skill {skill_name} added'}, 200

    @staticmethod
    def remove_skill(request, profile):
        skill_name = request.data.get('skill')
        if not skill_name:
            return {'error': 'Skill not provided'}, 400
        skill = Skill.objects.filter(name=skill_name).first()
        if not skill:
            return {'error': 'Skill not found'}, 404
        profile.skills.remove(skill)
        return {'status': f'Skill {skill_name} removed'}, 200
