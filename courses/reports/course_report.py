from django.db.models import Count
from courses.models import Course, CourseEnrollment, CourseCompletion, Lesson, LessonProgress, Quiz, QuizProgress, Question, Choice
from courses.serializers import CourseSerializer, CourseEnrollmentSerializer, CourseCompletionSerializer, LessonSerializer, LessonProgressSerializer, QuizSerializer, QuizProgressSerializer, QuestionSerializer, ChoiceSerializer
from courses.querying.course_query import CourseQuery


class CourseReport:
    @staticmethod
    def get_course_report(course):
        """
        Get a report for a specific course.
        """
        course_data = CourseSerializer(course).data
        course_enrollments = CourseEnrollment.objects.filter(course=course)
        course_data['enrollments'] = CourseEnrollmentSerializer(course_enrollments, many=True).data
        course_completions = CourseCompletion.objects.filter(course=course)
        course_data['completions'] = CourseCompletionSerializer(course_completions, many=True).data
        lessons = Lesson.objects.filter(course=course)
        course_data['lessons'] = LessonSerializer(lessons, many=True).data
        quizzes = Quiz.objects.filter(course=course)
        course_data['quizzes'] = QuizSerializer(quizzes, many=True).data
        questions = Question.objects.filter(quiz__in=quizzes)
        course_data['questions'] = QuestionSerializer(questions, many=True).data
        choices = Choice.objects.filter(question__in=questions)
        course_data['choices'] = ChoiceSerializer(choices, many=True).data

        # return json data

        json_data = {
            'course': course_data,
            'enrollments': course_data['enrollments'],
            'completions': course_data['completions'],
            'lessons': course_data['lessons'],
            'quizzes': course_data['quizzes'],
            'questions': course_data['questions'],
            'choices': course_data['choices']
        }

        return json_data

    @staticmethod
    def get_student_report(student):
        """
        Get a report for a specific student.
        """
        student_data = {}
        student_data['courses'] = CourseQuery.get_courses_by_student(student).count()
        student_data['enrollments'] = CourseQuery.get_course_enrollments_by_student(student).count()
        student_data['completions'] = CourseQuery.get_course_completions_by_student(student).count()
        student_data['lessons'] = LessonProgress.objects.filter(student=student).count()
        student_data['quizzes'] = QuizProgress.objects.filter(student=student).count()

        return student_data
    

    @staticmethod
    def get_courses_monthly_report():
        """
        Get a monthly report for all courses.
        """
        courses = Course.objects.annotate(
            enrollments_count=Count('courseenrollment'),
            completions_count=Count('coursecompletion'),
            lessons_count=Count('lesson'),
            quizzes_count=Count('quiz')
        )
        courses_data = CourseSerializer(courses, many=True).data

        return courses_data
    

    @staticmethod
    def get_top_courses_and_students():
        """
        Get top courses and students based on course completions and quiz completions.
        """
        top_courses = Course.objects.annotate(
            completions_count=Count('coursecompletion'),
            quizzes_count=Count('quiz')
        ).order_by('-completions_count', '-quizzes_count')[:5]
        top_courses_data = CourseSerializer(top_courses, many=True).data

        top_students = CourseCompletion.objects.values('student').annotate(
            completions_count=Count('course')
        ).order_by('-completions_count')[:5]
        top_students_data = CourseEnrollmentSerializer(top_students, many=True).data

        return top_courses_data, top_students_data
    