from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from companies.models import Company, CompanyUpdate
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from companies.controllers.companies_controller import CompanyController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

company_controller = CompanyController()

# class Follower(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_followers', on_delete=models.CASCADE)
#     follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_following', on_delete=models.CASCADE)
#     followed_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.follower.user.username} follows {self.user.user.username}"
    
#     @staticmethod
#     def is_follower(user, follower):
#         return Follower.objects.filter(user=user, follower=follower).exists()

#     @staticmethod
#     def get_followers(user):
#         return Follower.objects.filter(user=user)

# class FollowRequest(models.Model):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_requests_sent', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_requests_received', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     message = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.from_user.user.username} wants to follow {self.to_user.user.username}"

#     def accept(self):
#         self.status = 'accepted'
#         Follower.objects.create(user=self.to_user, follower=self.from_user)
#         self.save()

#     def reject(self):
#         self.status = 'rejected'
#         self.save()

# class FollowNotification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_notifications', on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.user.username}: {self.message}"


# class FollowerController:
        
#         def __init__(self):
#             self.follower_query = FollowerQuery()
#             self.follower_report = FollowerReport()
#             self.follower_service = FollowerService()
#             self.user_utils = UserUtils()
#             self.date_time_utils = DateTimeUtils()
    
    
#         def get_all_followers(self):
#             """
#             Get all followers.
#             """
#             return self.follower_service.get_followers()
    
    
#         def get_follower_by_id(self, follower_id):
#             """
#             Get a specific follower.
#             """
#             return self.follower_service.get_follower(follower_id)
    
    
#         def get_followers_by_user(self, user_id):
#             """
#             Get all followers of a specific user.
#             """
#             return self.follower_service.get_followers_by_user(user_id)
    
    
#         def get_followers_by_company(self, company_id):
#             """
#             Get all followers of a specific company.
#             """
#             return self.follower_service.get_followers_by_company(company_id)
    
    
#         def get_followers_by_user_and_company(self, user_id, company_id):
#             """
#             Get all followers of a specific user for a specific company.
#             """
#             return self.follower_service.get_followers_by_user_and_company(user_id, company_id)
        

#         # Follower Requests

#         def get_all_follow_requests(self):
#             """
#             Get all follow requests.
#             """
#             return self.follower_service.get_follow_requests()
        

#         def get_follow_request_by_id(self, request_id):
#             """
#             Get a specific follow request.
#             """
#             return self.follower_service.get_follow_request(request_id)
        

#         def get_follow_requests_by_user(self, user_id):
#             """
#             Get all follow requests for a user.
#             """
#             return self.follower_service.get_follow_requests_by_user(user_id)
        

#         def get_follow_requests_by_company(self, company_id):
#             """
#             Get all follow requests for a company.
#             """
#             return self.follower_service.get_follow_requests_by_company(company_id)
        
        

#         def get_follow_requests_by_user_and_company(self, user_id, company_id):
#             """
#             Get all follow requests for a user for a company.
#             """
#             return self.follower_service.get_follow_requests_by_user_and_company(user_id, company_id)
        

#         def create_follow_request(self, request_data):
#             """
#             Create a follow request.
#             """
#             return self.follower_service.create_follow_request(request_data)
        

        
        

#         def update_follow_request(self, request_id, request_data):
#             """
#             Update a follow request.
#             """
#             return self.follower_service.update_follow_request(request_id, request_data)
        

#         def delete_follow_request(self, request_id):
#             """
#             Delete a follow request.
#             """
#             return self.follower_service.delete_follow_request(request_id)
        

#         # Follow Notifications

#         def get_all_follow_notifications(self):
#             """
#             Get all follow notifications.
#             """
#             return self.follower_service.get_follow_notifications()
        

#         def get_follow_notification_by_id(self, notification_id):
#             """
#             Get a specific follow notification.
#             """
#             return self.follower_service.get_follow_notification(notification_id)
        

#         def create_follow_notification(self, notification_data):
#             """
#             Create a follow notification.
#             """
#             return self.follower_service.create_follow_notification(notification_data)
        

