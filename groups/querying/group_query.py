from django.db.models import Count, Q
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer


class GroupQuery:
    @staticmethod
    def get_all_groups():
        """
        Get all groups.
        """
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return serializer.data
    
    @staticmethod
    def get_group_by_id(group_id):
        """
        Get a group by its ID.
        """
        group = Group.objects.get(id=group_id)
        serializer = GroupSerializer(group)
        return serializer.data
    
    @staticmethod
    def get_group_by_id_without_serializer(group_id):
        """
        Get a group by its ID without using a serializer.
        """
        return Group.objects.get(id=group_id)
    
    @staticmethod
    def delete_group(group_id):
        """
        Delete a group by its ID.
        """
        group = Group.objects.get(id=group_id)
        group.delete()
        return True
    
    @staticmethod
    def delete_all_groups():
        """
        Delete all groups.
        """
        Group.objects.all().delete()
        return True
    
    @staticmethod
    def get_group_members(group_id):
        """
        Get all members in a specific group.
        """
        group = Group.objects.get(id=group_id)
        members = group.members.all()
        serializer = GroupMembershipSerializer(members, many=True)
        return serializer.data
    
    @staticmethod
    def get_group_member_by_id(group_id, member_id):
        """
        Get a member in a specific group by their ID.
        """
        group = Group.objects.get(id=group_id)
        member = group.members.get(id=member_id)
        serializer = GroupMembershipSerializer(member)
        return serializer.data
    
    @staticmethod
    def get_group_member_by_id_without_serializer(group_id, member_id):
        """
        Get a member in a specific group by their ID without using a serializer.
        """
        group = Group.objects.get(id=group_id)
        return group.members.get(id=member_id)
    
    @staticmethod
    def delete_all_group_members(group_id):
        """
        Delete all members in a specific group.
        """
        group = Group.objects.get(id=group_id)
        group.members.clear()
        return True
    
    @staticmethod
    def delete_group_member(group_id, member_id):
        """
        Delete a member in a specific group.
        """
        group = Group.objects.get(id=group_id)
        member = group.members.get(id=member_id)
        group.members.remove(member)
        return True
    
    @staticmethod
    def get_group_discussions(group_id):
        """
        Get all discussions in a specific group.
        """
        group = Group.objects.get(id=group_id)
        discussions = group.related_discussions.all()
        serializer = DiscussionSerializer(discussions, many=True)
        return serializer.data
    
    @staticmethod
    def get_group_discussion_by_id(group_id, discussion_id):
        """
        Get a discussion in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        discussion = group.related_discussions.get(id=discussion_id)
        serializer = DiscussionSerializer(discussion)
        return serializer.data
    
    @staticmethod
    def get_all_tasks_in_group(group_id):
        """
        Get all tasks in a specific group.
        """
        group = Group.objects.get(id=group_id)
        tasks = group.related_tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data
    

    @staticmethod
    def get_task_by_id_in_group(group_id, task_id):
        """
        Get a task in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        task = group.related_tasks.get(id=task_id)
        serializer = TaskSerializer(task)
        return serializer.data
    

    @staticmethod
    def get_all_projects_in_group(group_id):
        """
        Get all projects in a specific group.
        """
        group = Group.objects.get(id=group_id)
        projects = group.related_projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return serializer.data
    

    @staticmethod
    def get_project_by_id_in_group(group_id, project_id):
        """
        Get a project in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        project = group.related_projects.get(id=project_id)
        serializer = ProjectSerializer(project)
        return serializer.data
    

    @staticmethod
    def get_all_meetings_in_group(group_id):
        """
        Get all meetings in a specific group.
        """
        group = Group.objects.get(id=group_id)
        meetings = group.related_meetings.all()
        serializer = MeetingSerializer(meetings, many=True)
        return serializer.data
    

    @staticmethod
    def get_meeting_by_id_in_group(group_id, meeting_id):
        """
        Get a meeting in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        meeting = group.related_meetings.get(id=meeting_id)
        serializer = MeetingSerializer(meeting)
        return serializer.data
    

    @staticmethod
    def get_all_announcements_in_group(group_id):
        """
        Get all announcements in a specific group.
        """
        group = Group.objects.get(id=group_id)
        announcements = group.related_announcements.all()
        serializer = AnnouncementSerializer(announcements, many=True)
        return serializer.data
    

    @staticmethod
    def get_announcement_by_id_in_group(group_id, announcement_id):
        """
        Get an announcement in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        announcement = group.related_announcements.get(id=announcement_id)
        serializer = AnnouncementSerializer(announcement)
        return serializer.data
    

    @staticmethod
    def get_group_messages(group_id):
        """
        Get all messages in a specific group.
        """
        group = Group.objects.get(id=group_id)
        messages = Message.objects.filter(discussion__group=group)
        serializer = MessageSerializer(messages, many=True)
        return serializer.data
    
    
    @staticmethod
    def get_group_message_by_id(group_id, message_id):
        """
        Get a message in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        message = Message.objects.get(discussion__group=group, id=message_id)
        serializer = MessageSerializer(message)
        return serializer.data
    

    @staticmethod
    def get_milestones_in_group(group_id):
        """
        Get all milestones in a specific group.
        """
        group = Group.objects.get(id=group_id)
        milestones = Milestone.objects.filter(project__group=group)
        serializer = MilestoneSerializer(milestones, many=True)
        return serializer.data
    


    @staticmethod
    def get_milestone_by_id_in_group(group_id, milestone_id):
        """
        Get a milestone in a specific group by its ID.
        """
        group = Group.objects.get(id=group_id)
        milestone = Milestone.objects.get(project__group=group, id=milestone_id)
        serializer = MilestoneSerializer(milestone)
        return serializer.data
    

    


    






























