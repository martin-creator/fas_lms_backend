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
        # Fetch the 'fields' parameter if it exists
        fields = kwargs.pop('fields', None)
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Remove fields not specified in 'fields' parameter
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_user(self, obj):
        return UserSerializer(obj.user, context=self.context).data

    def get_skills(self, obj):
        skills = obj.skills.all()
        return SkillSerializer(skills, many=True, context=self.context).data

    def get_experiences(self, obj):
        experiences = obj.experiences.all()
        return ExperienceSerializer(experiences, many=True, context=self.context).data

    def get_educations(self, obj):
        educations = obj.educations.all()
        return EducationSerializer(educations, many=True, context=self.context).data

    def get_endorsements(self, obj):
        endorsements = obj.endorsements.all()
        return EndorsementSerializer(endorsements, many=True, context=self.context).data

    def get_achievements(self, obj):
        achievements = obj.achievements.all()
        return AchievementSerializer(achievements, many=True, context=self.context).data

    def get_portfolio(self, obj):
        portfolio = obj.portfolio.all()
        return PortfolioSerializer(portfolio, many=True, context=self.context).data

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