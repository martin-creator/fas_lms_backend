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


# class Event(models.Model):
#     organizer = models.ForeignKey(UserProfile, related_name='organized_events', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     attachments = GenericRelation(Attachment)
#     categories = models.ManyToManyField(Category, related_name='events')
#     location = models.CharField(max_length=255)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     capacity = models.PositiveIntegerField()
#     attendees = models.ManyToManyField(UserProfile, related_name='events', blank=True)
#     tags = TaggableManager()
#     registration_required = models.BooleanField(default=True)
#     is_online = models.BooleanField(default=False)
#     online_link = models.URLField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Create event',
            value={
                'title': 'Event name',
                'description': 'Event description',
                'start_date': '2022-01-01T00:00:00Z',
                'end_date': '2022-01-01T00:00:00Z',
                'location': 'Event location',
                'organizer': 1,
                'attendees': [1, 2],
                'tags': [1, 2],
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}

)
@api_view(['GET'])
def get_all_events(request):
    """
    Get all events.
    """
    events = event_controller.get_all_events()
    return Response(events, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Get specific event',
            value={
                'event_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Specific event')}
)
@api_view(['GET'])
def get_specific_event(request, event_id):
    """
    Get a specific event.
    """
    event = event_controller.get_event(event_id)
    return Response(event, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(name='title', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='description', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='location', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='start_time', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='end_time', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='capacity', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='registration_required', type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='is_online', type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='online_link', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='organizer', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='attendees', type=OpenApiTypes.ANY, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='tags', type=OpenApiTypes.ANY, location=OpenApiParameter.QUERY),
    ],
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Create event',
            value={
                'title': 'Event name',
                'description': 'Event description',
                'start_date': '2022-01-01T00:00:00Z',
                'end_date': '2022-01-01T00:00:00Z',
                'location': 'Event location',
                'organizer': 1,
                'attendees': [1, 2],
                'tags': [1, 2],
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
)
@api_view(['POST'])
def create_event(request):
    """
    Create a new event.
    """
    event_data = request.data
    event = event_controller.create_event(event_data)
    return Response(event, status=status.HTTP_201_CREATED)


@extend_schema(
    parameters=[
        OpenApiParameter(name='title', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='description', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='location', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='start_time', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='end_time', type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='capacity', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='registration_required', type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='is_online', type=OpenApiTypes.BOOL, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='online_link', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='organizer', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='attendees', type=OpenApiTypes.ANY, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='tags', type=OpenApiTypes.ANY, location=OpenApiParameter.QUERY),
    ],
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Create event',
            value={
                'title': 'Event name',
                'description': 'Event description',
                'start_date': '2022-01-01T00:00:00Z',
                'end_date': '2022-01-01T00:00:00Z',
                'location': 'Event location',
                'organizer': 1,
                'attendees': [1, 2],
                'tags': [1, 2],
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
)
@api_view(['PUT','GET'])
def update_event(request, event_id):
    """
    Update an event.
    """
    if request.method == 'PUT':
        event_data = request.data
        event = event_controller.update_event(event_id, event_data)
        return Response(event, status=status.HTTP_200_OK)
    else:
        event = event_controller.get_event(event_id)
        return Response(event, status=status.HTTP_200_OK)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Delete event',
            value={
                'event_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
)
@api_view(['DELETE'])
def delete_specific_event(request, event_id):
    """
    Delete a specific event.
    """
    event_controller.delete_event(event_id)
    return Response(status=status.HTTP_204_NO_CONTENT)

# delete_all_events


@extend_schema(
    request=EventSerializer,
    examples=[
        OpenApiExample(
            name='Delete all events',
            value={}
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All events deleted')}
)
@api_view(['DELETE'])
def delete_all_events(request):
    """
    Delete all events.
    """
    event_controller.delete_all_events()
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='attendee_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventRegistrationSerializer,
    examples=[
        OpenApiExample(
            name='Register for event',
            value={
                'event_id': 1,
                'attendee_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Event registration')}
)
@api_view(['POST'])
def register_event(request, event_id, attendee_id):
    """
    Register for an event.
    """
    event_controller.register_for_event(event_id, attendee_id)
    return Response(status=status.HTTP_201_CREATED)


#  rating = models.PositiveIntegerField()
# feedback = models.TextField()
@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='attendee_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='rating', type=OpenApiTypes.INT, location=OpenApiParameter.QUERY),
        OpenApiParameter(name='feedback', type=OpenApiTypes.STR, location=OpenApiParameter.QUERY),
    ],
    request=EventFeedbackSerializer,
    examples=[
        OpenApiExample(
            name='Give feedback',
            value={
                'event_id': 1,
                'attendee_id': 1,
                'rating': 5,
                'comment': 'Great event!',
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Event feedback')}
)
@api_view(['POST'])
def provide_event_feedback(request, event_id, attendee_id):
    """
    Provide feedback for an event.
    """
    feedback_data = request.data
    event_controller.provide_event_feedback(event_id, attendee_id, feedback_data)
    return Response(status=status.HTTP_201_CREATED)



@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
        OpenApiParameter(name='attendee_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],

    request=EventRegistrationSerializer,
    examples=[
        OpenApiExample(
            name='Unregister from event',
            value={
                'event_id': 1,
                'attendee_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Successfully unregistered')}
)
@api_view(['DELETE'])
def unregister_event(request, event_id, attendee_id):
    """
    Unregister from an event.
    """
    event_controller.unregister_from_event(event_id, attendee_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventRegistrationSerializer,
    examples=[
        OpenApiExample(
            name='Get event attendees',
            value={
                'event_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of attendees')}
)
@api_view(['GET'])
def get_event_attendees(request, event_id):
    """
    Get all attendees for a specific event.
    """
    attendees = event_controller.get_event_attendees(event_id)
    return Response(attendees, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventRegistrationSerializer,
    examples=[
        OpenApiExample(
            name='Get event registrations',
            value={
                'event_id': 1,
            }
        ),
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of registrations')}
)
@api_view(['GET'])
def get_event_registrations(request, event_id):
    """
    Get all event registrations for a specific event.
    """
    registrations = event_controller.get_event_registrations(event_id)
    return Response(registrations, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[
        OpenApiParameter(name='event_id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH),
    ],
    request=EventFeedbackSerializer,
    examples=[
        OpenApiExample(
            name='Get event feedbacks',
            value={
                'event_id': 1,
        },
        )
    ],
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of feedbacks')}
)
@api_view(['GET'])
def get_event_feedbacks(request, event_id):
    """
    Get all feedbacks for a specific event.
    """
    feedbacks = event_controller.get_event_feedbacks(event_id)
    return Response(feedbacks, status=status.HTTP_200_OK)

    







