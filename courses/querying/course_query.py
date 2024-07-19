from django.db.models import Count, Q
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer


class CourseQuery:
    @staticmethod
    def get_courses_by_instructor(instructor):
        """
        Get all courses taught by a specific instructor.
        """
        return Course.objects.filter(instructor=instructor)

    @staticmethod
    def get_courses_by_student(student):
        """
        Get all courses enrolled by a specific student.
        """
        return Course.objects.filter(courseenrollment__student=student)

    @staticmethod
    def get_course_enrollments_by_student(student):
        """
        Get all course enrollments by a specific student.
        """
        return CourseEnrollment.objects.filter(student=student)

    @staticmethod
    def get_course_completions_by_student(student):
        """
        Get all course completions by a specific student.
        """
        return CourseCompletion.objects.filter(student=student)

    @staticmethod
    def get_lessons_by_course(course):
        """
        Get all lessons in a specific course.
        """
        return Lesson.objects.filter(course=course)

    @staticmethod
    def get_lessons_by_student(student):
        """
        Get all lessons completed by a specific student.
        """
        return LessonProgress.objects.filter(student=student)

    @staticmethod
    def get_quizzes_by_course(course):
        """
        Get all quizzes in a specific course.
        """
        return Quiz.objects.filter(course=course)

    @staticmethod
    def get_quizzes_by_student(student):
        """
        Get all quizzes completed by a specific student.
        """
        return QuizProgress.objects.filter(student=student)

    @staticmethod
    def get_questions_by_quiz(quiz):
        """
        Get all questions in a specific quiz.
        """
        return Question.objects.filter(quiz=quiz)

    @staticmethod
    def get_choices_by_question(question):
        """
        Get all choices in a specific question.
        """
        return Choice.objects.filter(question=question)

    @staticmethod
    def get_courses_with_completions():
        """
        Get all courses with completions.
        """
        return Course.objects.annotate(completions_count=Count('coursecompletion')).filter(completions_count__gt=0)

    @staticmethod
    def get_courses_with_enrollments():
        """
        Get all courses with enrollments.
        """
        return Course.objects.annotate(enrollments_count=Count('courseenrollment')).filter(enrollments_count__gt=0)

    @staticmethod
    def get_courses_with_lessons():
        """
        Get all courses with lessons.
        """
        return Course
    
    @staticmethod
    def get_courses_with_quizzes():
        """
        Get all courses with quizzes.
        """
        return Course.objects.annotate(quizzes_count=Count('quiz')).filter(quizzes_count__gt=0)
    
    @staticmethod
    def get_courses_with_lessons_and_quizzes():
        """
        Get all courses with lessons and quizzes.
        """
        return Course.objects.annotate(lessons_count=Count('lesson'), quizzes_count=Count('quiz')).filter(Q(lessons_count__gt=0) | Q(quizzes_count__gt=0))
    
    @staticmethod
    def get_courses_with_lessons_and_quizzes_completed_by_student(student):
        """
        Get all courses with lessons and quizzes completed by a specific student.
        """
        return Course.objects.filter(Q(lesson__lessonprogress__student=student, quiz__quizprogress__student=student)).distinct()
    
    @staticmethod
    def get_courses_with_lessons_completed_by_student(student):
        """
        Get all courses with lessons completed by a specific student.
        """
        return Course.objects.filter(lesson__lessonprogress__student=student).distinct()
    
    @staticmethod
    def get_courses_with_quizzes_completed_by_student(student):
        """
        Get all courses with quizzes completed by a specific student.
        """
        return Course.objects.filter(quiz__quizprogress__student=student).distinct()
    
    @staticmethod
    def get_courses_with_lessons_and_quizzes_not_completed_by_student(student):
        """
        Get all courses with lessons and quizzes not completed by a specific student.
        """
        return Course.objects.exclude(Q(lesson__lessonprogress__student=student, quiz__quizprogress__student=student)).distinct()
    
    @staticmethod
    def get_courses_with_lessons_not_completed_by_student(student):
        """
        Get all courses with lessons not completed by a specific student.
        """
        return Course.objects.exclude(lesson__lessonprogress__student=student).distinct()
    
    @staticmethod
    def get_courses_with_quizzes_not_completed_by_student(student):
        """
        Get all courses with quizzes not completed by a specific student.
        """
        return Course.objects.exclude(quiz__quizprogress__student=student).distinct()
    
    