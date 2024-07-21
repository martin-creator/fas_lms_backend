from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer, CourseCreateSerializer
from courses.controllers.course_controller import CourseController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes





# Create your views here.
# Ony the title, description, instructor, categories and tags are required to create a course
# should return the id of the created course plus the other fields


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all courses',
            description='Get all courses',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
)
@api_view(['GET'])
def get_courses(request):
    """
    API endpoint that allows all courses to be retrieved.
    """
    if request.method == 'GET':
        course_controller = CourseController()
        courses = course_controller.get_all_courses()
        return Response(courses, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific course',
            description='Get a specific course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['GET'])
def get_specific_course(request, course_id):
    """
    API endpoint that allows a specific course to be retrieved.
    """
    if request.method == 'GET':
        course_controller = CourseController()
        course = course_controller.get_course_by_id(course_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@csrf_exempt
@extend_schema(
    parameters=[
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='instructor', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='duration', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='level', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new course',
            description='Create a new course',
            value={
                "title": "title",
                "description": "description",
                "instructor_id": 1,
                "categories": "categories",
                "tags": "tags"
            }
        )
    ],

    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}

)
@api_view(['POST'])
def create_course(request):
    """
    API endpoint that allows a course to be created.

    The following fields are required to create a course:
    - title
    - description
    - instructor_id
    - categories
    - tags
    - duration
    - level

    Examples of json data to be sent to the endpoint:
    {
        "title": "title",
        "description": "description",
        "instructor": 1,
        "categories": "categories",
        "tags": "tags",
        "duration": 10,
        "level": "Beginner"
    }

    Response:
    {
        "id": 1,
        "title": "title",
        "description": "description",
        "instructor_id": 1,
        "categories": "categories",
        "tags": "tags"
    }
    """
    if request.method == 'POST':
        course_data = request.data
        course_controller = CourseController()
        course = course_controller.create_course(course_data)
        return Response(course, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='instructor', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='duration', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='level', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing course',
            description='Update an existing course',
            value={
                "title": "title",
                "description": "description",
                "instructor": 1,
                "categories": "categories",
                "tags": "tags",
                "duration": 10,
                "level": "Beginner"
            }
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['PUT','GET'])
def update_course(request, course_id):
    """
    API endpoint that allows an existing course to be updated.

    The following fields can be updated:
    - title
    - description
    - instructor_id
    - categories
    - tags
    - duration
    - level

    Examples of json data to be sent to the endpoint:
    {
        "title": "title",
        "description": "description",
        "instructor": 1,
        "categories": "categories",
        "tags": "tags",
        "duration": 10,
        "level": "Beginner"
    }

    Response:
    {
        "id": 1,
        "title": "title",
        "description": "description",
        "instructor_id": 1,
        "categories": "categories",
        "tags": "tags"
    }
    """
    if request.method == 'PUT':
        course_data = request.data
        course_controller = CourseController()
        course = course_controller.update_course(course_id, course_data)
        return Response(course, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        course_controller = CourseController()
        course = course_controller.get_course_by_id(course_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific course',
            description='Delete a specific course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['DELETE'])
def delete_specific_course(request, course_id):
    """
    API endpoint that allows a specific course to be deleted.
    """
    if request.method == 'DELETE':
        course_controller = CourseController()
        course = course_controller.delete_specific_course(course_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all courses',
            description='Delete all courses',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['DELETE'])
def delete_all_courses(request):
    """
    API endpoint that allows all courses to be deleted.
    """
    if request.method == 'DELETE':
        course_controller = CourseController()
        course = course_controller.delete_all_courses()
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)