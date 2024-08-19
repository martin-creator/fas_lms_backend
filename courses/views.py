# create api views for courses
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



course_controller = CourseController()

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
        course = course_controller.update_course(course_id, course_data)
        return Response(course, status=status.HTTP_200_OK)
    elif request.method == 'GET':
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
        course = course_controller.delete_all_courses()
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Enroll in a course',
            description='Enroll in a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def enroll_course(request, course_id, user_id):
    """
    API endpoint that allows a user to enroll in a course.
    """
    if request.method == 'POST':
        course = course_controller.enroll_course(course_id, user_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters = [
         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update course progress',
            description='Update course progress',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['GET'])
def update_course_progress(request, course_id, user_id):
    """
    API endpoint that allows a user to update course progress.
    """
    if request.method == 'GET':
        course = course_controller.track_course_progress(course_id, user_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Complete course',
            description='Complete course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def complete_course(request, course_id, user_id):
    """
    API endpoint that allows a user to complete a course.
    """
    if request.method == 'POST':
        course = course_controller.complete_course(course_id, user_id)
        return Response(course, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    # title = models.CharField(max_length=255)
    # description = models.TextField(default='', blank=True, null=True)
    # content = models.TextField(default='', blank=True, null=True)
    # video_url = models.URLField(blank=True, null=True)
    # attachments = GenericRelation('Attachment')
    # tags = TaggableManager()
    # order = models.PositiveIntegerField(default=0, blank=True, null=True)


@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='video_url', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='order', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a lesson to a course',
            description='Add a lesson to a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def add_lesson_to_course(request, course_id):
    """
    API endpoint that allows a lesson to be added to a course.
    """
    if request.method == 'POST':
        lesson_data = request.data
        lesson = course_controller.add_lesson_to_course(course_id, lesson_data)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all lessons in a course',
            description='Get all lessons in a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['GET'])
def get_lessons_by_course(request, course_id):
    """
    API endpoint that allows all lessons in a course to be retrieved.
    """
    if request.method == 'GET':
        lessons = course_controller.get_lessons_by_course(course_id)
        return Response(lessons, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_order', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific lesson in a course',
            description='Get a specific lesson in a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['GET'])
def get_specific_lesson_by_order(request, course_id, lesson_order):
    """
    API endpoint that allows a specific lesson in a course to be retrieved.
    """
    if request.method == 'GET':
        lesson = course_controller.get_course_lesson_by_order(course_id, lesson_order)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a lesson',
            description='Update a lesson',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['PUT','GET'])
def update_lesson(request, course_id, lesson_id):
    """
    API endpoint that allows a lesson to be updated.
    """
    if request.method == 'PUT':
        lesson_data = request.data
        lesson = course_controller.update_lesson(course_id, lesson_id, lesson_data)
        return Response(lesson, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        lesson = course_controller.get_course_lesson_by_id(course_id, lesson_id)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all lessons in a course',
            description='Delete all lessons in a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['DELETE'])
def delete_all_course_lessons(request, course_id):
    """
    API endpoint that allows all lessons in a course to be deleted.
    """
    if request.method == 'DELETE':
        lesson = course_controller.delete_all_course_lessons(course_id)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific lesson in a course',
            description='Delete a specific lesson in a course',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['DELETE'])
def delete_specific_lesson(request, course_id, lesson_id):
    """
    API endpoint that allows a specific lesson in a course to be deleted.
    """
    if request.method == 'DELETE':
        lesson = course_controller.delete_specific_lesson(course_id, lesson_id)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Register course progress',
            description='Register course progress',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def register_lesson_progress(request, course_id, lesson_id, user_id):
    """
    API endpoint that allows course progress to be registered.
    """
    if request.method == 'POST':
        lesson = course_controller.register_lesson_progress(course_id, lesson_id, user_id,)
        return Response(lesson, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='lesson_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='quiz_data', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a quiz for a lesson',
            description='Create a quiz for a lesson',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def create_lesson_quiz(request, course_id, lesson_id):
    """
    API endpoint that allows a quiz to be created for a lesson.
    """
    quiz_data = request.data  # Extract the quiz data from the request body
    
    if request.method == 'POST':
        quiz = course_controller.create_lesson_quiz(course_id, lesson_id, quiz_data)
        return Response(quiz, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='quiz_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='question_data', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a question to a quiz',
            description='Add a question to a quiz',
            value={
                "text": "question",
                "choices": ["choice1", "choice2", "choice3", "choice4"],
                "correct_choice": ["choice1"]
            }
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def add_question_to_quiz(request, quiz_id):
    """
    API endpoint that allows a question to be added to a quiz.
    """

    if request.method == 'POST':
        question_data = request.data
        question = course_controller.add_question_to_quiz(quiz_id, question_data)
        return Response(question, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='quiz_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='question_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a question in a quiz',
            description='Update a question in a quiz',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['PUT','GET'])
def update_question(request, quiz_id, question_id):
    """
    API endpoint that allows a question in a quiz to be updated.
    """
    if request.method == 'PUT':
        question_data = request.data
        question = course_controller.update_question(quiz_id, question_id, question_data)
        return Response(question, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        question = course_controller.get_question_by_id(quiz_id, question_id)
        return Response(question, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='quiz_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific quiz questions',
            description='Get a specific quiz questions',
            value={}
        )
    ],
)
@api_view(['GET'])
def get_all_questions_for_quiz(request, quiz_id):
    """
    API endpoint that allows all questions in a quiz to be retrieved.
    """
    if request.method == 'GET':
        questions = course_controller.get_all_questions_for_quiz(quiz_id)
        return Response(questions, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='quiz_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Submit a quiz',
            description='Submit a quiz',
            value={}
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
)
@api_view(['POST'])
def submit_lesson_quiz(request, quiz_id, user_id):
    """
    API endpoint that allows a quiz to be submitted.
    """
    if request.method == 'POST':
        answers = request.data
        quiz = course_controller.submit_lession_quiz(quiz_id, user_id, answers)
        return Response(quiz, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)