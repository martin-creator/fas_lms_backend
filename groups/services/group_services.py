from django.core.exceptions import ObjectDoesNotExist, ValidationError
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer
from groups.utils import DateTimeUtils, UserUtils
from groups.helpers.group_helpers import GroupHelpers
from groups.querying.group_query import GroupQuery
from groups.settings.group_settings import GroupSettings
from groups.reports.group_report import GroupReport
import logging



class GroupService:

    @staticmethod
    def get_groups():
        """
        Retrieve all groups.
        """
        return GroupQuery.get_all_groups()
    
    @staticmethod
    def create_group(group_data):
        """
        Create a new group with the given data.
        """
        group, group_tag = GroupHelpers.process_group_data(group_data)
        group.save()
        if group_tag:
            group.tags.add(group_tag)
        
        serializer = GroupSerializer(group)
        return serializer.data
    
    @staticmethod
    def get_group(group_id):
        """
        Retrieve a specific group by its ID.
        """
        return GroupQuery.get_group_by_id(group_id)
    

    @staticmethod
    def update_group(group_id, group_data):
        """
        Update an existing group with the given data.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        group, new_tag = GroupHelpers.process_group_update_data(group, group_data)
        group.save()
        
        if new_tag:
            group.tags.add(new_tag)
        
        serializer = GroupSerializer(group)
        return serializer.data
    

    @staticmethod
    def delete_group(group_id):
        """
        Delete a group by its ID.
        """
        return GroupQuery.delete_group(group_id)
    

    @staticmethod
    def add_member_to_group(group_id, member_data):
        """
        Add a new member to a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        member = GroupHelpers.process_group_membership_data(group_id, member_data)
        member.save()
        
        serializer = GroupMembershipSerializer(member)
        return serializer.data
    


    @staticmethod
    def remove_member_from_group(group_id, member_id):
        """
        Remove a member from a specific group.
        """
        return GroupQuery.delete_group_member(group_id, member_id)
    

    @staticmethod
    def delete_all_groups():
        """
        Delete all groups.
        """
        return GroupQuery.delete_all_groups()
    

    @staticmethod
    def get_group_members(group_id):
        """
        Retrieve all members of a specific group.
        """
        return GroupQuery.get_group_members(group_id)
    

    @staticmethod
    def get_group_member(group_id, member_id):
        """
        Retrieve a specific member of a group by their ID.
        """
        return GroupQuery.get_group_member_by_id(group_id, member_id)
    

    @staticmethod
    def get_group_discussions(group_id):
        """
        Retrieve all discussions in a specific group.
        """
        return GroupQuery.get_group_discussions(group_id)
    

    @staticmethod
    def get_group_messages(group_id):
        """
        Retrieve all messages in a specific group.
        """
        return GroupQuery.get_group_messages(group_id)
    

    @staticmethod
    def get_group_discussion(group_id, discussion_id):
        """
        Retrieve a specific discussion in a specific group.
        """
        return GroupQuery.get_group_discussion_by_id(group_id, discussion_id)
    

    @staticmethod
    def get_group_message(group_id, message_id):
        """
        Retrieve a specific message in a specific group.
        """
        return GroupQuery.get_group_message_by_id(group_id, message_id)
    

    @staticmethod
    def get_specific_discussion(group_id, discussion_id):
        """
        Retrieve a specific discussion in a specific group.
        """
        return GroupQuery.get_group_discussion_by_id(group_id, discussion_id)
    

    @staticmethod
    def create_discussion(group_id, discussion_data):
        """
        Create a new discussion in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        discussion, tags = GroupHelpers.process_discussion_data(group, discussion_data)
        discussion.save()
        
        if tags:
            discussion.tags.add(*tags)
        
        serializer = DiscussionSerializer(discussion)
        return serializer.data
    

    @staticmethod
    def update_discussion(group_id, discussion_id, discussion_data):
        """
        Update an existing discussion in a specific group.
        """
        discussion = GroupQuery.get_group_discussion_by_id_without_serializer(group_id, discussion_id)
        discussion, new_tags = GroupHelpers.process_discussion_update_data(discussion, discussion_data)
        discussion.save()
        
        if new_tags:
            discussion.tags.add(*new_tags)
        
        serializer = DiscussionSerializer(discussion)
        return serializer.data
    

    @staticmethod
    def delete_discussion(group_id, discussion_id):
        """
        Delete a specific discussion in a group.
        """
        return GroupQuery.delete_group_discussion(group_id, discussion_id)
    

    @staticmethod
    def delete_all_discussions(group_id):
        """
        Delete all discussions in a specific group.
        """
        return GroupQuery.delete_all_group_discussions(group_id)
    


    @staticmethod
    def get_specific_message(group_id, discussion_id, message_id):
        """
        Retrieve a specific message in a specific discussion in a specific group.
        """
        return GroupQuery.get_group_message_by_id(group_id, discussion_id, message_id)
    

    @staticmethod
    def create_message(group_id, message_data):
        """
        Create a new message in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        message = GroupHelpers.process_message_data(group, message_data)
        message.save()
        
        serializer = MessageSerializer(message)
        return serializer.data
    

    @staticmethod
    def update_message(group_id, message_id, message_data):
        """
        Update an existing message in a specific group.
        """
        message = GroupQuery.get_group_message_by_id_without_serializer(group_id, message_id)
        message = GroupHelpers.process_message_update_data(message, message_data)
        message.save()
        
        serializer = MessageSerializer(message)
        return serializer.data
    

    @staticmethod
    def delete_message(group_id, message_id):
        """
        Delete a specific message in a group.
        """
        return GroupQuery.delete_group_message(group_id, message_id)
    

    @staticmethod
    def delete_all_messages(group_id):
        """
        Delete all messages in a specific group.
        """
        return GroupQuery.delete_all_group_messages(group_id)
    

    @staticmethod
    def create_announcement(group_id, announcement_data):
        """
        Create a new announcement in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        announcement, tags = GroupHelpers.process_announcement_data(group, announcement_data)
        announcement.save()
        
        if tags:
            announcement.tags.add(*tags)
        
        serializer = AnnouncementSerializer(announcement)
        return serializer.data
    

    @staticmethod
    def update_announcement(group_id, announcement_id, announcement_data):
        """
        Update an existing announcement in a specific group.
        """
        announcement = GroupQuery.get_group_announcement_by_id_without_serializer(group_id, announcement_id)
        announcement, new_tags = GroupHelpers.process_announcement_update_data(announcement, announcement_data)
        announcement.save()
        
        if new_tags:
            announcement.tags.add(*new_tags)
        
        serializer = AnnouncementSerializer(announcement)
        return serializer.data
    

    @staticmethod
    def get_group_announcements(group_id):
        """
        Retrieve all announcements in a specific group.
        """
        return GroupQuery.get_all_announcements_in_group(group_id)
    

    @staticmethod
    def get_specific_announcement(group_id, announcement_id):
        """
        Retrieve a specific announcement in a specific group.
        """
        return GroupQuery.get_announcement_by_id_in_group(group_id, announcement_id)
    

    @staticmethod
    def delete_announcement(group_id, announcement_id):
        """
        Delete a specific announcement in a group.
        """
        return GroupQuery.delete_group_announcement(group_id, announcement_id)
    

    @staticmethod
    def delete_all_announcements(group_id):
        """
        Delete all announcements in a specific group.
        """
        return GroupQuery.delete_all_group_announcements(group_id)
    

    @staticmethod
    def get_group_meetings(group_id):
        """
        Retrieve all meetings in a specific group.
        """
        return GroupQuery.get_all_meetings_in_group(group_id)
    

    @staticmethod
    def get_specific_meeting(group_id, meeting_id):
        """
        Retrieve a specific meeting in a specific group.
        """
        return GroupQuery.get_meeting_by_id_in_group(group_id, meeting_id)
    

    @staticmethod
    def create_meeting(group_id, meeting_data):
        """
        Create a new meeting in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        meeting, tags = GroupHelpers.process_meeting_data(group, meeting_data)
        meeting.save()
        
        if tags:
            meeting.tags.add(*tags)
        
        serializer = MeetingSerializer(meeting)
        return serializer.data
    


    @staticmethod
    def update_meeting(group_id, meeting_id, meeting_data):
        """
        Update an existing meeting in a specific group.
        """
        meeting = GroupQuery.get_group_meeting_by_id_without_serializer(group_id, meeting_id)
        meeting, new_tags = GroupHelpers.process_meeting_update_data(meeting, meeting_data)
        meeting.save()
        
        if new_tags:
            meeting.tags.add(*new_tags)
        
        serializer = MeetingSerializer(meeting)
        return serializer.data
    


    @staticmethod
    def delete_meeting(group_id, meeting_id):
        """
        Delete a specific meeting in a group.
        """
        return GroupQuery.delete_group_meeting(group_id, meeting_id)
    


    @staticmethod
    def delete_all_meetings(group_id):
        """
        Delete all meetings in a specific group.
        """
        return GroupQuery.delete_all_group_meetings(group_id)
    

    @staticmethod
    def create_task(group_id, task_data):
        """
        Create a new task in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        task, tags = GroupHelpers.process_task_data(group, task_data)
        task.save()
        
        if tags:
            task.tags.add(*tags)
        
        serializer = TaskSerializer(task)
        return serializer.data
    

    @staticmethod
    def update_task(group_id, task_id, task_data):
        """
        Update an existing task in a specific group.
        """
        task = GroupQuery.get_group_task_by_id_without_serializer(group_id, task_id)
        task, new_tags = GroupHelpers.process_task_update_data(task, task_data)
        task.save()
        
        if new_tags:
            task.tags.add(*new_tags)
        
        serializer = TaskSerializer(task)
        return serializer.data
    

    
    @staticmethod
    def delete_task(group_id, task_id):
        """
        Delete a specific task in a group.
        """
        return GroupQuery.delete_group_task(group_id, task_id)
    

    @staticmethod
    def delete_all_tasks(group_id):
        """
        Delete all tasks in a specific group.
        """
        return GroupQuery.delete_all_group_tasks(group_id)
    

    @staticmethod
    def get_group_tasks(group_id):
        """
        Retrieve all tasks in a specific group.
        """
        return GroupQuery.get_all_tasks_in_group(group_id)
    

    @staticmethod
    def get_specific_task(group_id, task_id):
        """
        Retrieve a specific task in a specific group.
        """
        return GroupQuery.get_task_by_id_in_group(group_id, task_id)
    

    @staticmethod
    def get_group_projects(group_id):
        """
        Retrieve all projects in a specific group.
        """
        return GroupQuery.get_all_projects_in_group(group_id)
    

    @staticmethod
    def get_specific_project(group_id, project_id):
        """
        Retrieve a specific project in a specific group.
        """
        return GroupQuery.get_project_by_id_in_group(group_id, project_id)
    

    @staticmethod
    def create_project(group_id, project_data):
        """
        Create a new project in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        project, tags = GroupHelpers.process_project_data(group, project_data)
        project.save()
        
        if tags:
            project.tags.add(*tags)
        
        serializer = ProjectSerializer(project)
        return serializer.data
    

    @staticmethod
    def update_project(group_id, project_id, project_data):
        """
        Update an existing project in a specific group.
        """
        project = GroupQuery.get_group_project_by_id_without_serializer(group_id, project_id)
        project, new_tags = GroupHelpers.process_project_update_data(project, project_data)
        project.save()
        
        if new_tags:
            project.tags.add(*new_tags)
        
        serializer = ProjectSerializer(project)
        return serializer.data
    

    @staticmethod
    def delete_project(group_id, project_id):
        """
        Delete a specific project in a group.
        """
        return GroupQuery.delete_group_project(group_id, project_id)
    

    @staticmethod
    def delete_all_projects(group_id):
        """
        Delete all projects in a specific group.
        """
        return GroupQuery.delete_all_group_projects(group_id)
    

    @staticmethod
    def get_group_milestones(group_id):
        """
        Retrieve all milestones in a specific group.
        """
        return GroupQuery.get_milestones_in_group(group_id)
    

    @staticmethod
    def get_specific_milestone(group_id, project_id, milestone_id):
        """
        Retrieve a specific milestone in a specific project.
        """
        return GroupQuery.get_milestone_by_id_in_group(group_id, milestone_id, project_id)
    

    @staticmethod
    def create_milestone(project_id, milestone_data):
        """
        Create a new milestone in a specific project.
        """
        project = GroupQuery.get_group_project_by_id_without_serializer(project_id)
        milestone, tags = GroupHelpers.process_milestone_data(project, milestone_data)
        milestone.save()
        
        if tags:
            milestone.tags.add(*tags)
        
        serializer = MilestoneSerializer(milestone)
        return serializer.data
    

    @staticmethod
    def update_milestone(project_id, milestone_id, milestone_data):
        """
        Update an existing milestone in a specific project.
        """
        milestone = GroupQuery.get_project_milestone_by_id_without_serializer(project_id, milestone_id)
        milestone, new_tags = GroupHelpers.process_milestone_update_data(milestone, milestone_data)
        milestone.save()
        
        if new_tags:
            milestone.tags.add(*new_tags)
        
        serializer = MilestoneSerializer(milestone)
        return serializer.data
    


    @staticmethod
    def delete_milestone(project_id, milestone_id):
        """
        Delete a specific milestone in a project.
        """
        return GroupQuery.delete_project_milestone(project_id, milestone_id)
    

    @staticmethod
    def delete_all_milestones(project_id):
        """
        Delete all milestones in a specific project.
        """
        return GroupQuery.delete_all_project_milestones(project_id)
    

    @staticmethod
    def get_group_report(group_id):
        """
        Get a report for a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        group_data = GroupReport.get_group_report(group)
        return group_data
    

    @staticmethod
    def get_group_members_report(group_id):
        """
        Get a report for all members in a specific group.
        """
        group = GroupQuery.get_group_by_id_without_serializer(group_id)
        group_members_data = GroupReport.get_group_members_report(group)
        return group_members_data

    
    


    





# class CourseService:
#     """
#     Service class for managing courses, lessons, quizzes, and user progress.
#     """

