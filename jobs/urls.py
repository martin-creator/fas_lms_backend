from django.urls import path
from jobs import views


urlpatterns = [
    path('', views.get_jobs, name='get_jobs'),
    path('<int:job_id>/', views.get_specific_job, name='get_specific_job'),
    path('create/', views.create_job, name='create_job'),
    path('update/<int:job_id>/', views.update_job, name='update_job'),
    path('delete/<int:job_id>/', views.delete_job, name='delete_job'),
    path('applications/<int:job_id>/', views.get_job_applications, name='get_job_applications'),
    path('applications/<int:application_id>/', views.get_specific_application, name='get_specific_application'),
    path('applications/applicant/<int:applicant_id>/', views.get_applications_by_applicant, name='get_applications_by_applicant'),
    path('applications/create/', views.create_application, name='create_application'),
    path('applications/update/<int:application_id>/', views.update_application, name='update_application'),
    path('applications/delete/<int:application_id>/', views.delete_application, name='delete_application'),
    path('notifications/<int:job_id>/', views.get_job_notifications, name='get_job_notifications'),
    path('notifications/<int:notification_id>/', views.get_specific_notification, name='get_specific_notification'),
    path('notifications/user/<int:user_id>/', views.get_notifications_by_user, name='get_notifications_by_user'),
    path('notifications/create/', views.create_notification, name='create_notification'),
    path('notifications/update/<int:notification_id>/', views.update_notification, name='update_notification'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('interviews/<int:job_id>/', views.get_interviews, name='get_interviews'),
    path('interviews/<int:interview_id>/', views.get_specific_interview, name='get_specific_interview'),
    path('interviews/create/', views.create_interview, name='create_interview'),
    path('interviews/update/<int:interview_id>/', views.update_interview, name='update_interview'),
    path('interviews/delete/<int:interview_id>/', views.delete_interview, name='delete_interview'),
    path('interviews/delete/all/', views.delete_all_interviews, name='delete_all_interviews'),
    path('reports/applications/<int:job_id>/', views.generate_job_application_report, name='generate_job_application_report'),
    path('reports/summary/', views.generate_job_summary, name='generate_job_summary'),
    path('interviews/job/<int:job_id>/', views.get_interviews_by_job, name='get_interviews_by_job'),
    path('interviews/application/<int:application_id>/', views.get_interviews_by_job_application, name='get_interviews_by_job_application'),
]