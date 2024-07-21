from django.urls import path
from courses import views

urlpatterns = [
    path('create/', views.create_course, name='create_course'),
    path('list/', views.get_courses, name='get_courses'),
    path('get/<int:course_id>/', views.get_specific_course, name='get_course'),
    path('update/<int:course_id>/', views.update_course, name='update_course'),
    path('delete/<int:course_id>/', views.delete_specific_course, name='delete_course'),
    path('delete/', views.delete_all_courses, name='delete_all_courses'),
    path('enroll/<int:course_id>/<int:user_id>/', views.enroll_course, name='enroll_course'),
    path('progress/<int:course_id>/<int:user_id>/', views.update_course_progress, name='track_course_progress'),
    path('complete/<int:course_id>/<int:user_id>/', views.complete_course, name='complete_course'),
    path('add_lesson/<int:course_id>/', views.add_lesson_to_course, name='add_lesson_to_course'),
    path('list_lessons/<int:course_id>/', views.get_lessons_by_course, name='get_lessons_by_course'),
    path('get_lesson_by_order/<int:course_id>/<int:lesson_order>/', views.get_specific_lesson_by_order, name='get_specific_lesson'),
    path('update_lesson/<int:course_id>/<int:lesson_id>/', views.update_lesson, name='update_lesson'),
    path('delete_lesson/<int:course_id>/', views.delete_all_course_lessons , name='delete_all_lessons'),
    path('delete_specific_lesson/<int:course_id>/<int:lesson_id>/', views.delete_specific_lesson, name='delete_specific_lesson'),
]