#     def __init__(self):
#         self.notification = NotificationUtils()

#     @staticmethod
#     def get_courses():
#         """
#         Retrieve all courses.
#         """
#         return CourseQuery.get_all_courses()

#     @staticmethod
#     def create_course(course_data):
#         """
#         Create a new course with the given data.
#         """
#         course, course_tag = CourseHelpers.process_course_data(course_data)
#         course.save()
#         if course_tag:
#             course.tags.add(course_tag)
        
#         serializer = CourseSerializer(course)
#         return serializer.data

#     @staticmethod
#     def get_course(course_id):
#         """
#         Retrieve a specific course by its ID.
#         """
#         return CourseQuery.get_course_by_id(course_id)

#     @staticmethod
#     def update_course(course_id, course_data):
#         """
#         Update an existing course with the given data.
#         """
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         course, new_tag = CourseHelpers.process_course_update_data(course, course_data)
#         course.save()
        
#         if new_tag:
#             course.tags.add(new_tag)
        
#         serializer = CourseSerializer(course)
#         return serializer.data

#     @staticmethod
#     def delete_course(course_id):
#         """
#         Delete a course by its ID.
#         """
#         return CourseQuery.delete_course(course_id)

#     @staticmethod
#     def delete_all_courses():
#         """
#         Delete all courses.
#         """
#         return CourseQuery.delete_all_courses()

