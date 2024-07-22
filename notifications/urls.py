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
    path('notifications/unread-count/', views.get_unread_notifications_count, name='get_unread_notifications_count'),
    path('notifications/templates/', views.create_notification_template, name='create_notification_template'),
    path('notifications/templates/<str:notification_type>/', views.get_notification_template, name='get_notification_template'),
    path('notifications/types/', views.get_notification_types, name='get_notification_types'),
    path('notifications/subscribe/', views.subscribe_to_notifications, name='subscribe_to_notifications'),
    path('notifications/unsubscribe/', views.unsubscribe_from_notifications, name='unsubscribe_from_notifications'),
    path('notifications/notify-followers/', views.notify_followers, name='notify_followers'),
    path('notifications/notify-all/', views.notify_all_users, name='notify_all_users'),
]