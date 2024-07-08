from django.urls import path
from .views import share_certification, email_certification, dashboard, verify_certification, renew_certification, analytics, certification_detail

urlpatterns = [
    path('share/<str:unique_id>/', share_certification, name='share_certification'),
    path('email/<int:cert_id>/', email_certification, name='email_certification'),
    path('dashboard/', dashboard, name='dashboard'),
    path('verify/<int:cert_id>/', verify_certification, name='verify_certification'),
    path('renew/<int:cert_id>/', renew_certification, name='renew_certification'),
    path('analytics/', analytics, name='analytics'),
    path('certification/<int:pk>/', certification_detail, name='certification_detail'),
]
