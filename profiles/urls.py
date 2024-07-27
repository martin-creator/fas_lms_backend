from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import UserProfileViewSet, ExperienceViewSet, EducationViewSet, SkillViewSet, EndorsementViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'experiences', ExperienceViewSet, basename='experience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'endorsements', EndorsementViewSet, basename='endorsement')

# Nested routers for related entities
profiles_router = routers.NestedSimpleRouter(router, r'profiles', lookup='profile')
profiles_router.register(r'experiences', ExperienceViewSet, basename='profile-experience')
profiles_router.register(r'educations', EducationViewSet, basename='profile-education')
profiles_router.register(r'skills', SkillViewSet, basename='profile-skill')
profiles_router.register(r'endorsements', EndorsementViewSet, basename='profile-endorsement')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(profiles_router.urls)),
]
