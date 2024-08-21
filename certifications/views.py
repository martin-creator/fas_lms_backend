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

# class Certification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_certifications', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     attachments = GenericRelation(Attachment)
#     issuing_organization = models.CharField(max_length=255)
#     issue_date = models.DateField()
#     expiration_date = models.DateField(null=True, blank=True)
#     credential_id = models.CharField(max_length=255, blank=True)
#     credential_url = models.URLField(blank=True)
#     description = models.TextField(blank=True)
#     categories = models.ManyToManyField('activity.Category', related_name='certifications_categories')
#     certificate_image = models.ImageField(upload_to='certificates/', blank=True)
#     verification_status = models.BooleanField(default=False)
#     related_jobs = models.ManyToManyField('jobs.JobListing', related_name='job_certifications', blank=True)
#     related_courses = models.ManyToManyField('courses.Course', related_name='courses_certifications', blank=True)
#     related_events = models.ManyToManyField('events.Event', related_name='event_certifications', blank=True)
#     revoked = models.BooleanField(default=False, blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - {self.user.user.username}"
    
# class LinkedInBadge(models.Model):
#     certification = models.OneToOneField(Certification, related_name='linkedin_badge', on_delete=models.CASCADE)
#     badge_image = models.ImageField(upload_to='linkedin_badges/', blank=True)
#     badge_url = models.URLField(blank=True)
#     share_on_linkedin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"LinkedIn Badge for {self.certification.name}"
    
    



# @extend_schema(
#     parameters=[],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get all companies',
#             description='Get all companies',
#             value={
#                 'name': 'name',
#                 'website': 'website',
#                 'location': 'location',
#                 'industry': 'industry',
#                 'description': 'description',
#                 'attachments': 'attachments',
#                 'categories': 'categories',
#                 'logo': 'logo',
#                 'founded_date': 'founded_date',
#                 'employee_count': 'employee_count',
#                 'revenue': 'revenue',
#                 'members': 'members',
#                 'followers': 'followers',
#                 'services': 'services'
#             }

#         )
#     ],
#     request=CompanySerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of companies')}
# )
# @api_view(['GET'])
# def get_companies(request):
#     """
#     API endpoint that allows all companies to be retrieved.
#     """
#     if request.method == 'GET':
#         companies = company_controller.get_all_companies()
#         return Response(companies, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get a specific company',
#             description='Get a specific company',
#             value={
#                 'name': 'name',
#                 'website': 'website',
#                 'location': 'location',
#                 'industry': 'industry',
#                 'description': 'description',
#                 'attachments': 'attachments',
#                 'categories': 'categories',
#                 'logo': 'logo',
#                 'founded_date': 'founded_date',
#                 'employee_count': 'employee_count',
#                 'revenue': 'revenue',
#                 'members': 'members',
#                 'followers': 'followers',
#                 'services': 'services'
#             }
#         )
#     ],
#     request=CompanySerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}
# )
# @api_view(['GET'])
# def get_specific_company(request, company_id):
#     """
#     API endpoint that allows a specific company to be retrieved.
#     """
#     if request.method == 'GET':
#         company = company_controller.get_company_by_id(company_id)
#         return Response(company, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='website', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='industry', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='founded_date', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='employee_count', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='revenue', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='services', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='logo', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Create a new company',
#             description='Create a new company',
#             value={
#                 'name': 'name',
#                 'website': 'website',
#                 'location': 'location',
#                 'industry': 'industry',
#                 'description': 'description',
#                 'founded_date': 'founded_date',
#                 'employee_count': 'employee_count',
#                 'revenue': 'revenue',
#                 'services': 'services',
#                 'logo': 'logo',
#                 'categories': 'categories',
#                 'members': 'members',
#                 'followers': 'followers'
#             }
#         )
#     ],
#     request=CompanySerializer,
#     responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

# )
# @api_view(['POST'])
# def create_company(request):
#     """
#     API endpoint that allows a new company to be created.
#     """
#     if request.method == 'POST':
#         company = company_controller.create_company(request.data)
#         return Response(company, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='website', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='location', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='industry', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='founded_date', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='employee_count', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='revenue', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='services', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='logo', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='followers', type=str, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Update a company',
#             description='Update a company',
#             value={
#                 'name': 'name',
#                 'website': 'website',
#                 'location': 'location',
#                 'industry': 'industry',
#                 'description': 'description',
#                 'founded_date': 'founded_date',
#                 'employee_count': 'employee_count',
#                 'revenue': 'revenue',
#                 'services': 'services',
#                 'logo': 'logo',
#                 'categories': 'categories',
#                 'members': 'members',
#                 'followers': 'followers'
#             }
#         )
#     ],
#     request=CompanySerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

