from profiles.models import UserProfile, Skill, Experience, Education, Endorsement
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserProfileSerializer, ExperienceSerializer, EducationSerializer, SkillSerializer, EndorsementSerializer
from profiles.actions.profile_actions import ProfileActions

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'include_user': self.request.query_params.get('include_user', 'false').lower() == 'true',
            'include_skills': self.request.query_params.get('include_skills', 'false').lower() == 'true',
            'include_experiences': self.request.query_params.get('include_experiences', 'false').lower() == 'true',
            'include_educations': self.request.query_params.get('include_educations', 'false').lower() == 'true',
            'include_endorsements': self.request.query_params.get('include_endorsements', 'false').lower() == 'true',
            'include_achievements': self.request.query_params.get('include_achievements', 'false').lower() == 'true',
            'include_portfolio': self.request.query_params.get('include_portfolio', 'false').lower() == 'true'
        })
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields')
        if fields:
            fields = fields.split(',')
            kwargs['fields'] = fields
        return serializer_class(*args, **kwargs)

    def perform_action(self, action_method, request, pk=None):
        profile = self.get_object()
        user_profile = request.user.profile
        result = action_method(request, profile, user_profile)
        return Response(result, status=result[1])

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        return self.perform_action(ProfileActions.follow_profile, request, pk)

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        return self.perform_action(ProfileActions.unfollow_profile, request, pk)

    @action(detail=True, methods=['post'])
    def endorse_skill(self, request, pk=None):
        return self.perform_action(ProfileActions.endorse_skill, request, pk)

    @action(detail=True, methods=['post'])
    def add_skill(self, request, pk=None):
        return self.perform_action(ProfileActions.add_skill, request, pk)

    @action(detail=True, methods=['post'])
    def remove_skill(self, request, pk=None):
        return self.perform_action(ProfileActions.remove_skill, request, pk)

    @action(detail=True, methods=['post'])
    def add_experience(self, request, pk=None):
        return self.perform_action(ProfileActions.add_experience, request, pk)

    @action(detail=True, methods=['post'])
    def remove_experience(self, request, pk=None):
        return self.perform_action(ProfileActions.remove_experience, request, pk)

    @action(detail=True, methods=['post'])
    def add_education(self, request, pk=None):
        return self.perform_action(ProfileActions.add_education, request, pk)

    @action(detail=True, methods=['post'])
    def remove_education(self, request, pk=None):
        return self.perform_action(ProfileActions.remove_education, request, pk)

    @action(detail=True, methods=['post'])
    def add_job_application(self, request, pk=None):
        return self.perform_action(ProfileActions.add_job_application, request, pk)

    @action(detail=True, methods=['post'])
    def remove_job_application(self, request, pk=None):
        return self.perform_action(ProfileActions.remove_job_application, request, pk)

    @action(detail=True, methods=['post'])
    def add_job_listing(self, request, pk=None):
        return self.perform_action(ProfileActions.add_job_listing, request, pk)

    @action(detail=True, methods=['post'])
    def remove_job_listing(self, request, pk=None):
        return self.perform_action(ProfileActions.remove_job_listing, request, pk)


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Experience.objects.all()
        return Experience.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Education.objects.all()
        return Education.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Skill.objects.all()
        return Skill.objects.filter(users=self.request.user.profile)

class EndorsementViewSet(viewsets.ModelViewSet):
    queryset = Endorsement.objects.all()
    serializer_class = EndorsementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Endorsement.objects.all()
        return Endorsement.objects.filter(endorsed_user=self.request.user.profile)

    def perform_action(self, action_method, request):
        profile = self.request.user.profile
        result = action_method(request, profile)
        return Response(result, status=result[1])

    @action(detail=False, methods=['post'])
    def add_achievement(self, request):
        return self.perform_action(ProfileActions.add_achievement, request)

    @action(detail=False, methods=['post'])
    def remove_achievement(self, request):
        return self.perform_action(ProfileActions.remove_achievement, request)
