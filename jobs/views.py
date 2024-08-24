from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from jobs.models import JobListing, JobApplication, JobNotification, Interview
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer, InterviewSerializer
from jobs.controllers.jobs_controller import JobController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

job_controller = JobController()



@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all jobs',
            description='Get all jobs',
            value={}
        )
    ],
    request=JobListingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of jobs')}
)
@api_view(['GET'])
def get_jobs(request):
    """
    API endpoint that allows all jobs to be retrieved.
    """
    if request.method == 'GET':
        jobs = job_controller.get_all_jobs()
        return Response(jobs, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific job',
            description='Get a specific job',
            value={}
        )
    ],
    request=JobListingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Job data')}
)
@api_view(['GET'])
def get_specific_job(request, job_id):
    """
    API endpoint that allows a specific job to be retrieved.
    """
    if request.method == 'GET':
        job = job_controller.get_job_by_id(job_id)
        return Response(job, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='closing_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_active', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='salary', type=float, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='requirements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='responsibilities', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='employment_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='experience_level', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='program_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='program_duration', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='skills_required', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new job',
            description='Create a new job',
            value={
                'company': 'company',
                'title': 'title',
                'description': 'description',
                'attachments': 'attachments',
                'categories': 'categories',
                'location': 'location',
                'closing_date': 'closing_date',
                'is_active': 'is_active',
                'salary': 'salary',
                'requirements': 'requirements',
                'responsibilities': 'responsibilities',
                'employment_type': 'employment_type',
                'experience_level': 'experience_level',
                'program_type': 'program_type',
                'program_duration': 'program_duration',
                'skills_required': 'skills_required',
                'applications': 'applications',
                'notifications': 'notifications',
                'shares': 'shares',
                'tags': 'tags'
            }
        )
    ],
    request=JobListingSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Job data')}
)
@api_view(['POST'])
def create_job(request):
    """
    API endpoint that allows a new job to be created.
    """
    if request.method == 'POST':
        job = job_controller.create_job(request.data)
        return Response(job, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='closing_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_active', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='salary', type=float, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='requirements', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='responsibilities', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='employment_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='experience_level', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='program_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='program_duration', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='skills_required', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='notifications', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a job',
            description='Update a job',
            value={
                'company': 'company',
                'title': 'title',
                'description': 'description',
                'attachments': 'attachments',
                'categories': 'categories',
                'location': 'location',
                'closing_date': 'closing_date',
                'is_active': 'is_active',
                'salary': 'salary',
                'requirements': 'requirements',
                'responsibilities': 'responsibilities',
                'employment_type': 'employment_type',
                'experience_level': 'experience_level',
                'program_type': 'program_type',
                'program_duration': 'program_duration',
                'skills_required': 'skills_required',
                'applications': 'applications',
                'notifications': 'notifications',
                'shares': 'shares',
                'tags': 'tags'
            }
        )
    ],
    request=JobListingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Job data')}
)
@api_view(['PUT','GET'])
def update_job(request, job_id):
    """
    API endpoint that allows a job to be updated.
    """
    if request.method == 'PUT':
        job = job_controller.update_job(job_id, request.data)
        return Response(job, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        job = job_controller.get_job_by_id(job_id)
        return Response(job, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a job',
            description='Delete a job',
            value={}
        )
    ],
    request=JobListingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Job data')}
)
@api_view(['DELETE'])
def delete_job(request, job_id):
    """
    API endpoint that allows a job to be deleted.
    """
    if request.method == 'DELETE':
        job = job_controller.delete_job(job_id)
        return Response(job, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all applications for a specific job',
            description='Get all applications for a specific job',
            value={}
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of applications')}
)
@api_view(['GET'])
def get_job_applications(request, job_id):
    """
    API endpoint that allows all applications for a specific job to be retrieved.
    """
    if request.method == 'GET':
        applications = job_controller.get_job_applications(job_id)
        return Response(applications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='application_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific application',
            description='Get a specific application',
            value={}
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Application data')}
)
@api_view(['GET'])
def get_specific_application(request, application_id):
    """
    API endpoint that allows a specific application to be retrieved.
    """
    if request.method == 'GET':
        application = job_controller.get_job_application_by_id(application_id)
        return Response(application, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='applicant_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all applications for a specific applicant',
            description='Get all applications for a specific applicant',
            value={}
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of applications')}
)
@api_view(['GET'])
def get_applications_by_applicant(request, applicant_id):
    """
    API endpoint that allows all applications for a specific applicant to be retrieved.
    """
    if request.method == 'GET':
        applications = job_controller.get_job_application_by_applicant(applicant_id)
        return Response(applications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applicant', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='resume', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='cover_letter', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applied_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new application',
            description='Create a new application',
            value={
                'job_listing': 'job_listing',
                'applicant': 'applicant',
                'resume': 'resume',
                'attachments': 'attachments',
                'cover_letter': 'cover_letter',
                'applied_date': 'applied_date',
                'status': 'status',
                'shares': 'shares'
            }
        )
    ],
    request=JobApplicationSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Application data')}
)
@api_view(['POST'])
def create_application(request):
    """
    API endpoint that allows a new application to be created.
    """
    if request.method == 'POST':
        application = job_controller.create_job_application(request.data)
        return Response(application, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='application_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applicant', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='resume', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='cover_letter', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='applied_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an application',
            description='Update an application',
            value={
                'job_listing': 'job_listing',
                'applicant': 'applicant',
                'resume': 'resume',
                'attachments': 'attachments',
                'cover_letter': 'cover_letter',
                'applied_date': 'applied_date',
                'status': 'status',
                'shares': 'shares'
            }
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Application data')}
)
@api_view(['PUT','GET'])
def update_application(request, application_id):
    """
    API endpoint that allows an application to be updated.
    """
    if request.method == 'PUT':
        application = job_controller.update_job_application(application_id, request.data)
        return Response(application, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        application = job_controller.get_job_application_by_id(application_id)
        return Response(application, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='application_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an application',
            description='Delete an application',
            value={}
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Application data')}
)
@api_view(['DELETE'])
def delete_application(request, application_id):
    """
    API endpoint that allows an application to be deleted.
    """
    if request.method == 'DELETE':
        application = job_controller.delete_job_application(application_id)
        return Response(application, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all notifications for a specific job',
            description='Get all notifications for a specific job',
            value={}
        )
    ],
    request=JobNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of notifications')}
)
@api_view(['GET'])
def get_job_notifications(request, job_id):
    """
    API endpoint that allows all notifications for a specific job to be retrieved.
    """
    if request.method == 'GET':
        notifications = job_controller.get_job_notifications(job_id)
        return Response(notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific notification',
            description='Get a specific notification',
            value={}
        )
    ],
    request=JobNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['GET'])
