from django.urls import re_path
from . import consumers
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConnectionRequestViewSet, ConnectionViewSet

websocket_urlpatterns = [
    re_path(r'ws/connection/(?P<room_name>\w+)/$', consumers.ConnectionConsumer.as_asgi()),
    re_path(r'ws/connections/$', consumers.ConnectionConsumer.as_asgi()),
]

router = DefaultRouter()
router.register(r'connection-requests', ConnectionRequestViewSet)
router.register(r'connections', ConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