#     def enroll_course(self, course_id, user_id):
#         """
#         Enroll a user in a course and send a notification.
#         """
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         user = UserUtils.get_user_by_id(user_id)

#         if CourseQuery.get_course_enrollment(user, course):
#             raise ValidationError('User is already enrolled in this course.')

#         course_enrollment = CourseEnrollment(user=user, course=course)
#         course_enrollment.save()

#         # Handle notification
#         self.notification.handle_course_enrollment(user_id=user_id, course_id=course_id)

#         serializer = CourseEnrollmentSerializer(course_enrollment)
#         return serializer.data

#     def get_course_progress(self, user_id, course_id):
#         """
#         Calculate the progress of a user in a specific course.
#         """
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         user = UserUtils.get_user_by_id(user_id)
#         lessons = Lesson.objects.filter(course=course)
#         total_lessons = lessons.count()
#         completed_lessons = LessonProgress.objects.filter(user=user, lesson__in=lessons).count()
#         progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
#         return progress

#     def complete_course(self, course_id, user_id):
#         """
#         Mark a course as completed for a user and send a notification.
#         """
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         user = UserUtils.get_user_by_id(user_id)

#         if CourseQuery.get_course_completion(user, course):
#             raise ValidationError('Course already completed by the user.')

#         course_completion = CourseCompletion(user=user, course=course)
#         course_completion.save()

