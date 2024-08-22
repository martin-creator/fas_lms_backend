from django.urls import path
from certifications import views

urlpatterns = [
    path('linkedin/login/', views.linkedin_login, name='linkedin_login'),
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),
    path('certifications/', views.get_certifications, name='get_all_certifications'),
    path('<int:certification_id>/', views.get_specific_certification, name='get_specific_certification'),
    path('<user_id>/certifications/', views.get_certifications_by_user, name='get_certifications_by_user'),
    path('create/', views.create_certification, name='create_certification'),
    path('update/', views.update_certification, name='update_certification'),
    path('delete/', views.delete_certification, name='delete_certification'),
    path('generate-certificate/', views.generate_pdf_certificate, name='generate_pdf_certificate'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
    path('revoke-certificate/', views.revoke_certificate, name='revoke_certificate'),
    path('linkedin-badges/', views.get_all_linkedin_badges, name='get_all_linkedin_badges'),
    path('linkedin-badges/<int:badge_id>/', views.get_specific_linkedin_badge, name='get_specific_linkedin_badge'),
    path('linkedin-badges/<int:certification_id>/', views.get_linkedin_badges_by_certification, name='get_linkedin_badges_by_certification'),
    path('linkedin-badges/<int:user_id>/', views.get_linkedin_badges_by_user, name='get_linkedin_badges_by_user'),
    path('linkedin-badges/create/', views.create_linkedin_badge, name='create_linkedin_badge'),
    path('linkedin-badges/update/', views.update_linkedin_badge, name='update_linkedin_badge'),
    path('linkedin-badges/delete/', views.delete_linkedin_badge, name='delete_linkedin_badge'),
    path('linkedin-badges/post/', views.post_badge_to_linkedin, name='post_badge_to_linkedin'),
    path('linkedin-badges/add/', views.add_badge_to_user_linkedin_achievements, name='add_badge_to_user_linkedin_achievements'),
   
]
