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
        return self.course_report.get_course_progress(user_id, course_id)
    
    def complete_course(self, course_id, user_id):
        """
        Complete a course.
        """
        return self.course_report.complete_course(user_id, course_id)
    


    