#         # Handle notification
#         self.notification.handle_course_completion(user_id=user_id, course_id=course_id)

#         serializer = CourseCompletionSerializer(course_completion)
#         return serializer.data

#     def add_lesson_to_course(self, course_id, lesson_data):
#         """
#         Add a new lesson to a specific course and send notifications.
#         """
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         lesson, tags = CourseHelpers.process_lesson_data(course_id, lesson_data)
#         lesson.save()
        
#         if tags:
#             lesson.tags.add(*tags)

#         # Notify all users enrolled in the course
#         enrollments = CourseEnrollment.objects.filter(course=course)
#         for enrollment in enrollments:
#             self.notification.send_notification(
#                 user=enrollment.user,
#                 notification_type_name='New Lesson Added',
#                 content=f'A new lesson has been added to the course: {course.title}.',
#                 url=f'/courses/{course_id}/lessons/{lesson.id}/'
#             )

#         serializer = LessonSerializer(lesson)
#         return serializer.data

#     def update_lesson(self, course_id, lesson_id, lesson_data):
#         """
#         Update an existing lesson in a specific course and notify users.
#         """
#         lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
#         lesson, new_tags = CourseHelpers.process_lesson_update_data(lesson, lesson_data)
#         lesson.save()
        
#         if new_tags:
#             lesson.tags.add(*new_tags)

