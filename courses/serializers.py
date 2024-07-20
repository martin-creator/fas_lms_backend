# Create serializers for the Course model

from rest_framework import serializers
from .models import Course, CourseEnrollment, CourseCompletion, Lesson, Quiz, Choice, LessonProgress, QuizProgress, Question

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        # Ony the title, description, instructor, categories and tags are required to create a course
        # should return the id of the created course plus the other fields
        fields  = ['id', 'title', 'description', 'instructor', 'categories', 'tags']

    

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseEnrollment
        fields = '__all__'

class CourseCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCompletion
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = '__all__'

class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'

class QuizProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizProgress
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

