from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer
from courses.utils import DateTimeUtils, UserUtils, NotificationUtils
from courses.helpers.course_helpers import CourseHelpers
from courses.querying.course_query import CourseQuery
from courses.settings.course_settings import CourseSettings
from courses.reports.course_report import CourseReport
import logging
from django.http import request


logger = logging.getLogger(__name__)

# automatically save course progress and then return the updated course progress when a person logs in

class CourseService:
    """
    Service class for managing courses, lessons, quizzes, and user progress.
    """

    def __init__(self):
        self.notification = NotificationUtils()

    @staticmethod
    def get_courses():
        """
        Retrieve all courses.
        """
        return CourseQuery.get_all_courses()

    @staticmethod
    def create_course(course_data):
        """
        Create a new course with the given data.
        """
        course, course_tag = CourseHelpers.process_course_data(course_data)
        course.save()
        if course_tag:
            course.tags.add(course_tag)
        
        serializer = CourseSerializer(course)
        return serializer.data

    @staticmethod
    def get_course(course_id):
        """
        Retrieve a specific course by its ID.
        """
        return CourseQuery.get_course_by_id(course_id)

    @staticmethod
    def update_course(course_id, course_data):
        """
        Update an existing course with the given data.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        course, new_tag = CourseHelpers.process_course_update_data(course, course_data)
        course.save()
        
        if new_tag:
            course.tags.add(new_tag)
        
        serializer = CourseSerializer(course)
        return serializer.data

    @staticmethod
    def delete_course(course_id):
        """
        Delete a course by its ID.
        """
        return CourseQuery.delete_course(course_id)

    @staticmethod
    def delete_all_courses():
        """
        Delete all courses.
        """
        return CourseQuery.delete_all_courses()

    def enroll_course(self, course_id, user_id):
        """
        Enroll a user in a course and send a notification.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)

        if CourseQuery.get_course_enrollment(user, course):
            raise ValidationError('User is already enrolled in this course.')

        course_enrollment = CourseEnrollment(user=user, course=course)
        course_enrollment.save()

        # Send notification to user
        self.notification.send_notification(
            user=user,
            notification_type_name='Course Enrollment',
            content=f'You have been enrolled in the course: {course.title}',
            url=f'/courses/{course_id}/'
        )

        serializer = CourseEnrollmentSerializer(course_enrollment)
        return serializer.data

    def get_course_progress(self, user_id, course_id):
        """
        Calculate the progress of a user in a specific course.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)
        lessons = Lesson.objects.filter(course=course)
        total_lessons = lessons.count()
        completed_lessons = LessonProgress.objects.filter(user=user, lesson__in=lessons).count()
        progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        return progress

    def complete_course(self, course_id, user_id):
        """
        Mark a course as completed for a user and send a notification.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)

        if CourseQuery.get_course_completion(user, course):
            raise ValidationError('Course already completed by the user.')

        course_completion = CourseCompletion(user=user, course=course)
        course_completion.save()

        # Send notification to user
        self.notification.send_notification(
            user=user,
            notification_type_name='Course Completion',
            content=f'Congratulations! You have completed the course: {course.title}',
            url=f'/courses/{course_id}/'
        )

        serializer = CourseCompletionSerializer(course_completion)
        return serializer.data

    def add_lesson_to_course(self, course_id, lesson_data):
        """
        Add a new lesson to a specific course and send a notification.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        lesson, tags = CourseHelpers.process_lesson_data(course_id, lesson_data)
        lesson.save()
        
        if tags:
            lesson.tags.add(*tags)

        # Send notification to all users enrolled in the course
        enrollments = CourseEnrollment.objects.filter(course=course)
        for enrollment in enrollments:
            self.notification.send_notification(
                user=enrollment.user,
                notification_type_name='New Lesson Added',
                content=f'A new lesson has been added to the course: {course.title}',
                url=f'/courses/{course_id}/lessons/{lesson.id}/'
            )

        serializer = LessonSerializer(lesson)
        return serializer.data

    def update_lesson(self, course_id, lesson_id, lesson_data):
        """
        Update an existing lesson in a specific course and notify users.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        lesson, new_tags = CourseHelpers.process_lesson_update_data(lesson, lesson_data)
        lesson.save()
        
        if new_tags:
            lesson.tags.add(*new_tags)

        # Notify users about the lesson update
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        enrollments = CourseEnrollment.objects.filter(course=course)
        for enrollment in enrollments:
            self.notification.send_notification(
                user=enrollment.user,
                notification_type_name='Lesson Updated',
                content=f'The lesson in course: {course.title} has been updated.',
                url=f'/courses/{course_id}/lessons/{lesson_id}/'
            )

        serializer = LessonSerializer(lesson)
        return serializer.data

    def get_lessons_by_course(self, course_id):
        """
        Retrieve all lessons for a specific course.
        """
        return CourseQuery.get_lessons_by_course(course_id)

    def get_lesson_by_order(self, course_id, lesson_order):
        """
        Retrieve a specific lesson by its order in a course.
        """
        return CourseQuery.get_course_lessons_by_order(course_id, lesson_order)

    def get_lesson(self, course_id, lesson_id):
        """
        Retrieve a specific lesson by its ID within a course.
        """
        return CourseQuery.get_course_lesson_by_id(course_id, lesson_id)

    def delete_all_lessons(self, course_id):
        """
        Delete all lessons for a specific course.
        """
        return CourseQuery.delete_all_course_lessons(course_id)

    def delete_lesson(self, course_id, lesson_id):
        """
        Delete a specific lesson in a course.
        """
        return CourseQuery.delete_course_lesson(course_id, lesson_id)

    def register_lesson_progress(self, course_id, lesson_id, user_id):
        """
        Register progress for a lesson completed by a user and send a notification.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        user = UserUtils.get_user_by_id(user_id)
        
        lesson_progress, created = LessonProgress.objects.get_or_create(lesson=lesson, user=user)
        if not created:
            lesson_progress.completed_at = DateTimeUtils.now()
            lesson_progress.save()

        # Send notification to user
        self.notification.send_notification(
            user=user,
            notification_type_name='Lesson Progress',
            content=f'You have made progress in the lesson: {lesson.title}',
            url=f'/courses/{course_id}/lessons/{lesson_id}/'
        )

        serializer = LessonProgressSerializer(lesson_progress)
        return serializer.data

    def add_quiz_to_lesson(self, course_id, lesson_id, quiz_data):
        """
        Add a quiz to a specific lesson and notify users.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        quiz = CourseHelpers.process_quiz_data(lesson, quiz_data)
        quiz.save()

        # Notify users about the new quiz
        enrollments = CourseEnrollment.objects.filter(course=lesson.course)
        for enrollment in enrollments:
            self.notification.send_notification(
                user=enrollment.user,
                notification_type_name='New Quiz Added',
                content=f'A new quiz has been added to the lesson: {lesson.title}',
                url=f'/courses/{course_id}/lessons/{lesson_id}/quizzes/{quiz.id}/'
            )

        serializer = QuizSerializer(quiz)
        return serializer.data

    def add_question_to_quiz(self, quiz_id, question_data):
        """
        Add a question to a specific quiz and notify users.
        """
        quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
        question, choices, correct_choice = CourseHelpers.process_question_data(quiz, question_data)
        
        question.save()
        question.choices.set(choices)
        question.correct_choice = correct_choice
        question.save()

        quiz.questions.add(question)
        quiz.save()

        # Notify admins about the new question
        self.notification.notify_admins(
            notification_type_name='New Question Added',
            content=f'A new question has been added to quiz: {quiz.title}',
            url=f'/quizzes/{quiz_id}/questions/{question.id}/'
        )

        serializer = QuestionSerializer(question)
        return serializer.data

    def update_quiz_question(self, quiz_id, question_id, question_data):
        """
        Update a specific question in a quiz and notify admins.
        """
        quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
        question = CourseQuery.get_quiz_question_by_id_without_serializer(quiz_id, question_id)
        question, choices, correct_choice = CourseHelpers.process_question_update_data(question, question_data)
        
        question.save()
        question.choices.set(choices)
        question.correct_choice = correct_choice
        question.save()

        # Notify admins about the question update
        self.notification.notify_admins(
            notification_type_name='Question Updated',
            content=f'The question in quiz: {quiz.title} has been updated.',
            url=f'/quizzes/{quiz_id}/questions/{question_id}/'
        )

        serializer = QuestionSerializer(question)
        return serializer.data

    def get_quiz_question(self, quiz_id, question_id):
        """
        Retrieve a specific question in a quiz.
        """
        return CourseQuery.get_quiz_question_by_id(quiz_id, question_id)

    def get_all_quiz_questions(self, quiz_id):
        """
        Retrieve all questions in a specific quiz.
        """
        return CourseQuery.get_all_quiz_questions(quiz_id)

    def submit_quiz(self, user_id, quiz_id, answers):
        """
        Submit quiz answers for a user and return the quiz progress.
        """
        quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
        user = UserUtils.get_user_by_id(user_id)
        score = sum(
            1 for answer in answers
            if CourseQuery.get_quiz_question_by_id_without_serializer(quiz_id, answer['question']).correct_choice == 
               CourseQuery.get_choice_by_id_without_serializer(answer['choice'])
        )

        quiz_progress = QuizProgress(user=user, quiz=quiz, score=score)
        quiz_progress.save()

        # Send notification to user
        self.notification.send_notification(
            user=user,
            notification_type_name='Quiz Submitted',
            content=f'Your quiz results for: {quiz.title} are now available.',
            url=f'/quizzes/{quiz_id}/results/'
        )

        serializer = QuizProgressSerializer(quiz_progress)
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

    
    