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
            return self.group_service.delete_group(group_id)
        

        def delete_all_groups(self):
            """
            Delete all groups.
            """
            return self.group_service.delete_all_groups()
        

        def get_group_members(self, group_id):
            """
            Get all members in a specific group.
            """
            return self.group_service.get_group_members(group_id)
        

        def get_group_discussions(self, group_id):
            """
            Get all discussions in a specific group.
            """
            return self.group_service.get_group_discussions(group_id)
        

        def get_group_messages(self, group_id):
            """
            Get all messages in a specific group.
            """
            return self.group_service.get_group_messages(group_id)
        

        def get_group_announcements(self, group_id):
            """
            Get all announcements in a specific group.
            """
            return self.group_service.get_group_announcements(group_id)
        

        def get_group_meetings(self, group_id):
            """
            Get all meetings in a specific group.
            """
            return self.group_service.get_group_meetings(group_id)
        

        def get_group_tasks(self, group_id):
            """
            Get all tasks in a specific group.
            """
            return self.group_service.get_group_tasks(group_id)
        

        def get_group_projects(self, group_id):
            """
            Get all projects in a specific group.
            """
            return self.group_service.get_group_projects(group_id)
        

        def get_group_milestones(self, group_id):
            """
            Get all milestones in a specific group.
            """
            return self.group_service.get_group_milestones(group_id)
        

        def create_meeting(self, group_id, meeting_data):
            """
            Create a meeting in a specific group.
            """
            return self.group_service.create_meeting(group_id, meeting_data)
        

        def get_meeting_by_id(self, group_id, meeting_id):
            """
            Get a specific meeting in a specific group.
            """
            return self.group_service.get_specific_meeting(group_id, meeting_id)
        

        def update_meeting(self, group_id, meeting_id, meeting_data):
            """
            Update a meeting in a specific group.
            """
            return self.group_service.update_meeting(group_id, meeting_id, meeting_data)
        

        def delete_meeting(self, group_id, meeting_id):
            """
            Delete a meeting in a specific group.
            """
            return self.group_service.delete_meeting(group_id, meeting_id)
        

        def create_task(self, group_id, task_data):
            """
            Create a task in a specific group.
            """
            return self.group_service.create_task(group_id, task_data)
        

        def get_task_by_id(self, group_id, task_id):
            """
            Get a specific task in a specific group.
            """
            return self.group_service.get_specific_task(group_id, task_id)
        

        def update_task(self, group_id, task_id, task_data):
            """
            Update a task in a specific group.
            """
            return self.group_service.update_task(group_id, task_id, task_data)
        

        def delete_task(self, group_id, task_id):
            """
            Delete a task in a specific group.
            """
            return self.group_service.delete_task(group_id, task_id)
        

        def create_project(self, group_id, project_data):
            """
            Create a project in a specific group.
            """
            return self.group_service.create_project(group_id, project_data)
        

        def get_project_by_id(self, group_id, project_id):
            """
            Get a specific project in a specific group.
            """
            return self.group_service.get_specific_project(group_id, project_id)
        

        def update_project(self, group_id, project_id, project_data):
            """
            Update a project in a specific group.
            """
            return self.group_service.update_project(group_id, project_id, project_data)
        

        def delete_project(self, group_id, project_id):
            """
            Delete a project in a specific group.
            """
            return self.group_service.delete_project(group_id, project_id)
        

        def create_milestone(self, group_id, project_id, milestone_data):
            """
            Create a milestone in a specific project.
            """
            return self.group_service.create_milestone(group_id, project_id, milestone_data)
        

        def get_milestone_by_id(self, group_id, project_id, milestone_id):
            """
            Get a specific milestone in a specific project.
            """
            return self.group_service.get_specific_milestone(group_id, project_id, milestone_id)
        

        def update_milestone(self, group_id, project_id, milestone_id, milestone_data):
            """
            Update a milestone in a specific project.
            """
            return self.group_service.update_milestone(group_id, project_id, milestone_id, milestone_data)
        

        def delete_milestone(self, group_id, project_id, milestone_id):
            """
            Delete a milestone in a specific project.
            """
            return self.group_service.delete_milestone(group_id, project_id, milestone_id)
        

        def create_discussion(self, group_id, discussion_data):
            """
            Create a discussion in a specific group.
            """
            return self.group_service.create_discussion(group_id, discussion_data)
        

        def get_discussion_by_id(self, group_id, discussion_id):
            """
            Get a specific discussion in a specific group.
            """
            return self.group_service.get_specific_discussion(group_id, discussion_id)
        

        def update_discussion(self, group_id, discussion_id, discussion_data):
            """
            Update a discussion in a specific group.
            """
            return self.group_service.update_discussion(group_id, discussion_id, discussion_data)
        

        def delete_discussion(self, group_id, discussion_id):
            """
            Delete a discussion in a specific group.
            """
            return self.group_service.delete_discussion(group_id, discussion_id)
        

        def create_message(self, group_id, discussion_id, message_data):
            """
            Create a message in a specific discussion.
            """
            return self.group_service.create_message(group_id, discussion_id, message_data)
        

        def get_message_by_id(self, group_id, discussion_id, message_id):
            """
            Get a specific message in a specific discussion.
            """
            return self.group_service.get_specific_message(group_id, discussion_id, message_id)
        

        def update_message(self, group_id, discussion_id, message_id, message_data):
            """
            Update a message in a specific discussion.
            """
            return self.group_service.update_message(group_id, discussion_id, message_id, message_data)
        

        def delete_message(self, group_id, discussion_id, message_id):
            """
            Delete a message in a specific discussion.
            """
            return self.group_service.delete_message(group_id, discussion_id, message_id)
        

        def create_announcement(self, group_id, announcement_data):
            """
            Create an announcement in a specific group.
            """
            return self.group_service.create_announcement(group_id, announcement_data)
        

        def get_announcement_by_id(self, group_id, announcement_id):
            """
            Get a specific announcement in a specific group.
            """
            return self.group_service.get_specific_announcement(group_id, announcement_id)
        

        def update_announcement(self, group_id, announcement_id, announcement_data):
            """
            Update an announcement in a specific group.
            """
            return self.group_service.update_announcement(group_id, announcement_id, announcement_data)
        

        def delete_announcement(self, group_id, announcement_id):
            """
            Delete an announcement in a specific group.
            """
            return self.group_service.delete_announcement(group_id, announcement_id)
        

        def add_member_to_group(self, group_id, user_id):
            """
            Add a member to a specific group.
            """
            return self.group_service.add_member_to_group(group_id, user_id)
        

        def remove_member_from_group(self, group_id, user_id):
            """
            Remove a member from a specific group.
            """
            return self.group_service.remove_member_from_group(group_id, user_id)
        

        def get_group_members_report(self, group):
            """
            Get a report for all members in a specific group.
            """
            return self.group_report.get_group_members_report(group)
        
        

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
    
    


    
