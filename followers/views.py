# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
# from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer CourseCreateSerializer
# from courses.controllers.course_controller import CourseController
# from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
# from drf_spectacular.types import OpenApiTypes






# api_view(['POST'])
# @extend_schema(
#     request=CourseSerializer,
#     responses={201: CourseSerializer}
# )

# def create_course(request):
#     """
#     Create a new course.
#     """
#     if request.method == 'POST':
#         course_data = request.data
#         course_controller = CourseController()
#         course = course_controller.create_course(course_data)
#         return Response(course, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# # Create your views here.
# # Ony the title, description, instructor, categories and tags are required to create a course
# # should return the id of the created course plus the other fields
