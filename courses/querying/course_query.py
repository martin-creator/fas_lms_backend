from django.db.models import Count, Q
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer


class CourseQuery:

    @staticmethod
    def get_all_courses():
        """
        Get all courses.
        """
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return serializer.data
    

    @staticmethod
    def get_course_by_id(course_id):
        """
        Get a course by its ID.
        """
        course = Course.objects.get(id=course_id)
        serializer = CourseSerializer(course)
        return serializer.data
    
    @staticmethod
    def get_course_by_id_without_serializer(course_id):
        """
        Get a course by its ID without using a serializer.
        """
        return Course.objects.get(id=course_id)
    
    @staticmethod
    def delete_course(course_id):
        """
        Delete a course by its ID.
        """
        course = Course.objects.get(id=course_id)
        course.delete()
        return True
    
    @staticmethod
    def delete_all_courses():
        """
        Delete all courses.
        """
        Course.objects.all().delete()
        return True
    


    

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
    
        

    @staticmethod
    def get_course_enrollment_by_id(enrollment_id):
        """
        Get a course enrollment by its ID.
        """
        return CourseEnrollment.objects.get(id=enrollment_id)
    
    @staticmethod
    def get_course_completion_by_id(completion_id):
        """
        Get a course completion by its ID.
        """
        return CourseCompletion.objects.get(id=completion_id)
        

    @staticmethod
    def get_lesson_by_id(lesson_id):
        """
        Get a lesson by its ID.
        """
      
        return Lesson.objects.get(id=lesson_id)
       
    @staticmethod
    def get_lesson_progress_by_id(progress_id):
        """
        Get a lesson progress by its ID.
        """
      
        return LessonProgress.objects.get(id=progress_id)
        

    @staticmethod
    def get_quiz_by_id(quiz_id):
        """
        Get a quiz by its ID.
        """
       
        return Quiz.objects.get(id=quiz_id)
       
    @staticmethod
    def get_quiz_progress_by_id(progress_id):
        """
        Get a quiz progress by its ID.
        """
        return QuizProgress.objects.get(id=progress_id)
        
    @staticmethod
    def get_question_by_id(question_id):
        """
        Get a question by its ID.
        """
        return Question.objects.get(id=question_id)

    @staticmethod
    def get_choice_by_id(choice_id):
        """
        Get a choice by its ID.
        """
        return Choice.objects.get(id=choice_id)
    
    
        
        
    
    