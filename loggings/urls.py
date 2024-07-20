from django.urls import path
from loggings.views import index

urlpatterns = [
    path('', index, name='index')
]