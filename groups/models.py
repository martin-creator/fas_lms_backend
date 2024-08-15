from django.db import models
from django.conf import settings
from activity.models import Reaction, Share, Category
from taggit.managers import TaggableManager
from django.utils import timezone

class Group(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category, related_name='group_categories')
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='GroupMembership', 
        related_name='user_groups', 
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    group_type = models.CharField(
        max_length=20, 
        choices=[('public', 'Public'), ('private', 'Private')], 
        default='public'
    )
    privacy_level = models.CharField(
        max_length=20, 
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], 
        default='medium'
    )
    tags = TaggableManager()
    cover_image = models.ImageField(upload_to='group_covers/', blank=True, null=True)
    shares = models.ManyToManyField(Share, related_name='group_shares', blank=True, db_index=True)

    # Advanced project management and collaboration features
    projects = models.ManyToManyField('Project', related_name='group_projects', blank=True)
    meetings = models.ManyToManyField('Meeting', related_name='group_meetings', blank=True)
    discussions = models.ManyToManyField('Discussion', related_name='group_discussions', blank=True)
    announcements = models.ManyToManyField('Announcement', related_name='group_announcements', blank=True)

    def __str__(self):
        return self.name

    def total_members(self):
        return self.members.count()

    def active_projects(self):
        return self.projects.filter(status='active').count()

    def completed_projects(self):
        return self.projects.filter(status='completed').count()

class GroupMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20, 
        choices=[('admin', 'Admin'), ('member', 'Member'), ('project_manager', 'Project Manager')], 
        default='member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    permissions = models.JSONField(blank=True, null=True)  # Custom permissions for roles

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_projects'
    )
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_members')
    tasks = models.ManyToManyField('Task', related_name='project_tasks', blank=True)
    milestones = models.ManyToManyField('Milestone', related_name='project_milestones', blank=True)

    def __str__(self):
        return self.name

    def progress(self):
        total_tasks = self.tasks.count()
        completed_tasks = self.tasks.filter(status='completed').count()
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    def is_delayed(self):
        return self.end_date < timezone.now() and self.status != 'completed'

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='assigned_tasks', 
        blank=True, null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_tasks'
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f"{self.title} ({self.status})"

    def is_overdue(self):
        return self.due_date < timezone.now() and self.status != 'completed'


class Milestone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    is_achieved = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')

    def __str__(self):
        return f"{self.name} ({'Achieved' if self.is_achieved else 'Pending'})"

class Meeting (models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    meeting_date = models.DateTimeField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_meetings'
    )
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='meeting_participants')
    related_group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='meetings')

    def __str__(self):
        return self.name

class Discussion(models.Model):
    topic = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_discussions'
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='discussions')
    messages = models.ManyToManyField('Message', related_name='discussion_messages', blank=True)

    def __str__(self):
        return self.topic

class Message(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_messages'
    )
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message by {self.created_by.username} on {self.created_at}"


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_announcements'
    )
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='announcements')

    def __str__(self):
        return self.title




# from django.db import models
# from django.conf import settings
# from activity.models import Reaction, Share, Category
# from taggit.managers import TaggableManager

# class Group(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     categories = mode
# ls.ManyToManyField(Category, related_name='groupes_categories')
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMembership', related_name='user_groups', db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     group_type = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')], default='public')
#     privacy_level = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')
#     tags = models.CharField(max_length=100, blank=True)
#     cover_image = models.ImageField(upload_to='group_covers/', blank=True, null=True)
#     shares = models.ManyToManyField(Share, related_name='group_shares', blank=True, db_index=True)
#     tags = TaggableManager()

#     def __str__(self):
#         return self.name

# class GroupMembership(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('member', 'Member')], default='member')
#     joined_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.user.username} in {self.group.name}"