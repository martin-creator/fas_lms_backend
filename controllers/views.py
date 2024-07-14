from rest_framework import generics
from rest_framework.response import Response
from .models import RegisteredController
from .serializers import RegisteredControllerSerializer

class RegisterControllerView(generics.CreateAPIView):
    queryset = RegisteredController.objects.all()
    serializer_class = RegisteredControllerSerializer

class ListControllersView(generics.ListAPIView):
    queryset = RegisteredController.objects.all()
    serializer_class = RegisteredControllerSerializer


class RegisterActivityControllerView(generics.CreateAPIView):
    queryset = RegisteredController.objects.all()
    serializer_class = RegisteredControllerSerializer

    def perform_create(self, serializer):
        # Example endpoint for registering ActivityController
        data = {
            'name': 'ActivityController',
            'app_name': 'activity',
            'description': 'Controller for managing user activities.',
            'endpoint': '/api/activity/activities/',
        }
        serializer.save(**data)
