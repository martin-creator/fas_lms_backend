from django.db.models import Count, Q
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer
from courses.utils import DateTimeUtils
from courses.helpers.course_helpers import CourseHelpers
from courses.querying.course_query import CourseQuery
from courses.settings.course_settings import CourseSettings
from courses.reports.course_report import CourseReport
from courses.services.course_services import CourseService


class CourseController:

    def __init__(self):
        self.course_service = CourseService()
        self.course_query = CourseQuery()
        self.course_settings = CourseSettings()
        self.course_report = CourseReport()
        self.course_helpers = CourseHelpers()


    def get_all_courses(self):
        """
        Get all courses.
        """
        return self.course_service.get_courses()
    

    def create_course(self, course_data):
        """
        Create a new course.
        """
        return self.course_service.create_course(course_data)
    
    def get_course_by_id(self, course_id):
        """
        Get a specific course.
        """
        return self.course_service.get_specific_course(course_id)
    
    def update_course(self, course_id, course_data):
        """
        Update an existing course.
        """
        return self.course_service.update_course(course_id, course_data)
    
    def delete_specific_course(self, course_id):
        """
        Delete a specific course.
        """
        return self.course_query.delete_course(course_id)
    
    def delete_all_courses(self):
        """
        Delete all courses.
        """
        return self.course_query.delete_all_courses()
    
    def enroll_course(self, course_id, user_id):
        """
        Enroll in a course.
        """
        return self.course_service.enroll_course(course_id, user_id)
    
    def track_course_progress(self, course_id, user_id):
        """
        Track course progress.
        """
        return self.course_service.get_course_progress(user_id, course_id)
    
    def complete_course(self, course_id, user_id):
        """
        Complete a course.
        """
        return self.course_service.complete_course(user_id, course_id)
    
    def add_lesson_to_course(self, course_id, lesson_data):
        """
        Add a lesson to a course.
        """
        return self.course_service.add_lesson_to_course(course_id, lesson_data)
    
    def get_lessons_by_course(self, course_id):
        """
        Get all lessons in a specific course.
        """
        return self.course_query.get_lessons_by_course(course_id)
    
    def get_course_lesson_by_order(self, course_id, lesson_order):
        """
        Get a specific lesson in a specific course.
        """
        return self.course_query.get_course_lessons_by_order(course_id, lesson_order)
    
    def update_lesson(self, course_id, lesson_id, lesson_data):
        """
        Update a lesson.
        """
        return self.course_service.update_lesson( course_id, lesson_id, lesson_data)
    
    def get_course_lesson_by_id(self, course_id, lesson_id):
        """
        Get a specific lesson in a specific course.
        """
        return self.course_query.get_course_lesson_by_id(course_id, lesson_id)
    
    def delete_all_course_lessons(self, course_id):
        """
        Delete all lessons in a specific course.
        """
        return self.course_service.delete_all_course_lesssons(course_id)
    
    def delete_specific_lesson(self, course_id, lesson_id):
        """
        Delete a specific lesson in a specific course.
        """
        return self.course_service.delete_specific_course_lesson(course_id, lesson_id)
    
    def register_lesson_progress(self, course_id, lesson_id, user_id):
        """
        Register course progress.
        """
        return self.course_service.register_lesson_progress(course_id, lesson_id, user_id,)
    
    def create_lesson_quiz(self, course_id, lesson_id, quiz_data):
        """
        Create a quiz for a lesson.
        """
        return self.course_service.add_quiz_to_lesson(course_id, lesson_id, quiz_data)
    
    def add_question_to_quiz(self, quiz_id, question_data):
        """
        Add a question to a quiz.
        """
        return self.course_service.add_question_to_quiz(quiz_id, question_data)
    
    def update_quiz_question(self, quiz_id, question_id, question_data):
        """
        Update a quiz question.
        """
        return self.course_service.update_quiz_question(quiz_id, question_id, question_data)
    
    def get_question_by_id(self, quiz_id, question_id):
        """
        Get a specific question.
        """
        return self.course_query.get_quiz_question_by_id(quiz_id, question_id)
    
    def get_all_questions_for_quiz(self, quiz_id):
        """
        Get all questions for a quiz.
        """
        return self.course_query.get_all_quiz_questions(quiz_id)
    
    def submit_lession_quiz(self, quiz_id, user_id, answers):
        """
        Submit a quiz.
        """
        return self.course_service.submit_lesson_quiz(quiz_id, user_id, answers)
    
    


    