from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
# from django.contrib.auth.models import User
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta
# from taggit

User = get_user_model()

class GroupHelpers:
    """
    GroupHelpers: Utility functions specific to groups.
    Functions:
    process_group_data, process_group_update_data, validate_group_permissions, process_group_membership_data, process_group_membership_update_data, validate_group_membership_permissions.
    """

    @staticmethod
    def process_group_data(group_data):
        """
        Process group data to create a group.
        """
        group_name = group_data.get('name')
        group_description = group_data.get('description')
        group_type = group_data.get('group_type')
        privacy_level = group_data.get('privacy_level')
        cover_image = group_data.get('cover_image')
        tags = group_data.get('tags')

        group = Group(
                name=group_name,
                description=group_description,
                group_type=group_type,
                privacy_level=privacy_level,
                cover_image=cover_image
            )

        return group, tags
    
    @staticmethod
    def process_group_update_data(group_id, group_data):
        """
        Process group data to update a group.
        """
        group_name = group_data.get('name')
        group_description = group_data.get('description')
        group_type = group_data.get('group_type')
        privacy_level = group_data.get('privacy_level')
        cover_image = group_data.get('cover_image')
        tags = group_data.get('tags')

        group = Group.objects.get(id=group_id)

        if group_name is not None:
            group.name = group_name
        
        if group_description is not None:
            group.description = group_description
        
        if group_type is not None:
            group.group_type = group_type
        
        if privacy_level is not None:
            group.privacy_level = privacy_level
        
        if cover_image is not None:
            group.cover_image = cover_image
        
        if tags is not None:
            group.tags = tags
        
        return group

    @staticmethod
    def validate_group_permissions(user, group):
        """
        Validate group permissions for a user.
        """
        if user.is_superuser:
            return True
        elif user in group.members.all():
            return True
        else:
            raise ValidationError('You do not have permission to perform this action.')
    
    @staticmethod
    def process_group_membership_data(group_id, membership_data):
        """
        Process group membership data to create a group membership.
        """
        user_id = membership_data.get('user')
        role = membership_data.get('role')
        permissions = membership_data.get


        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        group = Group.objects.get(id=group_id)

        membership = GroupMembership(
                user=user,
                group=group,
                role=role
            )
        
        return membership
    
    @staticmethod
    def process_group_membership_update_data(group_id, membership_id, membership_data):
        """
        Process group membership data to update a group membership.
        """
        role = membership_data.get('role')
        permissions = membership_data.get('permissions')

        membership = GroupMembership.objects.get(id=membership_id)

        if role is not None:
            membership.role = role
        
        if permissions is not None:
            membership.permissions = permissions
        
        return membership
    
    

