from django.urls import path
from events import views

url_patterns = [
    # path('create/', views.create_event, name='create_event'),
    path('list/', views.get_all_events, name='get_all_events'),
    # path('get/<int:event_id>/', views.get_specific_event, name='get_event'),
    # path('update/<int:event_id>/', views.update_event, name='update_event'),
    # path('delete/<int:event_id>/', views.delete_specific_event, name='delete_event'),
    # path('delete/', views.delete_all_events, name='delete_all_events'),
    # path('register/<int:event_id>/<int:user_id>/', views.register_event, name='register_event'),
    # path('feedback/<int:event_id>/<int:user_id>/', views.give_feedback, name='give_feedback'),
    # path('unregister/<int:event_id>/<int:user_id>/', views.unregister_event, name='unregister_event'),
    # path('attendees/<int:event_id>/', views.get_event_attendees, name='get_event_attendees'),
    # path('registrations/<int:event_id>/', views.get_event_registrations, name='get_event_registrations'),
    # path('feedbacks/<int:event_id>/', views.get_event_feedbacks, name='get_event_feedbacks'),
]