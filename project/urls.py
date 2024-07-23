"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenVerifyView,TokenObtainPairView,TokenRefreshView

from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from profiles.views import CustomConfirmEmailView

# schema_view = get_schema_view(
#     openapi.Info(
#         title="API Documentation",
#         default_version='v1',
#         description="API documentation for the follower system",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path("admin/", admin.site.urls),
    path('p/', include('django_prometheus.urls')),
    path('', include('loggings.urls')),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',CustomConfirmEmailView.as_view(),name='account_confirm_email',),
    
    path('api/', include('notifications.urls')),
    
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/course/', include('courses.urls')),
    
    path('django-rq/', include('django_rq.urls')),
    
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [path('api-auth/', include('rest_framework.urls')),]