def get_specific_notification(request, notification_id):
    """
    API endpoint that allows a specific notification to be retrieved.
    """
    if request.method == 'GET':
        notification = job_controller.get_job_notification_by_id(notification_id)
        return Response(notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all notifications for a specific user',
            description='Get all notifications for a specific user',
            value={}
        )
    ],
    request=JobNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of notifications')}
)
@api_view(['GET'])
def get_notifications_by_user(request, user_id):
    """
    API endpoint that allows all notifications for a specific user to be retrieved.
    """
    if request.method == 'GET':
        notifications = job_controller.get_job_notification_by_user(user_id)
        return Response(notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='read', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new notification',
            description='Create a new notification',
            value={
                'job_listing': 'job_listing',
                'user': 'user',
                'created_at': 'created_at',
                'read': 'read',
                'shares': 'shares'
            }
        )
    ],
    request=JobNotificationSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['POST'])
def create_notification(request):
    """
    API endpoint that allows a new notification to be created.
    """
    if request.method == 'POST':
        notification = job_controller.create_job_notification(request.data)
        return Response(notification, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a notification',
            description='Update a notification',
            value={}
        )
    ],
    request=JobNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['PUT','GET'])
def update_notification(request, notification_id):
    """
    API endpoint that allows a notification to be updated.
    """
    if request.method == 'PUT':
        notification = job_controller.update_job_notification(notification_id, request.data)
        return Response(notification, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        notification = job_controller.get_job_notification_by_id(notification_id)
        return Response(notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a notification',
            description='Delete a notification',
            value={}
        )
    ],
    request=JobNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['DELETE'])
