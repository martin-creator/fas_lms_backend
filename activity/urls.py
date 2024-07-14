from django.urls import path
from activity import views

urlpatterns = [
    path('activities/', views.get_user_activities, name='get_user_activities'),
    path('activities/create/', views.create_activity, name='create_activity'),
    path('activities/update/<int:id>/', views.update_activity, name='update_activity'),
    path('activities/delete/<int:id>/', views.delete_activity, name='delete_activity'),
    path('activities/<int:id>/', views.get_activity_by_id, name='get_activity_by_id'),
    path('activities/category/<str:category_name>/', views.get_activities_by_category, name='get_activities_by_category'),
    path('categories/popular/', views.get_popular_categories, name='get_popular_categories'),
    path('reactions/add/', views.add_reaction, name='add_reaction'),
    path('activities/share/', views.share_activity, name='share_activity'),
    path('attachments/add/', views.add_attachment, name='add_attachment'),
    path('attachments/activity/<int:activity_id>/', views.get_attachments_for_activity, name='get_attachments_for_activity'),
    path('engagement/analyze/', views.analyze_user_engagement, name='analyze_user_engagement'),
    path('analytics/trending/', views.get_trending_topics, name='get_trending_topics'),
    path('settings/activity/', views.get_activity_settings, name='get_activity_settings'),
    path('settings/activity/update/', views.update_activity_settings, name='update_activity_settings'),
]