#         def update_follow_notification(self, notification_id, notification_data):
#             """
#             Update a follow notification.
#             """
#             return self.follower_service.update_follow_notification(notification_id, notification_data)
        

#         def delete_follow_notification(self, notification_id):
#             """
#             Delete a follow notification.
#             """
#             return self.follower_service.delete_follow_notification(notification_id)
        

#         def delete_all_follow_notifications(self):
#             """
#             Delete all follow notifications.
#             """
#             return self.follower_service.delete_all_follow_notifications()
        

#         def get_follow_notifications_by_user(self, user_id):
#             """
#             Get all follow notifications for a user.
#             """
#             return self.follower_service.get_follow_notifications_by_user(user_id)
        

#         def get_follow_notifications_by_company(self, company_id):
#             """
#             Get all follow notifications for a company.
#             """
#             return self.follower_service.get_follow_notifications_by_company(company_id)







@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all companies',
            description='Get all companies',
            value={
                'name': 'name',
                'website': 'website',
                'location': 'location',
                'industry': 'industry',
                'description': 'description',
                'attachments': 'attachments',
                'categories': 'categories',
                'logo': 'logo',
                'founded_date': 'founded_date',
                'employee_count': 'employee_count',
                'revenue': 'revenue',
                'members': 'members',
                'followers': 'followers',
                'services': 'services'
            }

        )
    ],
    request=CompanySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of companies')}
)
@api_view(['GET'])
def get_companies(request):
    """
    API endpoint that allows all companies to be retrieved.
    """
    if request.method == 'GET':
        companies = company_controller.get_all_companies()
        return Response(companies, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific company',
            description='Get a specific company',
            value={
                'name': 'name',
                'website': 'website',
                'location': 'location',
                'industry': 'industry',
                'description': 'description',
                'attachments': 'attachments',
                'categories': 'categories',
                'logo': 'logo',
                'founded_date': 'founded_date',
                'employee_count': 'employee_count',
                'revenue': 'revenue',
                'members': 'members',
                'followers': 'followers',
                'services': 'services'
            }
        )
    ],
    request=CompanySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}
)
@api_view(['GET'])
def get_specific_company(request, company_id):
    """
    API endpoint that allows a specific company to be retrieved.
    """
    if request.method == 'GET':
        company = company_controller.get_company_by_id(company_id)
        return Response(company, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='website', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='industry', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='founded_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='employee_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='revenue', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='services', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='logo', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new company',
            description='Create a new company',
            value={
                'name': 'name',
                'website': 'website',
                'location': 'location',
                'industry': 'industry',
                'description': 'description',
                'founded_date': 'founded_date',
                'employee_count': 'employee_count',
                'revenue': 'revenue',
                'services': 'services',
                'logo': 'logo',
                'categories': 'categories',
                'members': 'members',
                'followers': 'followers'
            }
        )
    ],
    request=CompanySerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

)
@api_view(['POST'])
def create_company(request):
    """
    API endpoint that allows a new company to be created.
    """
    if request.method == 'POST':
        company = company_controller.create_company(request.data)
        return Response(company, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='website', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='industry', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='founded_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='employee_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='revenue', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='services', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='logo', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a company',
            description='Update a company',
            value={
                'name': 'name',
                'website': 'website',
                'location': 'location',
                'industry': 'industry',
                'description': 'description',
                'founded_date': 'founded_date',
                'employee_count': 'employee_count',
                'revenue': 'revenue',
                'services': 'services',
                'logo': 'logo',
                'categories': 'categories',
                'members': 'members',
                'followers': 'followers'
            }
        )
    ],
    request=CompanySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

)
@api_view(['PUT','GET'])
def update_company(request, company_id):
    """
    API endpoint that allows a company to be updated.
    """
    if request.method == 'PUT':
        company = company_controller.update_company(company_id, request.data)
        return Response(company, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        company = company_controller.get_company_by_id(company_id)
        return Response(company, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a company',
            description='Delete a company',
            value={}
        )
    ],
    request=CompanySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

)
@api_view(['DELETE'])
def delete_company(request, company_id):
    """
    API endpoint that allows a company to be deleted.
    """
    if request.method == 'DELETE':
        company = company_controller.delete_company(company_id)
        return Response(company, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all companies',
            description='Delete all companies',
            value={}
        )
    ],
    request=CompanySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

)
@api_view(['DELETE'])
def delete_all_companies(request):
    """
    API endpoint that allows all companies to be deleted.
    """
    if request.method == 'DELETE':
        companies = company_controller.delete_all_companies()
        return Response(companies, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all updates for a specific company',
            description='Get all updates for a specific company',
            value={
                'company': 'company',
                'title': 'title',
                'content': 'content',
                'attachments': 'attachments',
                'created_at': 'created_at'
            }
        )
    ],
    request=CompanyUpdateSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of updates')}
)
@api_view(['GET'])
def get_company_updates(request, company_id):
    """
    API endpoint that allows all updates for a specific company to be retrieved.
    """
    if request.method == 'GET':
        updates = company_controller.get_company_updates(company_id)
        return Response(updates, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific update for a company',
            description='Get a specific update for a company',
            value={
                'company': 'company',
                'title': 'title',
                'content': 'content',
                'attachments': 'attachments',
                'created_at': 'created_at'
            }
        )
    ],
    request=CompanyUpdateSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

)
@api_view(['GET'])
def get_specific_company_update(request, company_id, update_id):
    """
    API endpoint that allows a specific update for a company to be retrieved.
    """
    if request.method == 'GET':
        update = company_controller.get_company_update_by_id(update_id)
        return Response(update, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new update for a company',
            description='Create a new update for a company',
            value={
                'company': 'company',
                'title': 'title',
                'content': 'content',
                'attachments': 'attachments',
                'created_at': 'created_at'
            }
        )
    ],
    request=CompanyUpdateSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

)
@api_view(['POST'])
def create_company_update(request, company_id):
    """
    API endpoint that allows a new update for a company to be created.
    """
    if request.method == 'POST':
        update = company_controller.create_company_update(company_id, request.data)
        return Response(update, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an update for a company',
            description='Update an update for a company',
            value={
                'company': 'company',
                'title': 'title',
                'content': 'content',
                'attachments': 'attachments',
                'created_at': 'created_at'
            }
        )
    ],
    request=CompanyUpdateSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

)
@api_view(['PUT'])
def update_company_update(request, company_id, update_id):
    """
    API endpoint that allows an update for a company to be updated.
    """
    if request.method == 'PUT':
        update = company_controller.update_company_update(company_id, update_id, request.data)
        return Response(update, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an update for a company',
            description='Delete an update for a company',
            value={}
        )
    ],
    request=CompanyUpdateSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

)
@api_view(['DELETE'])
def delete_company_update(request, update_id):
    """
    API endpoint that allows an update for a company to be deleted.
    """
    if request.method == 'DELETE':
        update = company_controller.delete_company_update(update_id)
        return Response(update, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


    


# @extend_schema(
#     parameters=[],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get all courses',
#             description='Get all courses',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
# )
# @api_view(['GET'])
# def get_courses(request):
#     """
#     API endpoint that allows all courses to be retrieved.
#     """
#     if request.method == 'GET':
#         courses = course_controller.get_all_courses()
#         return Response(courses, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get a specific course',
#             description='Get a specific course',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['GET'])
# def get_specific_course(request, course_id):
#     """
#     API endpoint that allows a specific course to be retrieved.
#     """
#     if request.method == 'GET':
#         course = course_controller.get_course_by_id(course_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @csrf_exempt
# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='instructor', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='duration', type=int, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='level', type=str, location=OpenApiParameter.QUERY, required=False),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Create a new course',
#             description='Create a new course',
#             value={
#                 "title": "title",
#                 "description": "description",
#                 "instructor_id": 1,
#                 "categories": "categories",
#                 "tags": "tags"
#             }
#         )
#     ],
#     request=CourseCreateSerializer,
#     responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}

# )



