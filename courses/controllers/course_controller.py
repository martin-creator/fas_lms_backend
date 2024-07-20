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
    


    