class ProjectHelpers:
    """
    ProjectHelpers: Utility functions specific to projects.
    Functions:
    process_project_data, process_project_update_data, validate_project_permissions.
    """

    @staticmethod
    def process_project_data(project_data):
        """
        Process project data to create a project.
        """
        project_name = project_data.get('name')
        project_description = project_data.get('description')
        start_date = project_data.get('start_date')
        end_date = project_data.get('end_date')
        created_by_id = project_data.get('created_by')
        members = project_data.get('members')

        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        project = Project(
                name=project_name,
                description=project_description,
                start_date=start_date,
                end_date=end_date,
                created_by=created_by
            )

        return project, members
    
    @staticmethod
    def process_project_update_data(project_id, project_data):
        """
        Process project data to update a project.
        """
        project_name = project_data.get('name')
        project_description = project_data.get('description')
        start_date = project_data.get('start_date')
        end_date = project_data.get('end_date')
        members = project_data.get('members')

        project = Project.objects.get(id=project_id)

        if project_name is not None:
            project.name = project_name
        
        if project_description is not None:
            project.description = project_description
        
        if start_date is not None:
            project.start_date = start_date
        
        if end_date is not None:
            project.end_date = end_date
        
        if members is not None:
            project.members.set(members)
        
        return project

    @staticmethod
    def validate_project_permissions(user, project):
        """
        Validate project permissions for a user.
        """
        if user.is_superuser:
            return True
        elif user in project.members.all():
            return True
        else:
            raise ValidationError('You do not have permission to perform this action.')

    
    @staticmethod
    def process_task_data(project_id, task_data):
        """
        Process task data to create a task.
        """
        project_id = task_data.get('project')
        title = task_data.get('title')
        description = task_data.get('description')
        due_date = task_data.get('due_date')
        status = task_data.get('status')
        assigned_to_id = task_data.get('assigned_to')
        created_by_id = task_data.get('created_by')

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        task = Task(
                project_id=project_id,
                title=title,
                description=description,
                due_date=due_date,
                status=status,
                assigned_to=assigned_to,
                created_by=created_by
            )

        return task
    

    @staticmethod
    def process_task_update_data(project_id, task_id, task_data):
        """
        Process task data to update a task.
        """
        title = task_data.get('title')
        description = task_data.get('description')
        due_date = task_data.get('due_date')
        status = task_data.get('status')
        assigned_to_id = task_data.get('assigned_to')

        task = Task.objects.get(id=task_id)

        if title is not None:
            task.title = title
        
        if description is not None:
            task.description = description
        
        if due_date is not None:
            task.due_date = due_date
        
        if status is not None:
            task.status = status
        
        if assigned_to_id is not None:
            try:
                assigned_to = User.objects.get(id=assigned_to_id)
                task.assigned_to = assigned_to
            except ObjectDoesNotExist:
                raise ValidationError("User with the given ID does not exist.")
        
        return task
    

    @staticmethod
    def process_milestone_data(project_id, milestone_data):
        """
        Process milestone data to create a milestone.
        """
        project_id = milestone_data.get('project')
        name = milestone_data.get('name')
        description = milestone_data.get('description')
        due_date = milestone_data.get('due_date')
        is_achieved = milestone_data.get('is_achieved')

        milestone = Milestone(
                project_id=project_id,
                name=name,
                description=description,
                due_date=due_date,
                is_achieved=is_achieved
            )

        return milestone
    

    @staticmethod
    def process_milestone_update_data(project_id, milestone_id, milestone_data):
        """
        Process milestone data to update a milestone.
        """
        name = milestone_data.get('name')
        description = milestone_data.get('description')
        due_date = milestone_data.get('due_date')
        is_achieved = milestone_data.get('is_achieved')

        milestone = Milestone.objects.get(id=milestone_id)

        if name is not None:
            milestone.name = name
        
        if description is not None:
            milestone.description = description
        
        if due_date is not None:
            milestone.due_date = due_date
        
        if is_achieved is not None:
            milestone.is_achieved = is_achieved
        
        return milestone
    
    
    @staticmethod
    def process_meeting_data(group_id, meeting_data):
        """
        Process meeting data to create a meeting.
        """
        group_id = meeting_data.get('group')
        name = meeting_data.get('name')
        description = meeting_data.get('description')
        meeting_date = meeting_data.get('meeting_date')
        created_by_id = meeting_data.get('created_by')
        participants = meeting_data.get('participants')

        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        meeting = Meeting(
                group_id=group_id,
                name=name,
                description=description,
                meeting_date=meeting_date,
                created_by=created_by
            )

        return meeting, participants
    

    @staticmethod
    def process_meeting_update_data(group_id, meeting_id, meeting_data):
        """
        Process meeting data to update a meeting.
        """
        name = meeting_data.get('name')
        description = meeting_data.get('description')
        meeting_date = meeting_data.get('meeting_date')
        participants = meeting_data.get('participants')

        meeting = Meeting.objects.get(id=meeting_id)

        if name is not None:
            meeting.name = name
        
        if description is not None:
            meeting.description = description
        
        if meeting_date is not None:
            meeting.meeting_date = meeting_date
        
        if participants is not None:
            meeting.participants.set(participants)
        
        return meeting
    

    @staticmethod
    def process_discussion_data(group_id, discussion_data):
        """
        Process discussion data to create a discussion.
        """
        group_id = discussion_data.get('group')
        topic = discussion_data.get('topic')
        description = discussion_data.get('description')
        created_by_id = discussion_data.get('created_by')
        messages = discussion_data.get('messages')

        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        discussion = Discussion(
                group_id=group_id,
                topic=topic,
                description=description,
                created_by=created_by
            )

        return discussion, messages
    

    @staticmethod
    def process_discussion_update_data(group_id, discussion_id, discussion_data):
        """
        Process discussion data to update a discussion.
        """
        topic = discussion_data.get('topic')
        description = discussion_data.get('description')
        messages = discussion_data.get('messages')

        discussion = Discussion.objects.get(id=discussion_id)

        if topic is not None:
            discussion.topic = topic
        
        if description is not None:
            discussion.description = description
        
        if messages is not None:
            discussion.messages.set(messages)
        
        return discussion
    

    @staticmethod
    def process_announcement_data(group_id, announcement_data):
        """
        Process announcement data to create an announcement.
        """
        group_id = announcement_data.get('group')
        title = announcement_data.get('title')
        content = announcement_data.get('content')
        created_by_id = announcement_data.get('created_by')

        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        announcement = Announcement(
                group_id=group_id,
                title=title,
                content=content,
                created_by=created_by
            )

        return announcement
    

    @staticmethod
    def process_announcement_update_data(group_id, announcement_id, announcement_data):
        """
        Process announcement data to update an announcement.
        """
        title = announcement_data.get('title')
        content = announcement_data.get('content')

        announcement = Announcement.objects.get(id=announcement_id)

        if title is not None:
            announcement.title = title
        
        if content is not None:
            announcement.content = content
        
        return announcement
    

    @staticmethod
    def process_message_data(discussion_id, message_data):
        """
        Process message data to create a message.
        """
        discussion_id = message_data.get('discussion')
        content = message_data.get('content')
        created_by_id = message_data.get('created_by')

        try:
            created_by = User.objects.get(id=created_by_id)
        except ObjectDoesNotExist:
            raise ValidationError("User with the given ID does not exist.")
        
        message = Message(
                discussion_id=discussion_id,
                content=content,
                created_by=created_by
            )

        return message
    

    @staticmethod
    def process_message_update_data(discussion_id, message_id, message_data):
        """
        Process message data to update a message.
        """
        content = message_data.get('content')

        message = Message.objects.get(id=message_id)

        if content is not None:
            message.content = content
        
        return message
    