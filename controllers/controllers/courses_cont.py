from courses.models import Course, CourseEnrollment, CourseCompletion, LearningPath
from activity.models import Attachment


class CourseOperationsController:
    def __init__(self):
        pass

    def create_course(self, title, description, instructor, attachments=None, categories=None, tags=None):
        course = Course(
            title=title,
            description=description,
            instructor=instructor,
        )
        if attachments:
            for attachment in attachments:
                course.attachments.add(attachment)
        if categories:
            course.categories.set(categories)
        if tags:
            course.tags.add(*tags)
        course.save()
        return course

    def enroll_student_in_course(self, student, course):
        enrollment, created = CourseEnrollment.objects.get_or_create(student=student, course=course)
        return enrollment

    def complete_course(self, student, course, certificate_url=None, certificate=None, tags=None):
        completion = CourseCompletion(
            student=student,
            course=course,
            certificate_url=certificate_url,
            certificate=certificate,
        )
        if tags:
            completion.tags.add(*tags)
        completion.save()
        return completion

    def get_course_progress(self, student, course):
        try:
            enrollment = CourseEnrollment.objects.get(student=student, course=course)
            return enrollment
        except CourseEnrollment.DoesNotExist:
            return None

    def create_learning_path(self, name, description, courses=None, prerequisites=None):
        learning_path = LearningPath(
            name=name,
            description=description,
        )
        if courses:
            learning_path.courses.set(courses)
        if prerequisites:
            learning_path.prerequisites.set(prerequisites)
        learning_path.save()
        return learning_path
