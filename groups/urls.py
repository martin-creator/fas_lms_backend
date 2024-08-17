from django.urls import path
from groups import views

urlpatterns = [
    path('', views.get_groups, name='get_groups'),
    # path('<int:group_id>/', views.get_group, name='get_group'),
   
]
