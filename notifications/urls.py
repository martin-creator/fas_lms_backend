from django.urls import path
from notifications import views

urlpatterns = [
    path('notifications/', views.create_notification, name='create_notification'),
    path('notifications/<int:notification_id>/', views.get_notification, name='get_notification'),
    path('notifications/<int:notification_id>/update/', views.update_notification, name='update_notification'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
    path('notifications/user/', views.get_user_notifications, name='get_user_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/settings/', views.get_notification_settings, name='get_notification_settings'),
    path('notifications/settings/update/', views.update_notification_settings, name='update_notification_settings'),
    path('notifications/reports/user/<int:user_id>/', views.generate_user_report, name='generate_user_report'),
    path('notifications/reports/summary/', views.generate_summary_report, name='generate_summary_report'),
]