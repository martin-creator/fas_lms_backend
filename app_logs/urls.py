from django.urls import path
from app_logs.views import index

urlpatterns = [
    path('', index, name='index')
]