# )
# @api_view(['PUT','GET'])
# def update_company(request, company_id):
#     """
#     API endpoint that allows a company to be updated.
#     """
#     if request.method == 'PUT':
#         company = company_controller.update_company(company_id, request.data)
#         return Response(company, status=status.HTTP_200_OK)
#     elif request.method == 'GET':
#         company = company_controller.get_company_by_id(company_id)
#         return Response(company, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Delete a company',
#             description='Delete a company',
#             value={}
#         )
#     ],
#     request=CompanySerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

# )
# @api_view(['DELETE'])
# def delete_company(request, company_id):
#     """
#     API endpoint that allows a company to be deleted.
#     """
#     if request.method == 'DELETE':
#         company = company_controller.delete_company(company_id)
#         return Response(company, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Delete all companies',
#             description='Delete all companies',
#             value={}
#         )
#     ],
#     request=CompanySerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Company data')}

# )
# @api_view(['DELETE'])
# def delete_all_companies(request):
#     """
#     API endpoint that allows all companies to be deleted.
#     """
#     if request.method == 'DELETE':
#         companies = company_controller.delete_all_companies()
#         return Response(companies, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get all updates for a specific company',
#             description='Get all updates for a specific company',
#             value={
#                 'company': 'company',
#                 'title': 'title',
#                 'content': 'content',
#                 'attachments': 'attachments',
#                 'created_at': 'created_at'
#             }
#         )
#     ],
#     request=CompanyUpdateSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of updates')}
# )
# @api_view(['GET'])
# def get_company_updates(request, company_id):
#     """
#     API endpoint that allows all updates for a specific company to be retrieved.
#     """
#     if request.method == 'GET':
#         updates = company_controller.get_company_updates(company_id)
#         return Response(updates, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get a specific update for a company',
#             description='Get a specific update for a company',
#             value={
#                 'company': 'company',
#                 'title': 'title',
#                 'content': 'content',
#                 'attachments': 'attachments',
#                 'created_at': 'created_at'
#             }
#         )
#     ],
#     request=CompanyUpdateSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

# )
# @api_view(['GET'])
# def get_specific_company_update(request, company_id, update_id):
#     """
#     API endpoint that allows a specific update for a company to be retrieved.
#     """
#     if request.method == 'GET':
#         update = company_controller.get_company_update_by_id(update_id)
#         return Response(update, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Create a new update for a company',
#             description='Create a new update for a company',
#             value={
#                 'company': 'company',
#                 'title': 'title',
#                 'content': 'content',
#                 'attachments': 'attachments',
#                 'created_at': 'created_at'
#             }
#         )
#     ],
#     request=CompanyUpdateSerializer,
#     responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

# )
# @api_view(['POST'])
# def create_company_update(request, company_id):
#     """
#     API endpoint that allows a new update for a company to be created.
#     """
#     if request.method == 'POST':
#         update = company_controller.create_company_update(company_id, request.data)
#         return Response(update, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Update an update for a company',
#             description='Update an update for a company',
#             value={
#                 'company': 'company',
#                 'title': 'title',
#                 'content': 'content',
#                 'attachments': 'attachments',
#                 'created_at': 'created_at'
#             }
#         )
#     ],
#     request=CompanyUpdateSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

# )
# @api_view(['PUT'])
# def update_company_update(request, company_id, update_id):
#     """
#     API endpoint that allows an update for a company to be updated.
#     """
#     if request.method == 'PUT':
#         update = company_controller.update_company_update(company_id, update_id, request.data)
#         return Response(update, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='update_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Delete an update for a company',
#             description='Delete an update for a company',
#             value={}
#         )
#     ],
#     request=CompanyUpdateSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Update data')}

# )
# @api_view(['DELETE'])
# def delete_company_update(request, update_id):
#     """
#     API endpoint that allows an update for a company to be deleted.
#     """
#     if request.method == 'DELETE':
#         update = company_controller.delete_company_update(update_id)
#         return Response(update, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


 