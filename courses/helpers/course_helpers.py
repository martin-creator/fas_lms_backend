from django.core.exceptions import ValidationError
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer, LessonProgressSerializer, QuizProgressSerializer

class CourseHelpers:
# CourseHelpers: Utility functions specific to courses.
# Functions:
# process_course_data, validate_course_permissions.
    
    @staticmethod
    def process_course_data(course_data):
        """
        Process course data to create or update a course.
        """
        course_id = course_data.get('id')
        course_title = course_data.get('title')
        course_description = course_data.get('description')
        course_instructor = course_data.get('instructor')
        course_duration = course_data.get('duration')
        course_level = course_data.get('level')
        course_image = course_data.get('image')
        course_video = course_data.get('video')
        course_certificate = course_data.get('certificate')

        if course_id:
            # Update existing course
            course = Course.objects.get(id=course_id)
            course.title = course_title
            course.description = course_description
            course.instructor = course_instructor
            course.duration = course_duration
            course.level = course_level
            course.image = course_image
            course.video = course_video
            course.certificate = course_certificate
        else:
            # Create new course
            course = Course(
                title=course_title,
                description=course_description,
                instructor=course_instructor,
                duration=course_duration,
                level=course_level,
                image=course_image,
                video=course_video,
                certificate=course_certificate
            )

        return course
    

    @staticmethod
    def validate_course_permissions(user, course):
        """
        Validate course permissions for a user.
        """
        if user.is_superuser or course.instructor == user:
            return True
        else:
            raise ValidationError('You do not have permission to perform this action.')
        
    
    @staticmethod
    def process_course_enrollment_data(enrollment_data):
        """
        Process course enrollment data to create or update a course enrollment.
        """
        enrollment_id = enrollment_data.get('id')
        course_id = enrollment_data.get('course')
        student_id = enrollment_data.get('student')
        completed_at = enrollment_data.get('completed_at')
        certificate_url = enrollment_data.get('certificate_url')
        certificate = enrollment_data.get('certificate')

        if enrollment_id:
            # Update existing course enrollment
            enrollment = CourseEnrollment.objects.get(id=enrollment_id)
            enrollment.course_id = course_id
            enrollment.student_id = student_id
            enrollment.completed_at = completed_at
            enrollment.certificate_url = certificate_url
            enrollment.certificate = certificate
        else:
            # Create new course enrollment
            enrollment = CourseEnrollment(
                course_id=course_id,
                student_id=student_id,
                completed_at=completed_at,
                certificate_url=certificate_url,
                certificate=certificate
            )

        return enrollment
    