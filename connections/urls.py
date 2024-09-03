from django.urls import path
from connections import views

urlpatterns = [
    path('', views.get_connections, name='get_connections'),
    path('<int:connection_id>/', views.get_specific_connection, name='get_specific_connection'),
    path('connections/create/', views.create_connection, name='create_connection'),
    path('connections/update/<int:connection_id>/', views.update_connection, name='update_connection'),
    path('connections/delete/<int:connection_id>/', views.delete_connection, name='delete_connection'),
    path('connections/delete/all/', views.delete_all_connections, name='delete_all_connections'),
    path('connection_requests/', views.get_connection_requests, name='get_connection_requests'),
    path('connection_requests/<int:request_id>/', views.get_specific_connection_request, name='get_specific_connection_request'),
    path('connection_requests/create/', views.create_connection_request, name='create_connection_request'),
    path('connection_requests/update/<int:request_id>/', views.update_connection_request, name='update_connection_request'),
    path('connection_requests/delete/<int:request_id>/', views.delete_connection_request, name='delete_connection_request'),
    path('connection_requests/delete/all/', views.delete_all_connection_requests, name='delete_all_connection_requests'),
    path('user/<int:user_id>/', views.get_user_connections, name='get_user_connections'),
    path('connection_requests/user/<int:user_id>/', views.get_user_connection_requests, name='get_user_connection_requests'),
    path('connection_requests/user/<int:user_id>/status/<str:status>/', views.get_user_connection_requests_by_status, name='get_user_connection_requests_by_status'),
]