from rest_framework import serializers
from .models import User, UserProfile, Skill, Experience, Education, Endorsement, Achievement, Portfolio

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    experiences = serializers.SerializerMethodField()
    educations = serializers.SerializerMethodField()
    endorsements = serializers.SerializerMethodField()
    achievements = serializers.SerializerMethodField()
    portfolio = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        context = self.context
        include_flags = {
            'user': context.get('include_user'),
            'skills': context.get('include_skills'),
            'experiences': context.get('include_experiences'),
            'educations': context.get('include_educations'),
            'endorsements': context.get('include_endorsements'),
            'achievements': context.get('include_achievements'),
            'portfolio': context.get('include_portfolio')
        }
        for field_name, include_flag in include_flags.items():
            if not include_flag:
                self.fields.pop(field_name, None)

    def get_user(self, obj):
        return UserSerializer(obj.user, context=self.context).data

    def get_related_field(self, obj, related_name, serializer_class):
        related_objects = getattr(obj, related_name).all()
        return serializer_class(related_objects, many=True, context=self.context).data

    def get_skills(self, obj):
        return self.get_related_field(obj, 'skills', SkillSerializer)

    def get_experiences(self, obj):
        return self.get_related_field(obj, 'experiences', ExperienceSerializer)

    def get_educations(self, obj):
        return self.get_related_field(obj, 'educations', EducationSerializer)

    def get_endorsements(self, obj):
        return self.get_related_field(obj, 'endorsements', EndorsementSerializer)

    def get_achievements(self, obj):
        return self.get_related_field(obj, 'achievements', AchievementSerializer)

    def get_portfolio(self, obj):
        return self.get_related_field(obj, 'portfolio', PortfolioSerializer)

class SkillSerializer(serializers.ModelSerializer):
    endorsement_count = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = '__all__'

    def get_endorsement_count(self, obj):
        return obj.endorsements.count()

class ExperienceSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = '__all__'

    def get_company_name(self, obj):
        return obj.company.name if obj.company else None

class EducationSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = '__all__'

    def get_duration(self, obj):
        if obj.end_date:
            duration = (obj.end_date - obj.start_date).days
            return duration
        return None

class EndorsementSerializer(serializers.ModelSerializer):
    endorsed_user_name = serializers.SerializerMethodField()
    endorsed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Endorsement
        fields = '__all__'

    def get_endorsed_user_name(self, obj):
        return obj.endorsed_user.user.username

    def get_endorsed_by_name(self, obj):
        return obj.endorsed_by.user.username

class AchievementSerializer(serializers.ModelSerializer):
    year_achieved = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = '__all__'

    def get_year_achieved(self, obj):
        return obj.date_achieved.year

class PortfolioSerializer(serializers.ModelSerializer):
    project_summary = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = '__all__'

    def get_project_summary(self, obj):
        return f"{obj.project_name} - {obj.description[:50]}..."