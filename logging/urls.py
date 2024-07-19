from django.urls import path
from logging.views import index

urlpatterns = [
    path('', index, name='index')
]