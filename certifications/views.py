from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from certifications.controllers.certifications_controller import CertificationController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


# Create your views here.

certification_controller = CertificationController()


# linkedin login
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='LinkedIn login',
            description='LinkedIn login',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn login')}

)
@api_view(['GET'])
def linkedin_login(request):
    """
    API endpoint that allows users to be redirected to LinkedIn for authentication.
    """
    if request.method == 'GET':
        return certification_controller.linkedin_login(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# linkedin callback
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='LinkedIn callback',
            description='LinkedIn callback',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn callback')}

)
@api_view(['GET'])
def linkedin_callback(request):
    """
    API endpoint that allows the authorization code from LinkedIn to be received and exchanged for an access token.
    """
    if request.method == 'GET':
        return certification_controller.linkedin_callback(request)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get all certifications

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all certifications',
            description='Get all certifications',
            value={
                'user': 'user',
                'name': 'name',
                'issuing_organization': 'issuing_organization',
                'issue_date': 'issue_date',
                'expiration_date': 'expiration_date',
                'credential_id': 'credential_id',
                'credential_url': 'credential_url',
                'description': 'description',
                'categories': 'categories',
                'certificate_image': 'certificate_image',
                'verification_status': 'verification_status',
                'related_jobs': 'related_jobs',
                'related_courses': 'related_courses',
                'related_events': 'related_events',
                'revoked': 'revoked'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of certifications')}
)
@api_view(['GET'])
def get_certifications(request):
    """
    API endpoint that allows all certifications to be retrieved.
    """
    if request.method == 'GET':
        certifications = certification_controller.get_all_certifications()
        return Response(certifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# get specific certification
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific certification',
            description='Get a specific certification',
            value={
                'user': 'user',
                'name': 'name',
                'issuing_organization': 'issuing_organization',
                'issue_date': 'issue_date',
                'expiration_date': 'expiration_date',
                'credential_id': 'credential_id',
                'credential_url': 'credential_url',
                'description': 'description',
                'categories': 'categories',
                'certificate_image': 'certificate_image',
                'verification_status': 'verification_status',
                'related_jobs': 'related_jobs',
                'related_courses': 'related_courses',
                'related_events': 'related_events',
                'revoked': 'revoked'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}

)
@api_view(['GET'])
def get_specific_certification(request, certification_id):
    """
    API endpoint that allows a specific certification to be retrieved.
    """
    if request.method == 'GET':
        certification = certification_controller.get_certification_by_id(certification_id)
        return Response(certification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get certifications by user
@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all certifications for a specific user',
            description='Get all certifications for a specific user',
            value={
                'user': 'user',
                'name': 'name',
                'issuing_organization': 'issuing_organization',
                'issue_date': 'issue_date',
                'expiration_date': 'expiration_date',
                'credential_id': 'credential_id',
                'credential_url': 'credential_url',
                'description': 'description',
                'categories': 'categories',
                'certificate_image': 'certificate_image',
                'verification_status': 'verification_status',
                'related_jobs': 'related_jobs',
                'related_courses': 'related_courses',
                'related_events': 'related_events',
                'revoked': 'revoked'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of certifications')}

)
@api_view(['GET'])
def get_certifications_by_user(request):
    """
    API endpoint that allows all certifications for a specific user to be retrieved.
    """
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        certifications = certification_controller.get_certifications_by_user(user_id)
        return Response(certifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# create certification
@extend_schema(
    parameters=[
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='issuing_organization', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='issue_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='expiration_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='credential_id', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='credential_url', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='certificate_image', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verification_status', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_jobs', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_courses', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_events', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='revoked', type=bool, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new certification',
            description='Create a new certification',
            value={
                'user': 'user',
                'name': 'name',
                'issuing_organization': 'issuing_organization',
                'issue_date': 'issue_date',
                'expiration_date': 'expiration_date',
                'credential_id': 'credential_id',
                'credential_url': 'credential_url',
                'description': 'description',
                'categories': 'categories',
                'certificate_image': 'certificate_image',
                'verification_status': 'verification_status',
                'related_jobs': 'related_jobs',
                'related_courses': 'related_courses',
                'related_events': 'related_events',
                'revoked': 'revoked'
            }
        )
    ],
    request=CertificationSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}
)
@api_view(['POST'])
def create_certification(request):
    """
    API endpoint that allows a new certification to be created.
    """
    if request.method == 'POST':
        certification = certification_controller.create_certification(request.data)
        return Response(certification, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# update certification
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='issuing_organization', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='issue_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='expiration_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='credential_id', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='credential_url', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='certificate_image', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='verification_status', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_jobs', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_courses', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='related_events', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='revoked', type=bool, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a certification',
            description='Update a certification',
            value={
                'user': 'user',
                'name': 'name',
                'issuing_organization': 'issuing_organization',
                'issue_date': 'issue_date',
                'expiration_date': 'expiration_date',
                'credential_id': 'credential_id',
                'credential_url': 'credential_url',
                'description': 'description',
                'categories': 'categories',
                'certificate_image': 'certificate_image',
                'verification_status': 'verification_status',
                'related_jobs': 'related_jobs',
                'related_courses': 'related_courses',
                'related_events': 'related_events',
                'revoked': 'revoked'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}
)
@api_view(['PUT'])
def update_certification(request, certification_id):
    """
    API endpoint that allows a certification to be updated.
    """
    if request.method == 'PUT':
        certification = certification_controller.update_certification(certification_id, request.data)
        return Response(certification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# delete certification
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a certification',
            description='Delete a certification',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}

)
@api_view(['DELETE'])
def delete_certification(request, certification_id):
    """
    API endpoint that allows a certification to be deleted.
    """
    if request.method == 'DELETE':
        certification = certification_controller.delete_certification(certification_id)
        return Response(certification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# generate pdf certificate
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Generate a PDF certificate',
            description='Generate a PDF certificate',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}

)
@api_view(['GET'])
def generate_pdf_certificate(request, certification_id):
    """
    API endpoint that allows a PDF certificate to be generated for a specific certification.
    """
    if request.method == 'GET':
        certificate = certification_controller.generate_pdf_certificate(certification_id)
        return Response(certificate, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# verify certificate
@extend_schema(
    parameters=[
        OpenApiParameter(name='credential_id', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Verify a certificate',
            description='Verify a certificate',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}
)
@api_view(['GET'])
def verify_certificate(request, credential_id):
    """
    API endpoint that allows a certificate to be verified using the credential ID.
    """
    if request.method == 'GET':
        certificate = certification_controller.verify_certificate(credential_id)
        return Response(certificate, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# revoke certificate
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Revoke a certification',
            description='Revoke a certification',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Certification data')}

)
@api_view(['PUT'])
def revoke_certificate(request, certification_id):
    """
    API endpoint that allows a certification to be revoked.
    """
    if request.method == 'PUT':
        certification = certification_controller.revoke_certificate(certification_id)
        return Response(certification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get all linkedin badges
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all LinkedIn badges',
            description='Get all LinkedIn badges',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of LinkedIn badges')}

)
@api_view(['GET'])
def get_all_linkedin_badges(request):
    """
    API endpoint that allows all LinkedIn badges to be retrieved.
    """
    if request.method == 'GET':
        linkedin_badges = certification_controller.get_all_linkedin_badges()
        return Response(linkedin_badges, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get specific linkedin badge
@extend_schema(
    parameters=[
        OpenApiParameter(name='badge_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific LinkedIn badge',
            description='Get a specific LinkedIn badge',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['GET'])
def get_specific_linkedin_badge(request, badge_id):
    """
    API endpoint that allows a specific LinkedIn badge to be retrieved.
    """
    if request.method == 'GET':
        linkedin_badge = certification_controller.get_linkedin_badge_by_id(badge_id)
        return Response(linkedin_badge, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# get linkedin badges by certification
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all LinkedIn badges for a specific certification',
            description='Get all LinkedIn badges for a specific certification',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of LinkedIn badges')}

)
@api_view(['GET'])
def get_linkedin_badges_by_certification(request):
    """
    API endpoint that allows all LinkedIn badges for a specific certification to be retrieved.
    """
    if request.method == 'GET':
        certification_id = request.query_params.get('certification_id')
        linkedin_badges = certification_controller.get_linkedin_badges_by_certification(certification_id)
        return Response(linkedin_badges, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get linkedin badges by user
@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all LinkedIn badges for a specific user',
            description='Get all LinkedIn badges for a specific user',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of LinkedIn badges')}

)
@api_view(['GET'])
def get_linkedin_badges_by_user(request):
    """
    API endpoint that allows all LinkedIn badges for a specific user to be retrieved.
    """
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        linkedin_badges = certification_controller.get_linkedin_badges_by_user(user_id)
        return Response(linkedin_badges, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# create linkedin badge
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_image', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_url', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='share_on_linkedin', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='updated_at', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new LinkedIn badge',
            description='Create a new LinkedIn badge',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['POST'])
def create_linkedin_badge(request):
    """
    API endpoint that allows a new LinkedIn badge to be created.
    """
    if request.method == 'POST':
        linkedin_badge = certification_controller.create_linkedin_badge(request.data)
        return Response(linkedin_badge, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# update linkedin badge
@extend_schema(
    parameters=[
        OpenApiParameter(name='badge_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='certification', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_image', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_url', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='share_on_linkedin', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='updated_at', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a LinkedIn badge',
            description='Update a LinkedIn badge',
            value={
                'certification': 'certification',
                'badge_image': 'badge_image',
                'badge_url': 'badge_url',
                'share_on_linkedin': 'share_on_linkedin',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['PUT'])
def update_linkedin_badge(request, badge_id):
    """
    API endpoint that allows a LinkedIn badge to be updated.
    """
    if request.method == 'PUT':
        linkedin_badge = certification_controller.update_linkedin_badge(badge_id, request.data)
        return Response(linkedin_badge, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# delete linkedin badge
@extend_schema(
    parameters=[
        OpenApiParameter(name='badge_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a LinkedIn badge',
            description='Delete a LinkedIn badge',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['DELETE'])
def delete_linkedin_badge(request, badge_id):
    """
    API endpoint that allows a LinkedIn badge to be deleted.
    """
    if request.method == 'DELETE':
        linkedin_badge = certification_controller.delete_linkedin_badge(badge_id)
        return Response(linkedin_badge, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# post badge to linkedin
@extend_schema(
    parameters=[
        OpenApiParameter(name='certification_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Post a badge to LinkedIn',
            description='Post a badge to LinkedIn',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['POST'])
def post_badge_to_linkedin(request):
    """
    API endpoint that allows a badge to be posted to LinkedIn.
    """
    if request.method == 'POST':
        certification_id = request.query_params.get('certification_id')
        badge_id = request.query_params.get('badge_id')
        linkedin_badge = certification_controller.post_badge_to_linkedin(certification_id, badge_id)
        return Response(linkedin_badge, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# add badge to user linkedin achievements
@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='badge_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a badge to a user\'s LinkedIn achievements',
            description='Add a badge to a user\'s LinkedIn achievements',
            value={}
        )
    ],
    request=CertificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='LinkedIn badge data')}

)
@api_view(['POST'])
def add_badge_to_user_linkedin_achievements(request):
    """
    API endpoint that allows a badge to be added to a user's LinkedIn achievements section.
    """
    if request.method == 'POST':
        user_id = request.query_params.get('user_id')
        badge_id = request.query_params.get('badge_id')
        linkedin_badge = certification_controller.add_badge_to_user_linkedin_achievements(user_id, badge_id)
        return Response(linkedin_badge, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
