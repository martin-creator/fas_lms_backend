from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from events.models import Event, EventRegistration, EventFeedback
from events.serializers import EventSerializer, EventRegistrationSerializer, EventFeedbackSerializer
from events.controllers.event_controller import EventController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

event_controller = EventController()

@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}

)
@api_view(['GET'])
def get_all_events(request):
    """
    Get all events.
    """
    events = event_controller.get_all_events()
    return Response(events, status=status.HTTP_200_OK)



