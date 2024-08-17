from django.urls import path
from groups import views

urlpatterns = [
    path('', views.get_groups, name='get_groups'),
    path('<int:group_id>/', views.get_specific_group, name='get_specific_group'),
    path('create/', views.create_group, name='create_group'),
    path('join/<int:group_id>/<int:user_id>/', views.join_group, name='join_group'),
    path('leave/<int:group_id>/<int:user_id>/', views.leave_group, name='leave_group'),
    path('update/<int:group_id>/', views.update_group, name='update_group'),
    path('delete/<int:group_id>/', views.delete_group, name='delete_group'),
    path('delete/', views.delete_all_groups, name='delete_all_groups'),
    path('members/<int:group_id>/', views.get_group_members, name='get_group_members'),
    path('discussion/<int:group_id>/', views.get_group_discussions, name='get_group_discussions'),
    path('discussion/<int:group_id>/<int:discussion_id>/', views.get_specific_discussion, name='get_specific_discussion'),
    path('discussion/<int:group_id>/create/', views.create_discussion, name='create_group_discussion'),
    path('discussion/<int:group_id>/update/<int:discussion_id>/', views.update_discussion, name='update_group_discussion'),
    path('discussion/<int:group_id>/delete/<int:discussion_id>/', views.delete_discussion, name='delete_group_discussion'),
    path('messages/<int:group_id>/', views.get_group_messages, name='get_group_messages'),
    path('messages/<int:group_id>/create/', views.create_message, name='create_group_message'),
    path('messages/<int:group_id>/<int:message_id>/', views.get_specific_message, name='get_specific_message'),
    path('messages/<int:group_id>/delete/<int:message_id>/', views.delete_message, name='delete_group_message'),
    path('messages/<int:group_id>/update/<int:message_id>/', views.update_message, name='update_group_message'),
    path('announcements/<int:group_id>/', views.get_group_announcements, name='get_group_announcements'),
    path('meetings/<int:group_id>/', views.get_group_meetings, name='get_group_meetings'),
    path('tasks/<int:group_id>/', views.get_group_tasks, name='get_group_tasks'),
    path('projects/<int:group_id>/', views.get_group_projects, name='get_group_projects'),
    path('milestones/<int:group_id>/', views.get_group_milestones, name='get_group_milestones'),

    # path('<int:group_id>/', views.get_group, name='get_group'),
   
]
