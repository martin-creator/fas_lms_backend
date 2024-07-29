from profiles.models import UserProfile, Skill, Experience, Education, Endorsement
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserProfileSerializer, ExperienceSerializer, EducationSerializer, SkillSerializer, EndorsementSerializer
from profiles.actions.profile_actions import ProfileActions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username', 'bio', 'headline']
    ordering_fields = ['joined_date', 'location']
    filterset_fields = ['is_private', 'location']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        query_params = self.request.query_params
        flags = [
            'include_user', 'include_skills', 
            'include_experiences', 'include_educations',
            'include_endorsements', 'include_achievements', 
            'include_portfolio'
        ]
        context.update({flag: query_params.get(flag, 'false').lower() == 'true' for flag in flags})
        return context

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        fields = self.request.query_params.get('fields')
        if fields:
            kwargs['fields'] = fields.split(',')
        return serializer_class(*args, **kwargs)

    def perform_action(self, request, action_name):
        try:
            profile = self.get_object()
            user_profile = request.user.profile
            action_method = getattr(ProfileActions, action_name, None)
            if not action_method:
                raise ValueError(f"Unknown action: {action_name}")

            result = action_method(request, profile, user_profile)
            return Response(result[0], status=result[1])
        except PermissionDenied as e:
            logger.warning(f"Permission denied: {e}")
            return Response({'detail': str(e)}, status=403)
        except ValueError as e:
            logger.error(f"Value error: {e}")
            return Response({'detail': str(e)}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return Response({'detail': 'An unexpected error occurred.'}, status=500)

    def create_action(method_name):
        @action(detail=True, methods=['post'])
        def action_method(self, request, pk=None):
            return self.perform_action(request, method_name)
        return action_method

    follow = create_action('follow_profile')
    unfollow = create_action('unfollow_profile')
    endorse_skill = create_action('endorse_skill')
    add_skill = create_action('add_skill')
    remove_skill = create_action('remove_skill')
    add_experience = create_action('add_experience')
    remove_experience = create_action('remove_experience')
    add_education = create_action('add_education')
    remove_education = create_action('remove_education')
    add_job_application = create_action('add_job_application')
    remove_job_application = create_action('remove_job_application')
    add_job_listing = create_action('add_job_listing')
    remove_job_listing = create_action('remove_job_listing')
    add_achievement = create_action('add_achievement')
    remove_achievement = create_action('remove_achievement')
    add_portfolio = create_action('add_portfolio')
    remove_portfolio = create_action('remove_portfolio')


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
