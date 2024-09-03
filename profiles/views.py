from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from profiles.models import User, UserProfile, Follower, FollowRequest, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from profiles.serializers import UserSerializer, UserProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from profiles.controllers.profiles_controller import ProfileController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from allauth.account.views import ConfirmEmailView

############################### EMAIL CONFIRMATION ########################################


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirm.html'


###########################################################################################

# Create your views here.

profile_controller = ProfileController()

USER_PROFILE_VALUE = {
                'user': 'user',
                'bio': 'bio',
                'headline': 'headline',
                'location': 'location',
                'is_private': 'is_private',
                'joined_date': 'joined_date',
                'followers': 'followers',
                'skills': 'skills',
                'experiences': 'experiences',
                'educations': 'educations',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'followers': 'followers',
                'follow_requests': 'follow_requests',
                'shares': 'shares',
                'linkedin_id': 'linkedin_id',
                'linkedin_access_token': 'linkedin_access_token'
            }


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='data', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a user cover and profile picture',
            description='Update a user cover and profile picture',
            value={
                'user_id': 'user_id',
                'data': 'data'
            },
        )
    ],
    request=UserSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User data')}
)
@api_view(['PUT'])
def update_user_cover_and_profile_picture(request, user_id):
    """
    API endpoint that allows a user's cover and profile picture to be updated.
    """
    if request.method == 'PUT':
        user = profile_controller.update_user_cover_and_profile_picture(user_id, request.data)
        return Response(user, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all profiles',
            description='Get all profiles',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of profiles')}
)
@api_view(['GET'])
def get_all_profiles(request):
    """
    API endpoint that allows all profiles to be retrieved.
    """
    if request.method == 'GET':
        profiles = profile_controller.get_all_profiles()
        return Response(profiles, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific profile',
            description='Get a specific profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['GET'])
def get_specific_profile(request, profile_id):
    """
    API endpoint that allows a specific profile to be retrieved.
    """
    if request.method == 'GET':
        profile = profile_controller.get_profile(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='bio', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='headline', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_private', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='joined_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='skills', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='experiences', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='educations', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='endorsements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_listings', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='follow_requests', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='linkedin_id', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='linkedin_access_token', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new profile',
            description='Create a new profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def create_profile(request):
    """
    API endpoint that allows a new profile to be created.
    """
    if request.method == 'POST':
        profile = profile_controller.create_profile(request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='bio', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='headline', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_private', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='joined_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='skills', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='experiences', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='educations', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='endorsements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_listings', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='follow_requests', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='linkedin_id', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='linkedin_access_token', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a profile',
            description='Update a profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['PUT','GET'])
def update_profile(request, profile_id):
    """
    API endpoint that allows a profile to be updated.
    """
    if request.method == 'PUT':
        profile = profile_controller.update_profile(profile_id, request.data)
        return Response(profile, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        profile = profile_controller.get_profile(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a profile',
            description='Delete a profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['DELETE'])
def delete_profile(request, profile_id):
    """
    API endpoint that allows a profile to be deleted.
    """
    if request.method == 'DELETE':
        profile = profile_controller.delete_profile(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all profiles',
            description='Delete all profiles',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['DELETE'])
def delete_all_profiles(request):
    """
    API endpoint that allows all profiles to be deleted.
    """
    if request.method == 'DELETE':
        profiles = profile_controller.delete_all_profiles()
        return Response(profiles, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)    


@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Follow a profile',
            description='Follow a profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def follow_profile(request, profile_id):
    """
    API endpoint that allows a profile to be followed.
    """
    if request.method == 'POST':
        profile = profile_controller.follow_profile(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Unfollow a profile',
            description='Unfollow a profile',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def unfollow_profile(request, profile_id):
    """
    API endpoint that allows a profile to be unfollowed.
    """
    if request.method == 'POST':
        profile = profile_controller.unfollow_profile(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Accept a follow request',
            description='Accept a follow request',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def accept_follow_request(request, profile_id):
    """
    API endpoint that allows a follow request to be accepted.
    """
    if request.method == 'POST':
        profile = profile_controller.accept_follow_request(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Reject a follow request',
            description='Reject a follow request',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def reject_follow_request(request, profile_id):
    """
    API endpoint that allows a follow request to be rejected.
    """
    if request.method == 'POST':
        profile = profile_controller.reject_follow_request(profile_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='skill_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Endorse a skill',
            description='Endorse a skill',
            value={
                'skill': 'skill',
                'endorsed_by': 'endorsed_by',
                'endorsed_user': 'endorsed_user',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def endorse_skill(request, profile_id, skill_id):
    """
    API endpoint that allows a skill to be endorsed.
    """
    if request.method == 'POST':
        profile = profile_controller.endorse_skill(profile_id, skill_id)
        return Response(profile, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='company', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_current', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add an experience',
            description='Add an experience',
            value={
                'title': 'title',
                'company': 'company',
                'description': 'description',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def add_experience(request, profile_id):
    """
    API endpoint that allows an experience to be added.
    """
    if request.method == 'POST':
        profile = profile_controller.add_experience(profile_id, request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Add an education
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='institution', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='degree', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='field_of_study', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_current', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add an education',
            description='Add an education',
            value={
                'institution': 'institution',
                'degree': 'degree',
                'field_of_study': 'field_of_study',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def add_education(request, profile_id):
    """
    API endpoint that allows an education to be added.
    """
    if request.method == 'POST':
        profile = profile_controller.add_education(profile_id, request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Add a skill
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='proficiency', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='endorsements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_listings', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verified_from', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verified_to', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a skill',
            description='Add a skill',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def add_skill(request, profile_id):
    """
    API endpoint that allows a skill to be added.
    """
    if request.method == 'POST':
        profile = profile_controller.add_skill(profile_id, request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Add an achievement
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='date_achieved', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add an achievement',
            description='Add an achievement',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def add_achievement(request, profile_id):
    """
    API endpoint that allows an achievement to be added.
    """
    if request.method == 'POST':
        profile = profile_controller.add_achievement(profile_id, request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Add a portfolio
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='project_url', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a portfolio',
            description='Add a portfolio',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile data')}
)
@api_view(['POST'])
def add_portfolio(request, profile_id):
    """
    API endpoint that allows a portfolio to be added.
    """
    if request.method == 'POST':
        profile = profile_controller.add_portfolio(profile_id, request.data)
        return Response(profile, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# Get all followers for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all followers',
            description='Get all followers',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of followers')}
)
@api_view(['GET'])
def get_followers(request, profile_id):
    """
    API endpoint that allows all followers for a profile to be retrieved.
    """
    if request.method == 'GET':
        followers = profile_controller.get_followers(profile_id)
        return Response(followers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get all experiences for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all experiences',
            description='Get all experiences',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of experiences')}
)
@api_view(['GET'])
def get_experiences(request, profile_id):
    """
    API endpoint that allows all experiences for a profile to be retrieved.
    """
    if request.method == 'GET':
        experiences = profile_controller.get_experiences(profile_id)
        return Response(experiences, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get a specific experience for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='experience_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific experience',
            description='Get a specific experience',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Experience data')}
)
@api_view(['GET'])
def get_experience(request, profile_id, experience_id):
    """
    API endpoint that allows a specific experience for a profile to be retrieved.
    """
    if request.method == 'GET':
        experience = profile_controller.get_experience(profile_id, experience_id)
        return Response(experience, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Update an experience for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='experience_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='company', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_current', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an experience',
            description='Update an experience',
            value={
                'title': 'title',
                'company': 'company',
                'description': 'description',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Experience data')}
)
@api_view(['PUT'])
def update_experience(request, profile_id, experience_id):
    """
    API endpoint that allows an experience for a profile to be updated.
    """
    if request.method == 'PUT':
        experience = profile_controller.update_experience(profile_id, experience_id, request.data)
        return Response(experience, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete an experience for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='experience_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an experience',
            description='Delete an experience',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Experience data')}
)
@api_view(['DELETE'])
def delete_experience(request, profile_id, experience_id):
    """
    API endpoint that allows an experience for a profile to be deleted.
    """
    if request.method == 'DELETE':
        experience = profile_controller.delete_experience(profile_id, experience_id)
        return Response(experience, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete all experiences for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all experiences',
            description='Delete all experiences',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Experience data')}
)
@api_view(['DELETE'])
def delete_all_experiences(request, profile_id):
    """
    API endpoint that allows all experiences for a profile to be deleted.
    """
    if request.method == 'DELETE':
        experiences = profile_controller.delete_all_experiences(profile_id)
        return Response(experiences, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get all educations for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all educations',
            description='Get all educations',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of educations')}
)
@api_view(['GET'])
def get_educations(request, profile_id):
    """
    API endpoint that allows all educations for a profile to be retrieved.
    """
    if request.method == 'GET':
        educations = profile_controller.get_educations(profile_id)
        return Response(educations, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get a specific education for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='education_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific education',
            description='Get a specific education',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Education data')}
)
@api_view(['GET'])
def get_education(request, profile_id, education_id):
    """
    API endpoint that allows a specific education for a profile to be retrieved.
    """
    if request.method == 'GET':
        education = profile_controller.get_education(profile_id, education_id)
        return Response(education, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Update an education for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='education_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='institution', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='degree', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='field_of_study', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_current', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an education',
            description='Update an education',
            value={
                'institution': 'institution',
                'degree': 'degree',
                'field_of_study': 'field_of_study',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Education data')}
)
@api_view(['PUT'])
def update_education(request, profile_id, education_id):
    """
    API endpoint that allows an education for a profile to be updated.
    """
    if request.method == 'PUT':
        education = profile_controller.update_education(profile_id, education_id, request.data)
        return Response(education, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete an education for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='education_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an education',
            description='Delete an education',
            value={
                'institution': 'institution',
                'degree': 'degree',
                'field_of_study': 'field_of_study',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Education data')}
)
@api_view(['DELETE'])
def delete_education(request, profile_id, education_id):
    """
    API endpoint that allows an education for a profile to be deleted.
    """
    if request.method == 'DELETE':
        education = profile_controller.delete_education(profile_id, education_id)
        return Response(education, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete all educations for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all educations',
            description='Delete all educations',
            value={
                'institution': 'institution',
                'degree': 'degree',
                'field_of_study': 'field_of_study',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'is_current': 'is_current',
                'shares': 'shares'
            }
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Education data')}
)
@api_view(['DELETE'])
def delete_all_educations(request, profile_id):
    """
    API endpoint that allows all educations for a profile to be deleted.
    """
    if request.method == 'DELETE':
        educations = profile_controller.delete_all_educations(profile_id)
        return Response(educations, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get all skills for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all skills',
            description='Get all skills',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            },
        )
    ],
    request=SkillSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of skills')}
)
@api_view(['GET'])
def get_skills(request, profile_id):
    """
    API endpoint that allows all skills for a profile to be retrieved.
    """
    if request.method == 'GET':
        skills = profile_controller.get_skills(profile_id)
        return Response(skills, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get a specific skill for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='skill_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific skill',
            description='Get a specific skill',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            },
        )
    ],
    request=SkillSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Skill data')}
)
@api_view(['GET'])
def get_skill(request, profile_id, skill_id):
    """
    API endpoint that allows a specific skill for a profile to be retrieved.
    """
    if request.method == 'GET':
        skill = profile_controller.get_skill(profile_id, skill_id)
        return Response(skill, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Update a skill for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='skill_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='proficiency', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='endorsements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='job_listings', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verified_from', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verified_to', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a skill',
            description='Update a skill',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            },
        )
    ],
    request=SkillSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Skill data')}
)
@api_view(['PUT'])
def update_skill(request, profile_id, skill_id):
    """
    API endpoint that allows a skill for a profile to be updated.
    """
    if request.method == 'PUT':
        skill = profile_controller.update_skill(profile_id, skill_id, request.data)
        return Response(skill, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete a skill for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='skill_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a skill',
            description='Delete a skill',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            },
        )
    ],
    request=SkillSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Skill data')}
)
@api_view(['DELETE'])
def delete_skill(request, profile_id, skill_id):
    """
    API endpoint that allows a skill for a profile to be deleted.
    """
    if request.method == 'DELETE':
        skill = profile_controller.delete_skill(profile_id, skill_id)
        return Response(skill, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Delete all skills for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all skills',
            description='Delete all skills',
            value={
                'name': 'name',
                'proficiency': 'proficiency',
                'shares': 'shares',
                'endorsements': 'endorsements',
                'job_applications': 'job_applications',
                'job_listings': 'job_listings',
                'notifications': 'notifications',
                'verified_from': 'verified_from',
                'verified_to': 'verified_to'
            },
        )
    ],
    request=SkillSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Skill data')}
)
@api_view(['DELETE'])
def delete_all_skills(request, profile_id):
    """
    API endpoint that allows all skills for a profile to be deleted.
    """
    if request.method == 'DELETE':
        skills = profile_controller.delete_all_skills(profile_id)
        return Response(skills, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get all achievements for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all achievements',
            description='Get all achievements',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            },
        )
    ],
    request=AchievementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of achievements')}
)
@api_view(['GET'])
def get_achievements(request, profile_id):
    """
    API endpoint that allows all achievements for a profile to be retrieved.
    """
    if request.method == 'GET':
        achievements = profile_controller.get_achievements(profile_id)
        return Response(achievements, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Get a specific achievement for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='achievement_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific achievement',
            description='Get a specific achievement',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            },
        )
    ],
    request=AchievementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Achievement data')}
)
@api_view(['GET'])
def get_achievement(request, profile_id, achievement_id):
    """
    API endpoint that allows a specific achievement for a profile to be retrieved.
    """
    if request.method == 'GET':
        achievement = profile_controller.get_achievement(profile_id, achievement_id)
        return Response(achievement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Update an achievement for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='achievement_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='date_achieved', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an achievement',
            description='Update an achievement',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            },
        )
    ],
    request=AchievementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Achievement data')}
)
@api_view(['PUT'])
def update_achievement(request, profile_id, achievement_id):
    """
    API endpoint that allows an achievement for a profile to be updated.
    """
    if request.method == 'PUT':
        achievement = profile_controller.update_achievement(profile_id, achievement_id, request.data)
        return Response(achievement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Delete an achievement for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='achievement_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an achievement',
            description='Delete an achievement',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            },
        )
    ],
    request=AchievementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Achievement data')}
)
@api_view(['DELETE'])
def delete_achievement(request, profile_id, achievement_id):
    """
    API endpoint that allows an achievement for a profile to be deleted.
    """
    if request.method == 'DELETE':
        achievement = profile_controller.delete_achievement(profile_id, achievement_id)
        return Response(achievement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Delete all achievements for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all achievements',
            description='Delete all achievements',
            value={
                'title': 'title',
                'description': 'description',
                'date_achieved': 'date_achieved'
            },
        )
    ],
    request=AchievementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Achievement data')}
)
@api_view(['DELETE'])
def delete_all_achievements(request, profile_id):
    """
    API endpoint that allows all achievements for a profile to be deleted.
    """
    if request.method == 'DELETE':
        achievements = profile_controller.delete_all_achievements(profile_id)
        return Response(achievements, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Get all portfolios for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all portfolios',
            description='Get all portfolios',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            },
        )
    ],
    request=PortfolioSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of portfolios')}
)
@api_view(['GET'])
def get_portfolios(request, profile_id):
    """
    API endpoint that allows all portfolios for a profile to be retrieved.
    """
    if request.method == 'GET':
        portfolios = profile_controller.get_portfolios(profile_id)
        return Response(portfolios, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Get a specific portfolio for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='portfolio_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific portfolio',
            description='Get a specific portfolio',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            },
        )
    ],
    request=PortfolioSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Portfolio data')}
)
@api_view(['GET'])
def get_portfolio(request, profile_id, portfolio_id):
    """
    API endpoint that allows a specific portfolio for a profile to be retrieved.
    """
    if request.method == 'GET':
        portfolio = profile_controller.get_portfolio(profile_id, portfolio_id)
        return Response(portfolio, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Update a portfolio for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='portfolio_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='project_url', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a portfolio',
            description='Update a portfolio',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            },
        )
    ],
    request=PortfolioSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Portfolio data')}
)
@api_view(['PUT'])
def update_portfolio(request, profile_id, portfolio_id):
    """
    API endpoint that allows a portfolio for a profile to be updated.
    """
    if request.method == 'PUT':
        portfolio = profile_controller.update_portfolio(profile_id, portfolio_id, request.data)
        return Response(portfolio, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Delete a portfolio for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='portfolio_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a portfolio',
            description='Delete a portfolio',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            },
        )
    ],
    request=PortfolioSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Portfolio data')}
)
@api_view(['DELETE'])
def delete_portfolio(request, profile_id, portfolio_id):
    """
    API endpoint that allows a portfolio for a profile to be deleted.
    """
    if request.method == 'DELETE':
        portfolio = profile_controller.delete_portfolio(profile_id, portfolio_id)
        return Response(portfolio, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Delete all portfolios for a profile
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all portfolios',
            description='Delete all portfolios',
            value={
                'project_name': 'project_name',
                'description': 'description',
                'project_url': 'project_url'
            },
        )
    ],
    request=PortfolioSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Portfolio data')}
)
@api_view(['DELETE'])
def delete_all_portfolios(request, profile_id):
    """
    API endpoint that allows all portfolios for a profile to be deleted.
    """
    if request.method == 'DELETE':
        portfolios = profile_controller.delete_all_portfolios(profile_id)
        return Response(portfolios, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Get profile report
@extend_schema(
    parameters=[
        OpenApiParameter(name='profile_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get profile report',
            description='Get profile report',
            value=USER_PROFILE_VALUE
        )
    ],
    request=UserProfileSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Profile report')}
)
@api_view(['GET'])
def get_profile_report(request, profile_id):
    """
    API endpoint that allows a profile report to be retrieved.
    """
    if request.method == 'GET':
        profile_report = profile_controller.get_profile_report(profile_id)
        return Response(profile_report, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Generare url patterns for all the views above following this format.
# the functions SHOULD be imported from the views.function
# urlpatterns = [
#     path('', views.get_companies, name='get_companies'),
#     path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
#     path('companies/create/', views.create_company, name='create_company'),
#     path('companies/update/<int:company_id>/', views.update_company, name='update_company'),
#     path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
#     path('companies/delete/all/', views.delete_all_companies, name='delete_all_companies'),
#     path('companies/updates/<int:company_id>/', views.get_company_updates, name='get_company_updates'),
#     path('<int:update_id>/', views.get_specific_company_update, name='get_specific_company_update'),
#     path('companies/updates/create/<int:company_id>/', views.create_company_update, name='create_company_update'),
#     path('companies/updates/update/<int:company_id>/<int:update_id>/', views.update_company_update, name='update_company_update'),
#     path('companies/updates/delete/<int:update_id>/', views.delete_company_update, name='delete_company_update'),
#     # path('events/', views.get_events),
#     # path('events/<int:event_id>/', views.get_event),
#     # path('events/create/', views.create_event),
# ]
    
    



