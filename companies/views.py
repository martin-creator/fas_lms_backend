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

# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     website = models.URLField(blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     industry = models.CharField(max_length=255, blank=True)
#     description = models.TextField(blank=True)
#     attachments = GenericRelation(Attachment)
#     categories = models.ManyToManyField(Category, related_name='companies_categories')
#     logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
#     founded_date = models.DateField(null=True, blank=True)
#     employee_count = models.IntegerField(default=0)
#     revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member_companies')
#     followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_companies')
#     services = models.TextField(blank=True)  # New field for listing services provided by the company

#     def __str__(self):
#         return self.name
    
    
# class CompanyUpdate(models.Model):
#     company = models.ForeignKey(Company, related_name='company_updates', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     attachments = GenericRelation(Attachment)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.company.name} Update: {self.title}"


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



