from django.urls import path
from companies import views

urlpatterns = [
    path('companies/', views.get_companies, name='get_companies'),
    path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
    path('companies/create/', views.create_company, name='create_company'),
    path('companies/update/<int:company_id>/', views.update_company, name='update_company'),
    path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
    # path('events/', views.get_events),
    # path('events/<int:event_id>/', views.get_event),
    # path('events/create/', views.create_event),
]