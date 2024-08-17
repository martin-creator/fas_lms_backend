from django.db.models import Count, Q
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer
from groups.utils import DateTimeUtils, UserUtils
from groups.helpers.group_helpers import GroupHelpers
from groups.querying.group_query import GroupQuery
from groups.settings.group_settings import GroupSettings
from groups.reports.group_report import GroupReport
from groups.services.group_services import GroupService


class GroupController:
    
        def __init__(self):
            self.group_service = GroupService()
            self.group_query = GroupQuery()
            self.group_settings = GroupSettings()
            self.group_report = GroupReport()
            self.group_helpers = GroupHelpers()
    
        def get_all_groups(self):
            """
            Get all groups.
            """
            return self.group_service.get_groups()
        
        def create_group(self, group_data):
            """
            Create a new group.
            """
            return self.group_service.create_group(group_data)
        
        def get_group_by_id(self, group_id):
            """
            Get a specific group.
            """
            return self.group_service.get_specific_group(group_id)
        
        def update_group(self, group_id, group_data):
            """
            Update an existing group.
            """
            return self.group_service.update_group(group_id, group_data)
        
        def delete_specific_group(self, group_id):
            """
            Delete a specific group.
            """
            return self.group_query.delete_group(group_id)
        
        def delete_all_groups(self):
            """
            Delete all groups.
            """
            return self.group_query.delete_all_groups()
        
        def get_group_members(self, group_id):
            """
            Get all members in a specific group.
            """
            return self.group_query.get_group_members(group_id)
        
        def get_group_member_by_id(self, group_id, member_id):
            """
            Get a specific member in a specific group.
            """
            return self.group_query.get_group_member_by_id(group_id, member_id)
        
        def get_group_discussions(self, group_id):
            """
            Get all discussions in a specific group.
            """
            return self.group_query.get_group_discussions(group_id)
        
        def get_group_discussion_by_id(self, group_id, discussion_id):
            """
            Get a specific discussion in a specific group.
            """
            return self.group_query.get_group_discussion_by_id(group_id, discussion_id)
        
        def get_group_messages(self, group_id):
            """
            Get all messages in a specific group.
            """
            return self.group_query.C(group_id)
        
        def get_group_message_by_id(self, group_id, message_id):
            """
            Get a specific message in a specific group.
            """
            return self.group_query.get_group_message_by_id(group_id, message_id)
        
        def get_group_announcements(self, group_id):
            """
            Get all announcements in a specific group.
            """

# class CourseController:

#     def __init__(self):
#         self.course_service = CourseService()
#         self.course_query = CourseQuery()
#         self.course_settings = CourseSettings()
#         self.course_report = CourseReport()
#         self.course_helpers = CourseHelpers()


#     def get_all_courses(self):
#         """
#         Get all courses.
#         """
#         return self.course_service.get_courses()
    

#     def create_course(self, course_data):
#         """
#         Create a new course.
#         """
#         return self.course_service.create_course(course_data)
    
#     def get_course_by_id(self, course_id):
#         """
#         Get a specific course.
#         """
#         return self.course_service.get_specific_course(course_id)
    
#     def update_course(self, course_id, course_data):
#         """
#         Update an existing course.
#         """
#         return self.course_service.update_course(course_id, course_data)
    
#     def delete_specific_course(self, course_id):
#         """
#         Delete a specific course.
#         """
#         return self.course_query.delete_course(course_id)
    
#     def delete_all_courses(self):
#         """
#         Delete all courses.
#         """
#         return self.course_query.delete_all_courses()
    
#     def enroll_course(self, course_id, user_id):
#         """
#         Enroll in a course.
#         """
#         return self.course_service.enroll_course(course_id, user_id)
    
#     def track_course_progress(self, course_id, user_id):
#         """
#         Track course progress.
#         """
#         return self.course_service.get_course_progress(user_id, course_id)
    
#     def complete_course(self, course_id, user_id):
#         """
#         Complete a course.
#         """
#         return self.course_service.complete_course(user_id, course_id)
    
#     def add_lesson_to_course(self, course_id, lesson_data):
#         """
#         Add a lesson to a course.
#         """
#         return self.course_service.add_lesson_to_course(course_id, lesson_data)
    
#     def get_lessons_by_course(self, course_id):
#         """
#         Get all lessons in a specific course.
#         """
#         return self.course_query.get_lessons_by_course(course_id)
    
#     def get_course_lesson_by_order(self, course_id, lesson_order):
#         """
#         Get a specific lesson in a specific course.
#         """
#         return self.course_query.get_course_lessons_by_order(course_id, lesson_order)
    
#     def update_lesson(self, course_id, lesson_id, lesson_data):
#         """
#         Update a lesson.
#         """
#         return self.course_service.update_lesson( course_id, lesson_id, lesson_data)
    
#     def get_course_lesson_by_id(self, course_id, lesson_id):
#         """
#         Get a specific lesson in a specific course.
#         """
#         return self.course_query.get_course_lesson_by_id(course_id, lesson_id)
    
#     def delete_all_course_lessons(self, course_id):
#         """
#         Delete all lessons in a specific course.
#         """
#         return self.course_service.delete_all_course_lesssons(course_id)
    
#     def delete_specific_lesson(self, course_id, lesson_id):
#         """
#         Delete a specific lesson in a specific course.
#         """
#         return self.course_service.delete_specific_course_lesson(course_id, lesson_id)
    
#     def register_lesson_progress(self, course_id, lesson_id, user_id):
#         """
#         Register course progress.
#         """
#         return self.course_service.register_lesson_progress(course_id, lesson_id, user_id,)
    
#     def create_lesson_quiz(self, course_id, lesson_id, quiz_data):
#         """
#         Create a quiz for a lesson.
#         """
#         return self.course_service.add_quiz_to_lesson(course_id, lesson_id, quiz_data)
    
#     def add_question_to_quiz(self, quiz_id, question_data):
#         """
#         Add a question to a quiz.
#         """
#         return self.course_service.add_question_to_quiz(quiz_id, question_data)
    
#     def update_quiz_question(self, quiz_id, question_id, question_data):
#         """
#         Update a quiz question.
#         """
#         return self.course_service.update_quiz_question(quiz_id, question_id, question_data)
    
#     def get_question_by_id(self, quiz_id, question_id):
#         """
#         Get a specific question.
#         """
#         return self.course_query.get_quiz_question_by_id(quiz_id, question_id)
    
#     def get_all_questions_for_quiz(self, quiz_id):
#         """
#         Get all questions for a quiz.
#         """
#         return self.course_query.get_all_quiz_questions(quiz_id)
    
#     def submit_lession_quiz(self, quiz_id, user_id, answers):
#         """
#         Submit a quiz.
#         """
#         return self.course_service.submit_lesson_quiz(quiz_id, user_id, answers)
    
    


    
