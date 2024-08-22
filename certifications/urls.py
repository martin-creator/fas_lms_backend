from django.urls import path
from certifications import views

urlpatterns = [
    path('', views.get_certifications, name='get_certifications'),
    path('<int:certification_id>/', views.get_specific_certification, name='get_specific_certification'),
    path('<int:userd_id>/', views.get_certifications_by_user, name='get_certifications_by_user'),
    path('/create/', views.create_certification, name='create_certification'),
    # path('', views.get_companies, name='get_companies'),
    # path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
   
]


# urlpatterns = [
#     path('linkedin/login/', LinkedInLoginView.as_view(), name='linkedin_login'),
#     path('linkedin/callback/', LinkedInCallbackView.as_view(), name='linkedin_callback'),
#     path('generate-certificate/', GenerateCertificateView.as_view(), name='generate_certificate'),
#     path('verify-certificate/<str:credential_id>/', VerifyCertificateView.as_view(), name='verify_certificate'),
#     path('assign-badge/<str:credential_id>/', AssignBadgeView.as_view(), name='assign_badge'),
# ]