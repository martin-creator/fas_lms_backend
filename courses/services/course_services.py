from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer
from courses.utils import DateTimeUtils
from courses.helpers.course_helpers import CourseHelpers
from courses.querying.course_query import CourseQuery
from courses.settings.course_settings import CourseSettings
from courses.reports.course_report import CourseReport

# automatically save course progress and then return the updated course progress when a person logs in

class CourseService:
    # CourseService: Service class for courses.
    # Functions:
    # get_courses, get_course, create_course, update_course, delete_course, enroll_course, complete_course, get_lessons, get_lesson, get_quizzes, get_quiz, submit_quiz, get_questions, get_question, get_choices, get_choice, get_course_enrollments, get_course_completions, get_lesson_progresses, get_quiz_progresses, get_question_choices.


    @staticmethod
    def get_courses():
        """
        Get all courses.
        """
        return CourseQuery.get_all_courses()


    @staticmethod
    def create_course(course_data):
        """
        Create a new course.
        """
        course, course_tag = CourseHelpers.process_course_data(course_data)
        course.save()
        # Add tags to the course after it has been saved
        if course_tag:
            course.tags.add(course_tag)

        serializer = CourseSerializer(course)
        return serializer.data

    
    @staticmethod
    def get_specific_course(course_id):
        """
        Get a specific course.
        """
        return CourseQuery.get_course_by_id(course_id)
    
    
    @staticmethod
    def update_course(course_id, course_data):
        """
        Update an existing course.
        """
        course = CourseHelpers.process_course_update_data(course_id, course_data)
        course.save()
        serializer = CourseSerializer(course)
        return serializer.data
    
    
    


        


    
    # @staticmethod
    # def get_courses():
    #     """
    #     Get all courses.
    #     """
    #     courses = Course.objects.all()
    #     serializer = CourseSerializer(courses, many=True)
    #     return serializer.data
    
    # @staticmethod
    # def get_course(course_id):
    #     """
    #     Get a course by ID.
    #     """
    #     course = Course.objects.get(id=course_id)
    #     serializer = CourseSerializer(course)
    #     return serializer.data
    
    # @staticmethod
    # def create_course(course_data):
    #     """
    #     Create a new course.
    #     """
    #     course = CourseHelpers.process_course_data(course_data)
    #     course.save()
    #     serializer = CourseSerializer(course)
    #     return serializer.data
    
    # @staticmethod
    # def update_course(course_data):
    #     """
    #     Update an existing course.
    #     """
    #     course = CourseHelpers.process_course_data(course_data)
    #     course.save()
    #     serializer = CourseSerializer(course)
    #     return serializer.data
    
    # @staticmethod
    # def delete_course(course_id):
    #     """
    #     Delete a course by ID.
    #     """
    #     course = Course.objects.get(id=course_id)
    #     course.delete()
    #     return {'message': 'Course deleted successfully.'}
    
    # @staticmethod
    # def enroll_course(user, course_id):
    #     """
    #     Enroll a user in a course.
    #     """
    #     course = Course.objects.get(id=course_id)
    #     course_enrollment = CourseEnrollment(user=user, course=course)
    #     course_enrollment.save()
    #     serializer = CourseEnrollmentSerializer(course_enrollment)
    #     return serializer.data
    
    # @staticmethod
    # def complete_course(user, course_id):
    #     """
    #     Complete a course for a user.
    #     """
    #     course = Course.objects.get(id=course_id)
    #     course_completion = CourseCompletion(user=user, course=course)
    #     course_completion.save()
    #     serializer = CourseCompletionSerializer(course_completion)
    #     return serializer.data
    
    # @staticmethod
    # def get_lessons(course_id):
    #     """
    #     Get all lessons for a course.
    #     """
    #     lessons = Lesson.objects.filter(course_id=course_id)
    #     serializer = LessonSerializer(lessons, many=True)
    #     return serializer.data
    
    # @staticmethod
    # def get_lesson(lesson_id):
    #     """
    #     Get a lesson by ID.
    #     """
    #     lesson = Lesson.objects.get(id=lesson_id)
    #     serializer = LessonSerializer(lesson)
    #     return serializer.data
    
    # @staticmethod
    # def get_quizzes(lesson_id):
    #     """
    #     Get all quizzes for a lesson.
    #     """
    #     quizzes = Quiz.objects.filter(lesson_id=lesson_id)
    #     serializer = QuizSerializer(quizzes, many=True)
    #     return serializer.data
    
    # @staticmethod
    # def get_quiz(quiz_id):
    #     """
    #     Get a quiz by ID.
    #     """
    #     quiz = Quiz.objects.get(id=quiz_id)
    #     serializer = QuizSerializer(quiz)
    #     return serializer.data
    
    # @staticmethod
    # def submit_quiz(user, quiz_id, answers):
    #     """
    #     Submit a quiz for a user.
    #     """
    #     quiz = Quiz.objects.get(id=quiz_id)
    #     score = 0
    #     for answer in answers:
    #         question = Question.objects.get(id=answer['question'])
    #         choice = Choice.objects.get(id=answer['choice'])
    #         if choice.correct:
    #             score += 1
    #     quiz_progress = QuizProgress(user=user, quiz=quiz, score=score)
    #     quiz_progress.save()
    #     serializer = QuizProgressSerializer(quiz_progress)
    #     return serializer.data
    
    # @staticmethod
    # def get_questions(quiz_id):
    #     """
    #     Get all questions for a quiz.
    #     """
    #     questions = Question.objects.filter(quiz_id=quiz_id)
    #     serializer = QuestionSerializer(questions, many=True)
    #     return serializer.data
    
    # @staticmethod
    # def get_question(question_id):
    #     """
    #     Get a question by ID.
    #     """
    #     question = Question.objects.get(id=question_id)
    #     serializer = QuestionSerializer(question)
    #     return serializer.data
    
    # @staticmethod
    # def get_choices(question_id):
    #     """
    #     Get all choices for a question.
    #     """
    #     choices = Choice.objects.filter(question_id=question_id)
    #     serializer = ChoiceSerializer(choices, many=True)
    #     return serializer.data
    
    # @staticmethod
    # def get_choice(choice_id):
    #     """
    #     Get a choice by ID.
    #     """
    #     choice = Choice.objects.get(id=choice_id)
    #     serializer = ChoiceSerializer(choice)
    #     return serializer.data
    
    # @staticmethod

    
    