def delete_notification(request, notification_id):
    """
    API endpoint that allows a notification to be deleted.
    """
    if request.method == 'DELETE':
        notification = job_controller.delete_job_notification(notification_id)
        return Response(notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all interviews for a specific job',
            description='Get all interviews for a specific job',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of interviews')}
)
@api_view(['GET'])
def get_interviews(request, job_id):
    """
    API endpoint that allows all interviews for a specific job to be retrieved.
    """
    if request.method == 'GET':
        interviews = job_controller.get_interviews_by_job(job_id)
        return Response(interviews, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='interview_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific interview',
            description='Get a specific interview',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Interview data')}
)
@api_view(['GET'])
def get_specific_interview(request, interview_id):
    """
    API endpoint that allows a specific interview to be retrieved.
    """
    if request.method == 'GET':
        interview = job_controller.get_interview_by_id(interview_id)
        return Response(interview, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='application', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_time', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interviewer', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new interview',
            description='Create a new interview',
            value={
                'job_listing': 'job_listing',
                'application': 'application',
                'interview_date': 'interview_date',
                'interview_time': 'interview_time',
                'interview_location': 'interview_location',
                'interviewer': 'interviewer',
                'interview_type': 'interview_type',
                'status': 'status',
                'shares': 'shares'
            }
        )
    ],
    request=InterviewSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Interview data')}
)
@api_view(['POST'])
def create_interview(request):
    """
    API endpoint that allows a new interview to be created.
    """
    if request.method == 'POST':
        interview = job_controller.create_interview(request.data)
        return Response(interview, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='interview_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='application', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_time', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interviewer', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='interview_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),

    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an interview',
            description='Update an interview',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Interview data')}
)
@api_view(['PUT','GET'])
def update_interview(request, interview_id):
    """
    API endpoint that allows an interview to be updated.
    """
    if request.method == 'PUT':
        interview = job_controller.update_interview(interview_id, request.data)
        return Response(interview, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        interview = job_controller.get_interview_by_id(interview_id)
        return Response(interview, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='interview_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an interview',
            description='Delete an interview',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Interview data')}
)
@api_view(['DELETE'])
def delete_interview(request, interview_id):
    """
    API endpoint that allows an interview to be deleted.
    """
    if request.method == 'DELETE':
        interview = job_controller.delete_interview(interview_id)
        return Response(interview, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all interviews',
            description='Delete all interviews',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of interviews')}
)
@api_view(['DELETE'])
def delete_all_interviews(request):
    """
    API endpoint that allows all interviews to be deleted.
    """
    if request.method == 'DELETE':
        interviews = job_controller.delete_all_interviews()
        return Response(interviews, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Generate a report for a specific job application',
            description='Generate a report for a specific job application',
            value={}
        )
    ],
    request=JobApplicationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Report data')}
)
@api_view(['GET'])
def generate_job_application_report(request, job_id):
    """
    API endpoint that allows a report to be generated for a specific job application.
    """
    if request.method == 'GET':
        report = job_controller.generate_job_application_report(job_id)
        return Response(report, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Generate a summary report for all jobs',
            description='Generate a summary report for all jobs',
            value={}
        )
    ],
    request=JobListingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Report data')}
)
@api_view(['GET'])
def generate_job_summary(request):
    """
    API endpoint that allows a summary report to be generated for all jobs.
    """
    if request.method == 'GET':
        report = job_controller.generate_job_summary()
        return Response(report, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='job_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all interviews for a specific job',
            description='Get all interviews for a specific job',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of interviews')}
)
@api_view(['GET'])
def get_interviews_by_job(request, job_id):
    """
    API endpoint that allows all interviews for a specific job to be retrieved.
    """
    if request.method == 'GET':
        interviews = job_controller.get_interviews_by_job(job_id)
        return Response(interviews, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='application_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all interviews for a specific job application',
            description='Get all interviews for a specific job application',
            value={}
        )
    ],
    request=InterviewSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of interviews')}
)
@api_view(['GET'])
def get_interviews_by_job_application(request, application_id):
    """
    API endpoint that allows all interviews for a specific job application to be retrieved.
    """
    if request.method == 'GET':
        interviews = job_controller.get_interviews_by_job_application(application_id)
        return Response(interviews, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

