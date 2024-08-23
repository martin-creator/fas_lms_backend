from django.contrib import admin
from .models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from django.conf import settings
from django.utils.html import format_html
from activity.models import Share, Category

# Inline for GroupMembership
class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1
    readonly_fields = ('joined_at',)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_summary', 'group_type', 'privacy_level', 'created_at')
    list_filter = ('group_type', 'privacy_level', 'categories')
    search_fields = ('name', 'description')

    def description_summary(self, obj):
        return obj.description[:100] + '...' if len(obj.description) > 100 else obj.description
    description_summary.short_description = 'Description'

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'joined_at')
    list_filter = ('role', 'joined_at')
    search_fields = ('user__user__username', 'group__name')

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'group', 'created_at')
    list_filter = ('group', 'created_at')
    search_fields = ('topic', 'group__name')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'discussion', 'created_at')
    list_filter = ('discussion', 'created_at')
    search_fields = ('created_by__username', 'discussion__title')

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'created_at')
    list_filter = ('group', 'created_at')
    search_fields = ('title', 'group__name')


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'related_group', 'meeting_date')
    list_filter = ('related_group', 'meeting_date')
    search_fields = ('name', 'related_group__name')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'due_date')
    list_filter = ('project', 'status', 'due_date')
    search_fields = ('title', 'project__name')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name',  'description', 'start_date', 'end_date')
    list_filter = ('name', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'due_date')
    list_filter = ('project', 'due_date')
    search_fields = ('name', 'project__name')



