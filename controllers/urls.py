from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterControllerView.as_view(), name='register-controller'),
    path('list/', views.ListControllersView.as_view(), name='list-controllers'),
    path('register-activity/', views.RegisterActivityControllerView.as_view(), name='register-activity-controller'),
]