#         # Notify users about the lesson update
#         course = CourseQuery.get_course_by_id_without_serializer(course_id)
#         enrollments = CourseEnrollment.objects.filter(course=course)
#         for enrollment in enrollments:
#             self.notification.send_notification(
#                 user=enrollment.user,
#                 notification_type_name='Lesson Updated',
#                 content=f'The lesson in course: {course.title} has been updated.',
#                 url=f'/courses/{course_id}/lessons/{lesson_id}/'
#             )

#         serializer = LessonSerializer(lesson)
#         return serializer.data

#     def get_lessons_by_course(self, course_id):
#         """
#         Retrieve all lessons for a specific course.
#         """
#         return CourseQuery.get_lessons_by_course(course_id)

#     def get_lesson_by_order(self, course_id, lesson_order):
#         """
#         Retrieve a specific lesson by its order in a course.
#         """
#         return CourseQuery.get_course_lessons_by_order(course_id, lesson_order)

#     def get_lesson(self, course_id, lesson_id):
#         """
#         Retrieve a specific lesson by its ID within a course.
#         """
#         return CourseQuery.get_course_lesson_by_id(course_id, lesson_id)

#     def delete_all_lessons(self, course_id):
#         """
#         Delete all lessons for a specific course.
#         """
#         return CourseQuery.delete_all_course_lessons(course_id)

#     def delete_lesson(self, course_id, lesson_id):
#         """
#         Delete a specific lesson in a course.
#         """
#         return CourseQuery.delete_course_lesson(course_id, lesson_id)

#     def register_lesson_progress(self, course_id, lesson_id, user_id):
#         """
#         Register progress for a lesson completed by a user and send a notification.
#         """
#         lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
#         user = UserUtils.get_user_by_id(user_id)
        
#         lesson_progress, created = LessonProgress.objects.get_or_create(lesson=lesson, user=user)
#         if not created:
#             lesson_progress.completed_at = DateTimeUtils.now()
#             lesson_progress.save()