# class CourseQuery:

#     @staticmethod
#     def get_all_courses():
#         """
#         Get all courses.
#         """
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return serializer.data
    

#     @staticmethod
#     def get_course_by_id(course_id):
#         """
#         Get a course by its ID.
#         """
#         course = Course.objects.get(id=course_id)
#         serializer = CourseSerializer(course)
#         return serializer.data
    
#     @staticmethod
#     def get_course_by_id_without_serializer(course_id):
#         """
#         Get a course by its ID without using a serializer.
#         """
#         return Course.objects.get(id=course_id)
    
#     @staticmethod
#     def delete_course(course_id):
#         """
#         Delete a course by its ID.
#         """
#         course = Course.objects.get(id=course_id)
#         course.delete()
#         return True
    
#     @staticmethod
#     def delete_all_courses():
#         """
#         Delete all courses.
#         """
#         Course.objects.all().delete()
#         return True
    
#     @staticmethod
#     def get_lessons_by_course(course_id):
#         """
#         Get all lessons in a specific course.
#         """
#         lessons = Lesson.objects.filter(course=course_id)
#         serializer = LessonSerializer(lessons, many=True)
#         return serializer.data
    
#     @staticmethod
#     def get_course_lesson_by_id(course_id, lesson_id):
#         """
#         Get a lesson in a specific course by its ID.
#         """
#         lesson = Lesson.objects.get(course=course_id, id=lesson_id)
#         serializer = LessonSerializer(lesson)
#         return serializer.data
    
#     @staticmethod
#     def get_course_lesson_by_id_without_serializer(course_id, lesson_id):
#         """
#         Get a lesson in a specific course by its ID without using a serializer.
#         """
#         return Lesson.objects.get(course=course_id, id=lesson_id)
    
#     @staticmethod
#     def get_course_lessons_by_order(course_id, lesson_order):
#         """
#         Get a specific lesson in a specific course.
#         """
#         lessons =  Lesson.objects.get(course=course_id, order=lesson_order)
#         serializer = LessonSerializer(lessons)
#         return serializer.data
    
#     @staticmethod
#     def delete_all_course_lessons(course_id):
#         """
#         Delete all lessons in a specific course.
#         """
#         Lesson.objects.filter(course=course_id).delete()
#         return True
    
#     @staticmethod
#     def delete_course_lesson(course_id, lesson_id):
#         """
#         Delete a lesson in a specific course.
#         """
#         Lesson.objects.get(course=course_id, id=lesson_id).delete()
#         return True
    
#     @staticmethod
#     def make_lesson_progress(lesson_id, user):
#         """
#         Make a lesson progress.
#         """
#         lesson = Lesson.objects.get(id=lesson_id)
#         lesson_progress = LessonProgress(lesson=lesson, user=user)
#         lesson_progress.save()
#         return True