from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, QuizSerializer, QuestionSerializer, ChoiceSerializer, LessonProgressSerializer, QuizProgressSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta
# from taggit

User = get_user_model()
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
        instructor_id = course_data.get('instructor')
        course_duration = course_data.get('duration')
        course_level = course_data.get('level')
        course_tag = course_data.get('tags')

        try:
            instructor = User.objects.get(id=instructor_id)
        except ObjectDoesNotExist:
            raise ValidationError("Instructor with the given ID does not exist.")
        
        course = Course(
                title=course_title,
                description=course_description,
                instructor=instructor,
                duration=timedelta(hours=int(course_duration)),
                level=course_level)

        return course, course_tag
    
    @staticmethod
    def process_course_update_data(course_id, course_data):
        """
        Process course data to update a course.
        """
        course_title = course_data.get('title')
        course_description = course_data.get('description')
        instructor_id = course_data.get('instructor')
        course_duration = course_data.get('duration')
        course_level = course_data.get('level')
        course_language = course_data.get('language')

        # try:
        #     instructor = 
        # except ObjectDoesNotExist:
        #     raise ValidationError("Instructor with the given ID does not exist.")

        course = Course.objects.get(id=course_id)
        # make sure that if if the course data does not provide a value for specific element, the existing value is retained
        # Update course attributes if provided in the data, otherwise retain the existing values
        if course_title is not None:
            course.title = course_title
        
        if course_description is not None:
            course.description = course_description
        
        if instructor_id is not None:
            try:
                instructor = User.objects.get(id=instructor_id)
                course.instructor = instructor
            except:
                raise ValidationError("Instructor with the given ID does not exist.")
        
        if course_duration is not None:
            course.duration = timedelta(hours=int(course_duration))
        
        if course_level is not None:
            course.level = course_level
        
        if course_language is not None:
            course.language = course_language
        
        return course

        # print(course)
      
        # return course
        
    # @staticmethod
    # def process_course_data(course_data):
    #     """
    #     Process course data to create or update a course.
    #     """
    #     course_id = course_data.get('id')
    #     course_title = course_data.get('title')
    #     course_description = course_data.get('description')
    #     course_instructor = course_data.get('instructor')
    #     course_duration = course_data.get('duration')
    #     course_level = course_data.get('level')
    #     course_image = course_data.get('image')
    #     course_video = course_data.get('video')
    #     course_certificate = course_data.get('certificate')

    #     if course_id:
    #         # Update existing course
    #         course = Course.objects.get(id=course_id)
    #         course.title = course_title
    #         course.description = course_description
    #         course.instructor = course_instructor
    #         course.duration = course_duration
    #         course.level = course_level
    #         course.image = course_image
    #         course.video = course_video
    #         course.certificate = course_certificate
    #     else:
    #         # Create new course
    #         course = Course(
    #             title=course_title,
    #             description=course_description,
    #             instructor=course_instructor,
    #             duration=course_duration,
    #             level=course_level,
    #         )

    #     return course
    

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
    

    # course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    # title = models.CharField(max_length=255)
    # description = models.TextField(default='', blank=True, null=True)
    # content = models.TextField(default='', blank=True, null=True)
    # video_url = models.URLField(blank=True, null=True)
    # attachments = GenericRelation('Attachment')
    # tags = TaggableManager()
    # order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def process_lesson_data(course_id, lesson_data):
        """
        Process lesson data to create a lesson.
        """
        course_id = lesson_data.get('course')
        title = lesson_data.get('title')
        description = lesson_data.get('description')
        content = lesson_data.get('content')
        video_url = lesson_data.get('video_url')
        order = lesson_data.get('order')
        tags = lesson_data.get('tags')

        lesson = Lesson(
                course_id=course_id,
                title=title,
                description=description,
                content=content,
                video_url=video_url,
                order=order
            )

        return lesson, tags
    

    def process_lesson_update_data(lesson_id, lesson_data):
        """
        Process lesson data to update a lesson.
        """
        title = lesson_data.get('title')
        description = lesson_data.get('description')
        content = lesson_data.get('content')
        video_url = lesson_data.get('video_url')
        order = lesson_data.get('order')
        tags = lesson_data.get('tags')

        lesson = Lesson.objects.get(id=lesson_id)

        if title is not None:
            lesson.title = title
        
        if description is not None:
            lesson.description = description
        
        if content is not None:
            lesson.content = content
        
        if video_url is not None:
            lesson.video_url = video_url
        
        if order is not None:
            lesson.order = order
        
        if tags is not None:
            lesson.tags = tags
        
        return lesson
    

    

