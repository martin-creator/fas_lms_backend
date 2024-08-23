from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from followers.models import Follower, FollowRequest, FollowNotification
from followers.serializers import FollowerSerializer, FollowRequestSerializer, FollowNotificationSerializer
from followers.controllers.followers_controller import FollowerController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

follower_controller = FollowerController()


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all followers',
            description='Get all followers',
            value={
                'user': 'user',
                'follower': 'follower',
                'followed_at': 'followed_at'
            }
        )
    ],
    request=FollowerSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of followers')}
)
@api_view(['GET'])
def get_followers(request):
    """
    API endpoint that allows all followers to be retrieved.
    """
    if request.method == 'GET':
        followers = follower_controller.get_all_followers()
        return Response(followers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='follower_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific follower',
            description='Get a specific follower',
            value={
                'user': 'user',
                'follower': 'follower',
                'followed_at': 'followed_at'
            }
        )
    ],
    request=FollowerSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follower data')}
)
@api_view(['GET'])
def get_specific_follower(request, follower_id):
    """
    API endpoint that allows a specific follower to be retrieved.
    """
    if request.method == 'GET':
        follower = follower_controller.get_follower_by_id(follower_id)
        return Response(follower, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all followers of a specific user',
            description='Get all followers of a specific user',
            value={
                'user': 'user',
                'follower': 'follower',
                'followed_at': 'followed_at'
            }
        )
    ],
    request=FollowerSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of followers')}
)
@api_view(['GET'])
def get_followers_by_user(request, user_id):
    """
    API endpoint that allows all followers of a specific user to be retrieved.
    """
    if request.method == 'GET':
        followers = follower_controller.get_followers_by_user(user_id)
        return Response(followers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all followers of a specific company',
            description='Get all followers of a specific company',
            value={
                'user': 'user',
                'follower': 'follower',
                'followed_at': 'followed_at'
            }
        )
    ],
    request=FollowerSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of followers')}
)
@api_view(['GET'])
def get_followers_by_company(request, company_id):
    """
    API endpoint that allows all followers of a specific company to be retrieved.
    """
    if request.method == 'GET':
        followers = follower_controller.get_followers_by_company(company_id)
        return Response(followers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all followers of a specific user for a specific company',
            description='Get all followers of a specific user for a specific company',
            value={
                'user': 'user',
                'follower': 'follower',
                'followed_at': 'followed_at'
            }
        )
    ],
    request=FollowerSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of followers')}
)
@api_view(['GET'])
def get_followers_by_user_and_company(request, user_id, company_id):
    """
    API endpoint that allows all followers of a specific user for a specific company to be retrieved.
    """
    if request.method == 'GET':
        followers = follower_controller.get_followers_by_user_and_company(user_id, company_id)
        return Response(followers, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow requests',
            description='Get all follow requests',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow requests')}
)
@api_view(['GET'])
def get_follow_requests(request):
    """
    API endpoint that allows all follow requests to be retrieved.
    """
    if request.method == 'GET':
        follow_requests = follower_controller.get_all_follow_requests()
        return Response(follow_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific follow request',
            description='Get a specific follow request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow request data')}
)
@api_view(['GET'])
def get_specific_follow_request(request, request_id):
    """
    API endpoint that allows a specific follow request to be retrieved.
    """
    if request.method == 'GET':
        follow_request = follower_controller.get_follow_request_by_id(request_id)
        return Response(follow_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow requests for a user',
            description='Get all follow requests for a user',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow requests')}
)
@api_view(['GET'])
def get_follow_requests_by_user(request, user_id):
    """
    API endpoint that allows all follow requests for a user to be retrieved.
    """
    if request.method == 'GET':
        follow_requests = follower_controller.get_follow_requests_by_user(user_id)
        return Response(follow_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),\
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow requests for a company',
            description='Get all follow requests for a company',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow requests')}
)
@api_view(['GET'])
def get_follow_requests_by_company(request, company_id):
    """
    API endpoint that allows all follow requests for a company to be retrieved.
    """
    if request.method == 'GET':
        follow_requests = follower_controller.get_follow_requests_by_company(company_id)
        return Response(follow_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow requests for a user for a company',
            description='Get all follow requests for a user for a company',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow requests')}
)
@api_view(['GET'])
def get_follow_requests_by_user_and_company(request, user_id, company_id):
    """
    API endpoint that allows all follow requests for a user for a company to be retrieved.
    """
    if request.method == 'GET':
        follow_requests = follower_controller.get_follow_requests_by_user_and_company(user_id, company_id)
        return Response(follow_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='from_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='to_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new follow request',
            description='Create a new follow request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow request data')}
)
@api_view(['POST'])
def create_follow_request(request):
    """
    API endpoint that allows a new follow request to be created.
    """
    if request.method == 'POST':
        follow_request = follower_controller.create_follow_request(request.data)
        return Response(follow_request, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='from_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='to_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a follow request',
            description='Update a follow request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'message': 'message'
            }
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow request data')}
)
@api_view(['PUT','GET'])
def update_follow_request(request, request_id):
    """
    API endpoint that allows a follow request to be updated.
    """
    if request.method == 'PUT':
        follow_request = follower_controller.update_follow_request(request_id, request.data)
        return Response(follow_request, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        follow_request = follower_controller.get_follow_request_by_id(request_id)
        return Response(follow_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a follow request',
            description='Delete a follow request',
            value={}
        )
    ],
    request=FollowRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow request data')}
)
@api_view(['DELETE'])
def delete_follow_request(request, request_id):
    """
    API endpoint that allows a follow request to be deleted.
    """
    if request.method == 'DELETE':
        follow_request = follower_controller.delete_follow_request(request_id)
        return Response(follow_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow notifications',
            description='Get all follow notifications',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow notifications')}
)
@api_view(['GET'])
def get_follow_notifications(request):
    """
    API endpoint that allows all follow notifications to be retrieved.
    """
    if request.method == 'GET':
        follow_notifications = follower_controller.get_all_follow_notifications()
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific follow notification',
            description='Get a specific follow notification',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow notification data')}
)
@api_view(['GET'])
def get_specific_follow_notification(request, notification_id):
    """
    API endpoint that allows a specific follow notification to be retrieved.
    """
    if request.method == 'GET':
        follow_notification = follower_controller.get_follow_notification_by_id(notification_id)
        return Response(follow_notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow notifications for a user',
            description='Get all follow notifications for a user',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow notifications')}
)
@api_view(['GET'])
def get_follow_notifications_by_user(request, user_id):
    """
    API endpoint that allows all follow notifications for a user to be retrieved.
    """
    if request.method == 'GET':
        follow_notifications = follower_controller.get_follow_notifications_by_user(user_id)
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow notifications for a company',
            description='Get all follow notifications for a company',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow notifications')}
)
@api_view(['GET'])
def get_follow_notifications_by_company(request, company_id):
    """
    API endpoint that allows all follow notifications for a company to be retrieved.
    """
    if request.method == 'GET':
        follow_notifications = follower_controller.get_follow_notifications_by_company(company_id)
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new follow notification',
            description='Create a new follow notification',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow notification data')}
)
@api_view(['POST'])
def create_follow_notification(request):
    """
    API endpoint that allows a new follow notification to be created.
    """
    if request.method == 'POST':
        follow_notification = follower_controller.create_follow_notification(request.data)
        return Response(follow_notification, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a follow notification',
            description='Update a follow notification',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow notification data')}
)
@api_view(['PUT','GET'])
def update_follow_notification(request, notification_id):
    """
    API endpoint that allows a follow notification to be updated.
    """
    if request.method == 'PUT':
        follow_notification = follower_controller.update_follow_notification(notification_id, request.data)
        return Response(follow_notification, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        follow_notification = follower_controller.get_follow_notification_by_id(notification_id)
        return Response(follow_notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a follow notification',
            description='Delete a follow notification',
            value={}
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow notification data')}
)
@api_view(['DELETE'])
def delete_follow_notification(request, notification_id):
    """
    API endpoint that allows a follow notification to be deleted.
    """
    if request.method == 'DELETE':
        follow_notification = follower_controller.delete_follow_notification(notification_id)
        return Response(follow_notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all follow notifications',
            description='Delete all follow notifications',
            value={}
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Follow notification data')}
)
@api_view(['DELETE'])
def delete_all_follow_notifications(request):
    """
    API endpoint that allows all follow notifications to be deleted.
    """
    if request.method == 'DELETE':
        follow_notifications = follower_controller.delete_all_follow_notifications()
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow notifications for a user',
            description='Get all follow notifications for a user',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow notifications')}
)
@api_view(['GET'])
def get_follow_notifications_by_user(request, user_id):
    """
    API endpoint that allows all follow notifications for a user to be retrieved.
    """
    if request.method == 'GET':
        follow_notifications = follower_controller.get_follow_notifications_by_user(user_id)
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='company_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all follow notifications for a company',
            description='Get all follow notifications for a company',
            value={
                'user': 'user',
                'message': 'message',
                'created_at': 'created_at'
            }
        )
    ],
    request=FollowNotificationSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of follow notifications')}
)
@api_view(['GET'])
def get_follow_notifications_by_company(request, company_id):
    """
    API endpoint that allows all follow notifications for a company to be retrieved.
    """
    if request.method == 'GET':
        follow_notifications = follower_controller.get_follow_notifications_by_company(company_id)
        return Response(follow_notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
