from django.urls import path
from companies import views

urlpatterns = [
    path('', views.get_companies, name='get_companies'),
    path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
    path('companies/create/', views.create_company, name='create_company'),
    path('companies/update/<int:company_id>/', views.update_company, name='update_company'),
    path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
    path('companies/delete/all/', views.delete_all_companies, name='delete_all_companies'),
    path('companies/updates/<int:company_id>/', views.get_company_updates, name='get_company_updates'),
    path('<int:update_id>/', views.get_specific_company_update, name='get_specific_company_update'),
    path('companies/updates/create/<int:company_id>/', views.create_company_update, name='create_company_update'),
    path('companies/updates/update/<int:company_id>/<int:update_id>/', views.update_company_update, name='update_company_update'),
    path('companies/updates/delete/<int:update_id>/', views.delete_company_update, name='delete_company_update'),
    # path('events/', views.get_events),
    # path('events/<int:event_id>/', views.get_event),
    # path('events/create/', views.create_event),
]


# urlpatterns = [
#     path('linkedin/login/', LinkedInLoginView.as_view(), name='linkedin_login'),
#     path('linkedin/callback/', LinkedInCallbackView.as_view(), name='linkedin_callback'),
#     path('generate-certificate/', GenerateCertificateView.as_view(), name='generate_certificate'),
#     path('verify-certificate/<str:credential_id>/', VerifyCertificateView.as_view(), name='verify_certificate'),
#     path('assign-badge/<str:credential_id>/', AssignBadgeView.as_view(), name='assign_badge'),
# ]