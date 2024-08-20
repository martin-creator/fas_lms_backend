from django.db.models import Count
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer
from groups.querying.group_query import GroupQuery


class GroupReport:
    @staticmethod
    def get_group_report(group):
        """
        Get a report for a specific group.
        """
        group_data = GroupSerializer(group).data
        group_members = GroupMembership.objects.filter(group=group)
        group_data['members'] = GroupMembershipSerializer(group_members, many=True).data
        group_discussions = Discussion.objects.filter(group=group)
        group_data['discussions'] = DiscussionSerializer(group_discussions, many=True).data
        group_messages = Message.objects.filter(discussion__in=group_discussions)
        group_data['messages'] = MessageSerializer(group_messages, many=True).data
        group_announcements = Announcement.objects.filter(group=group)
        group_data['announcements'] = AnnouncementSerializer(group_announcements, many=True).data
        group_meetings = Meeting.objects.filter(group=group)
        group_data['meetings'] = MeetingSerializer(group_meetings, many=True).data
        group_tasks = Task.objects.filter(group=group)
        group_data['tasks'] = TaskSerializer(group_tasks, many=True).data
        group_projects = Project.objects.filter(group=group)
        group_data['projects'] = ProjectSerializer(group_projects, many=True).data
        group_milestones = Milestone.objects.filter(project__in=group_projects)
        group_data['milestones'] = MilestoneSerializer(group_milestones, many=True).data

        return group_data

    @staticmethod
    def get_group_members_report(group):
        """
        Get a report for all members in a specific group.
        """
        group_members = GroupMembership.objects.filter(group=group)
        group_members_data = GroupMembershipSerializer(group_members, many=True).data

        return group_members_data

    @staticmethod
    def get_group_discussions_report(group):
        """
        Get a report for all discussions in a specific group.
        """
        group_discussions = Discussion.objects.filter(group=group)
        group_discussions_data = DiscussionSerializer(group_discussions, many=True).data

        return group_discussions_data

    @staticmethod
    def get_group_messages_report(group):
        """
        Get a report for all messages in a specific group.
        """
        group_discussions = Discussion.objects.filter(group=group)
        group_messages = Message.objects.filter(discussion__in=group_discussions)
        group_messages_data = MessageSerializer(group_messages, many=True).data

        return group_messages_data

    @staticmethod
    def get_group_announcements_report(group):
        """
        Get a report for all announcements in a specific group.
        """
        group_announcements = Announcement.objects.filter(group=group)
        group_announcements_data = AnnouncementSerializer(group_announcements, many=True).data

        return group_announcements_data



# class CourseReport:
#     @staticmethod
#     def get_course_report(course):
#         """
#         Get a report for a specific course.
#         """
#         course_data = CourseSerializer(course).data
#         course_enrollments = CourseEnrollment.objects.filter(course=course)
#         course_data['enrollments'] = CourseEnrollmentSerializer(course_enrollments, many=True).data
#         course_completions = CourseCompletion.objects.filter(course=course)
#         course_data['completions'] = CourseCompletionSerializer(course_completions, many=True).data
#         lessons = Lesson.objects.filter(course=course)
#         course_data['lessons'] = LessonSerializer(lessons, many=True).data
#         quizzes = Quiz.objects.filter(course=course)
#         course_data['quizzes'] = QuizSerializer(quizzes, many=True).data
#         questions = Question.objects.filter(quiz__in=quizzes)
#         course_data['questions'] = QuestionSerializer(questions, many=True).data
#         choices = Choice.objects.filter(question__in=questions)
#         course_data['choices'] = ChoiceSerializer(choices, many=True).data

#         # return json data

#         json_data = {
#             'course': course_data,
#             'enrollments': course_data['enrollments'],
#             'completions': course_data['completions'],
#             'lessons': course_data['lessons'],
#             'quizzes': course_data['quizzes'],
#             'questions': course_data['questions'],
#             'choices': course_data['choices']
#         }

#         return json_data

#     @staticmethod
#     def get_student_report(student):
#         """
#         Get a report for a specific student.
#         """
#         student_data = {}
#         student_data['courses'] = CourseQuery.get_courses_by_student(student).count()
#         student_data['enrollments'] = CourseQuery.get_course_enrollments_by_student(student).count()
#         student_data['completions'] = CourseQuery.get_course_completions_by_student(student).count()
#         student_data['lessons'] = LessonProgress.objects.filter(student=student).count()
#         student_data['quizzes'] = QuizProgress.objects.filter(student=student).count()

#         return student_data
    

#     @staticmethod
#     def get_courses_monthly_report():
#         """
#         Get a monthly report for all courses.
#         """
#         courses = Course.objects.annotate(
#             enrollments_count=Count('courseenrollment'),
#             completions_count=Count('coursecompletion'),
#             lessons_count=Count('lesson'),
#             quizzes_count=Count('quiz')
#         )
#         courses_data = CourseSerializer(courses, many=True).data

#         return courses_data
    

#     @staticmethod
#     def get_top_courses_and_students():
#         """
#         Get top courses and students based on course completions and quiz completions.
#         """
#         top_courses = Course.objects.annotate(
#             completions_count=Count('coursecompletion'),
#             quizzes_count=Count('quiz')
#         ).order_by('-completions_count', '-quizzes_count')[:5]
#         top_courses_data = CourseSerializer(top_courses, many=True).data

#         top_students = CourseCompletion.objects.values('student').annotate(
#             completions_count=Count('course')
#         ).order_by('-completions_count')[:5]
#         top_students_data = CourseEnrollmentSerializer(top_students, many=True).data

#         return top_courses_data, top_students_data
    
