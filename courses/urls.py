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
    path('lesson_progress/<int:course_id>/<int:lesson_id>/<int:user_id>/', views.register_lesson_progress, name='make_lesson_progress'),
    path('create_quiz/<int:course_id>/<int:lesson_id>/', views.create_lesson_quiz, name='create_lesson_quiz'),
    path('add_question_to_quiz/<int:quiz_id>/', views.add_question_to_quiz, name='add_question_to_quiz'),
    path('update_question/<int:quiz_id>/<int:question_id>/', views.update_question, name='update_question'),
    path('list_quiz_questions/<int:quiz_id>/', views.get_all_questions_for_quiz, name='get_quiz_questions'),
    path('submit_lessson_quiz/<user_id>/<quiz_id>/', views.submit_lesson_quiz, name='submit_lesson_quiz'),
]


# addd routes to create bootcamp that has specific courses, tracking lesson progress
# and quiz completion
# Add routes for delete most of the resources
# Add routes for updating most of the resources