#         # Handle notification
#         self.notification.send_notification(
#             user=user,
#             notification_type_name='Lesson Progress',
#             content=f'You have made progress in the lesson: {lesson.title}.',
#             url=f'/courses/{course_id}/lessons/{lesson_id}/'
#         )

#         serializer = LessonProgressSerializer(lesson_progress)
#         return serializer.data

#     def add_quiz_to_lesson(self, course_id, lesson_id, quiz_data):
#         """
#         Add a quiz to a specific lesson and notify users.
#         """
#         lesson = CourseQuery.get_course_lesson_by_id_without_serializer(course_id, lesson_id)
#         quiz = CourseHelpers.process_quiz_data(lesson, quiz_data)
#         quiz.save()

#         # Notify all users enrolled in the course
#         self.notification.notify_all_users(
#             notification_type_name='New Quiz Added',
#             content=f'A new quiz has been added to the lesson: {lesson.title}.',
#             url=f'/courses/{course_id}/lessons/{lesson_id}/quizzes/{quiz.id}/'
#         )

#         serializer = QuizSerializer(quiz)
#         return serializer.data

#     def add_question_to_quiz(self, quiz_id, question_data):
#         """
#         Add a question to a specific quiz and notify admins.
#         """
#         quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
#         question, choices, correct_choice = CourseHelpers.process_question_data(quiz, question_data)
        
#         question.save()
#         question.choices.set(choices)
#         question.correct_choice = correct_choice
#         question.save()

#         quiz.questions.add(question)
#         quiz.save()

#         # Notify admins about the new question
#         self.notification.notify_admins(
#             notification_type_name='Question Added/Updated',
#             content=f'A question has been added or updated in quiz: {quiz.title}.',
#             url=f'/quizzes/{quiz_id}/questions/{question.id}/'
#         )

#         serializer = QuestionSerializer(question)
#         return serializer.data

# def update_quiz_question(self, quiz_id, question_id, question_data):
#     """
#     Update a specific question in a quiz and notify admins.
#     """
#     quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
#     question = CourseQuery.get_quiz_question_by_id_without_serializer(quiz_id, question_id)
#     question, choices, correct_choice = CourseHelpers.process_question_update_data(question, question_data)
    
#     question.save()
#     question.choices.set(choices)
#     question.correct_choice = correct_choice
#     question.save()

#     # Notify admins about the question update
#     self.notification.notify_admins(
#         notification_type_name='Question Added/Updated',
#         content=f'A question has been added or updated in quiz: {quiz.title}.',
#         url=f'/quizzes/{quiz_id}/questions/{question.id}/'
#     )

#     serializer = QuestionSerializer(question)
#     return serializer.data

# def get_quiz_question(self, quiz_id, question_id):
#     """
#     Retrieve a specific question in a quiz.
#     """
#     return CourseQuery.get_quiz_question_by_id(quiz_id, question_id)

# def get_all_quiz_questions(self, quiz_id):
#     """
#     Retrieve all questions in a specific quiz.
#     """
#     return CourseQuery.get_all_quiz_questions(quiz_id)

# def submit_quiz(self, user_id, quiz_id, answers):
#     """
#     Submit quiz answers for a user and return the quiz progress.
#     """
#     quiz = CourseQuery.get_quiz_by_id_without_serializer(quiz_id)
#     user = UserUtils.get_user_by_id(user_id)
#     score = sum(
#         1 for answer in answers
#         if CourseQuery.get_quiz_question_by_id_without_serializer(quiz_id, answer['question']).correct_choice == 
#            CourseQuery.get_choice_by_id_without_serializer(answer['choice'])
#     )

#     quiz_progress = QuizProgress(user=user, quiz=quiz, score=score)
#     quiz_progress.save()

#     # Handle notification
#     self.notification.handle_quiz_submission(user_id=user_id, quiz_id=quiz_id, answers=answers)

#     serializer = QuizProgressSerializer(quiz_progress)
#     return serializer.data
    
    
    

    
    
    
    


        
