from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer
from courses.utils import DateTimeUtils, UserUtils
from courses.helpers.course_helpers import CourseHelpers
from courses.querying.course_query import CourseQuery
from courses.settings.course_settings import CourseSettings
from courses.reports.course_report import CourseReport
import logging
from django.http import request

logger = logging.getLogger(__name__)

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
    
    @staticmethod
    def delete_course(course_id):
        """
        Delete a course.
        """
        return CourseQuery.delete_course(course_id)
    
    @staticmethod
    def delete_all_courses():
        """
        Delete all courses.
        """
        return CourseQuery.delete_all_courses()
    
    @staticmethod
    def enroll_course(course_id, user_id):
        """
        Enroll a user in a course.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)

        # Check if the user is already enrolled in the course
        if CourseQuery.get_course_enrollment(user, course):
            raise ValidationError('You are already enrolled in this course.')
        
        course_enrollment = CourseEnrollment(user=user, course=course)
        course_enrollment.save()
        serializer = CourseEnrollmentSerializer(course_enrollment)
        return serializer.data
    
    @staticmethod
    def get_course_progress(user_id, course_id):
        """
        Update course progress for a user.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)
        lessons = Lesson.objects.filter(course=course)
        total_lessons = lessons.count()
        completed_lessons = LessonProgress.objects.filter(user=user, lesson__in=lessons).count()
        progress = (completed_lessons / total_lessons) * 100
        return progress
    
    
    
    @staticmethod
    def complete_course(course_id, user_id):
        """
        Complete a course for a user.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        user = UserUtils.get_user_by_id(user_id)

        # Check if the user has already completed the course
        if CourseQuery.get_course_completion(user, course):
            raise ValidationError('You have already completed this course.')
        
        course_completion = CourseCompletion(user=user, course=course)
        course_completion.save()
        serializer = CourseCompletionSerializer(course_completion)
        return serializer.data
    

    @staticmethod
    def add_lesson_to_course(course_id, lesson_data):
        """
        Add a lesson to a course.
        """
        course = CourseQuery.get_course_by_id_without_serializer(course_id)
        lesson, tags = CourseHelpers.process_lesson_data(course_id, lesson_data)
        lesson.save()

        # Add tags to the lesson after it has been saved
        if tags:
            for tag in tags:
             lesson.tags.add(tag)

        serializer = LessonSerializer(lesson)
        return serializer.data
    
    @staticmethod
    def update_lesson(course_id, lesson_id, lesson_data):
        """
        Update an existing lesson.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        lesson, new_tags = CourseHelpers.process_lesson_update_data(lesson, lesson_data)
        lesson.save()
        # save tags
        if new_tags:
            for tag in new_tags:
                lesson.tags.add(tag)
        serializer = LessonSerializer(lesson)
        return serializer.data
    
    
    @staticmethod
    def get_lessons_by_course(course_id):
        """
        Get all lessons for a course.
        """
        return CourseQuery.get_lessons_by_course(course_id)
    
    @staticmethod
    def get_course_lessons_by_order(course_id, lesson_order):
        """
        Get a specific lesson in a course.
        """
        return CourseQuery.get_course_lessons_by_order(course_id, lesson_order)
    
    @staticmethod
    def get_specific_lesson_by_id(course_id, lesson_id):
        """
        Get a specific lesson in a course.
        """
        return CourseQuery.get_course_lesson_by_id(course_id, lesson_id)
    
    @staticmethod
    def delete_all_course_lesssons(course_id):
        """
        Delete all lessons in a course.
        """
        return CourseQuery.delete_all_course_lessons(course_id)
    
    @staticmethod
    def delete_specific_course_lesson(course_id, lesson_id):
        """
        Delete a specific lesson in a course.
        """
        return CourseQuery.delete_course_lesson(course_id, lesson_id)
    
    
    # @staticmethod
    # def make_course_lesson_progress(lesson_id, student_id):

    # class LessonProgress(models.Model):
    # """
    # Represents the progress of a user through a lesson.

    # Attributes:
    #     user (ForeignKey): The user who is progressing through the lesson.
    #     lesson (ForeignKey): The lesson being tracked.
    #     completed_at (DateTimeField): The date and time when the lesson was completed.
    # """
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    # completed_at = models.DateTimeField(null=True, blank=True)

    # class Meta:
    #     unique_together = ('user', 'lesson')

    # def __str__(self):
    #     return f"{self.user.username} - {self.lesson.title}"

    @staticmethod
    def register_lesson_progress(course_id, lesson_id, user_id,):
        """
        Make a lesson progress.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        user = UserUtils.get_user_by_id(user_id)
        lesson_progress = LessonProgress(lesson=lesson, user=user)
        lesson_progress.save()
        serializer = LessonProgressSerializer(lesson_progress)
        return serializer.data
    

    # class Quiz(models.Model):
    # """
    # Represents a quiz associated with a lesson.

    # Attributes:
    #     lesson (ForeignKey): The lesson to which the quiz belongs.
    #     title (CharField): The title of the quiz.
    #     description (TextField): A detailed description of the quiz.
    #     questions (ManyToManyField): The questions that are part of the quiz.
    # """
    # lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    # title = models.CharField(max_length=255)
    # description = models.TextField(default='', blank=True, null=True)
    # questions = models.ManyToManyField('Question', related_name='quizzes')

    # def __str__(self):
    #     return f"Quiz for {self.lesson.title}"

    @staticmethod
    def add_quiz_to_lesson(course_id, lesson_id, quiz_data):
        """
        Add a quiz to a lesson.
        """
        lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
        quiz = CourseHelpers.process_quiz_data(lesson, quiz_data)
        quiz.save()
        serializer = QuizSerializer(quiz)
        return serializer.data
    


#     class Question(models.Model):
#     """
#     Represents a question in a quiz.

#     Attributes:
#         text (TextField): The text of the question.
#         choices (ManyToManyField): The possible choices for the question.
#         correct_choice (ForeignKey): The correct choice for the question.
#     """
#     text = models.TextField(default='', blank=True, null=True)
#     choices = models.ManyToManyField('Choice', related_name='questions')
#     correct_choice = models.ForeignKey('Choice', related_name='correct_for_questions', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.text

# class Choice(models.Model):
#     """
#     Represents a choice for a quiz question.

#     Attributes:
#         text (CharField): The text of the choice.
#     """
#     text = models.CharField(max_length=255)

#     def __str__(self):
#         return self.text
    
    # add  questions and choices to a quiz, you should also add the correct choice to the question

    @staticmethod
    def add_question_to_quiz(quiz_id, question_data):
        """
        Add a question to a quiz.
        """
        quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
        question, choices, correct_choice = CourseHelpers.process_question_data(quiz, question_data)
        
        # # Log details for debugging
        # logger.debug(f"Question: {question}")
        # logger.debug(f"Choices: {choices}")
        # logger.debug(f"Correct Choice: {correct_choice}")

        # Save the question first to get an ID
        question.save()

        print("Printing functions in add_question_to_quiz")
        print(question)
        print(choices)
        print(correct_choice)

        # Associate choices with the question
        # choice format = [<Choice: Protein synthesis>, <Choice: DNA replication>, <Choice: Lipid synthesis>, <Choice: Cell division>]
        question.choices.set(choices)
        question.correct_choice = correct_choice
        question.save()

        # Add the question to the quiz
        quiz.questions.add(question)
        quiz.save()
        
        # Serialize and return response data
        # serializer = QuestionSerializer(question)
        # return actual choice data instead of the choice id
        serializer = QuestionSerializer(question, context={'request': request})
        
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

    
    

