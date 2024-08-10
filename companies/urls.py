from django.urls import path
from companies import views

urlpatterns = [
    path('companies/', views.get_companies, name='get_companies'),
    # path('events/', views.get_events),
    # path('events/<int:event_id>/', views.get_event),
    # path('events/create/', views.create_event),
]