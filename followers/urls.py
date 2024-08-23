from django.urls import path
from followers import views

urlpatterns = [
    path('', views.get_followers, name='get_followers'),
    path('<int:follower_id>/', views.get_specific_follower, name='get_specific_follower'),
    path('user/<int:user_id>/', views.get_followers_by_user, name='get_followers_by_user'),
    path('company/<int:company_id>/', views.get_followers_by_company, name='get_followers_by_company'),
    path('user/<int:user_id>/company/<int:company_id>/', views.get_followers_by_user_and_company, name='get_followers_by_user_and_company'),
    path('follow_requests/', views.get_follow_requests, name='get_follow_requests'),
    path('follow_requests/<int:request_id>/', views.get_specific_follow_request, name='get_specific_follow_request'),
    path('follow_requests/user/<int:user_id>/', views.get_follow_requests_by_user, name='get_follow_requests_by_user'),
    path('follow_requests/company/<int:company_id>/', views.get_follow_requests_by_company, name='get_follow_requests_by_company'),
    path('follow_requests/user/<int:user_id>/company/<int:company_id>/', views.get_follow_requests_by_user_and_company, name='get_follow_requests_by_user_and_company'),
    path('follow_requests/', views.create_follow_request, name='create_follow_request'),
    path('follow_requests/<int:request_id>/', views.update_follow_request, name='update_follow_request'),
    path('follow_requests/<int:request_id>/', views.delete_follow_request, name='delete_follow_request'),
    path('follow_notifications/', views.get_follow_notifications, name='get_follow_notifications'),
    path('follow_notifications/<int:notification_id>/', views.get_specific_follow_notification, name='get_specific_follow_notification'),
    path('follow_notifications/', views.create_follow_notification, name='create_follow_notification'),
    path('follow_notifications/<int:notification_id>/', views.update_follow_notification, name='update_follow_notification'),
    path('follow_notifications/<int:notification_id>/', views.delete_follow_notification, name='delete_follow_notification'),
    path('follow_notifications/', views.delete_all_follow_notifications, name='delete_all_follow_notifications'),
    path('follow_notifications/user/<int:user_id>/', views.get_follow_notifications_by_user, name='get_follow_notifications_by_user'),
    path('follow_notifications/company/<int:company_id>/', views.get_follow_notifications_by_company, name='get_follow_notifications_by_company'),
   
]