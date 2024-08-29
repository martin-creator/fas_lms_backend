from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from connections.models import Connection, ConnectionRequest
from connections.serializers import ConnectionSerializer, ConnectionRequestSerializer
from connections.controllers.connections_controller import ConnectionController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


connection_controller = ConnectionController()


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all connections',
            description='Get all connections',
            value={
                'user': 'user',
                'connection': 'connection',
                'created_at': 'created_at'
            }
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of connections')}
)
@api_view(['GET'])
def get_connections(request):
    """
    API endpoint that allows all connections to be retrieved.
    """
    if request.method == 'GET':
        connections = connection_controller.get_all_connections()
        return Response(connections, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='connection_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific connection',
            description='Get a specific connection',
            value={
                'user': 'user',
                'connection': 'connection',
                'created_at': 'created_at'
            }
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection data')}
)
@api_view(['GET'])
def get_specific_connection(request, connection_id):
    """
    API endpoint that allows a specific connection to be retrieved.
    """
    if request.method == 'GET':
        connection = connection_controller.get_connection(connection_id)
        return Response(connection, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='connection', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new connection',
            description='Create a new connection',
            value={
                'user': 'user',
                'connection': 'connection',
                'created_at': 'created_at'
            }
        )
    ],
    request=ConnectionSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection data')}
)
@api_view(['POST'])
def create_connection(request):
    """
    API endpoint that allows a new connection to be created.
    """
    if request.method == 'POST':
        connection = connection_controller.create_connection(request.data)
        return Response(connection, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='connection_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='connection', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a connection',
            description='Update a connection',
            value={
                'user': 'user',
                'connection': 'connection',
                'created_at': 'created_at'
            }
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection data')}
)
@api_view(['PUT'])
def update_connection(request, connection_id):
    """
    API endpoint that allows a connection to be updated.
    """
    if request.method == 'PUT':
        connection = connection_controller.update_connection(connection_id, request.data)
        return Response(connection, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='connection_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a connection',
            description='Delete a connection',
            value={}
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection data')}
)
@api_view(['DELETE'])
def delete_connection(request, connection_id):
    """
    API endpoint that allows a connection to be deleted.
    """
    if request.method == 'DELETE':
        connection = connection_controller.delete_connection(connection_id)
        return Response(connection, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all connections',
            description='Delete all connections',
            value={}
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection data')}
)
@api_view(['DELETE'])
def delete_all_connections(request):
    """
    API endpoint that allows all connections to be deleted.
    """
    if request.method == 'DELETE':
        connections = connection_controller.delete_all_connections()
        return Response(connections, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all connection requests',
            description='Get all connection requests',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of connection requests')}
)
@api_view(['GET'])
def get_connection_requests(request):
    """
    API endpoint that allows all connection requests to be retrieved.
    """
    if request.method == 'GET':
        connection_requests = connection_controller.get_all_connection_requests()
        return Response(connection_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific connection request',
            description='Get a specific connection request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection request data')}
)
@api_view(['GET'])
def get_specific_connection_request(request, request_id):
    """
    API endpoint that allows a specific connection request to be retrieved.
    """
    if request.method == 'GET':
        connection_request = connection_controller.get_connection_request(request_id)
        return Response(connection_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='from_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='to_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new connection request',
            description='Create a new connection request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection request data')}
)
@api_view(['POST'])
def create_connection_request(request):
    """
    API endpoint that allows a new connection request to be created.
    """
    if request.method == 'POST':
        connection_request = connection_controller.create_connection_request(request.data)
        return Response(connection_request, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='from_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='to_user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a connection request',
            description='Update a connection request',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection request data')}
)
@api_view(['PUT'])
def update_connection_request(request, request_id):
    """
    API endpoint that allows a connection request to be updated.
    """
    if request.method == 'PUT':
        connection_request = connection_controller.update_connection_request(request_id, request.data)
        return Response(connection_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='request_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a connection request',
            description='Delete a connection request',
            value={}
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection request data')}
)
@api_view(['DELETE'])
def delete_connection_request(request, request_id):
    """
    API endpoint that allows a connection request to be deleted.
    """
    if request.method == 'DELETE':
        connection_request = connection_controller.delete_connection_request(request_id)
        return Response(connection_request, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all connection requests',
            description='Delete all connection requests',
            value={}
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Connection request data')}
)
@api_view(['DELETE'])
def delete_all_connection_requests(request):
    """
    API endpoint that allows all connection requests to be deleted.
    """
    if request.method == 'DELETE':
        connection_requests = connection_controller.delete_all_connection_requests()
        return Response(connection_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all connections for a specific user',
            description='Get all connections for a specific user',
            value={
                'user': 'user',
                'connection': 'connection',
                'created_at': 'created_at'
            }
        )
    ],
    request=ConnectionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of connections')}
)
@api_view(['GET'])
def get_user_connections(request, user_id):
    """
    API endpoint that allows all connections for a specific user to be retrieved.
    """
    if request.method == 'GET':
        connections = connection_controller.get_user_connections(user_id)
        return Response(connections, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all connection requests for a specific user',
            description='Get all connection requests for a specific user',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of connection requests')}
)
@api_view(['GET'])
def get_user_connection_requests(request, user_id):
    """
    API endpoint that allows all connection requests for a specific user to be retrieved.
    """
    if request.method == 'GET':
        connection_requests = connection_controller.get_user_connection_requests(user_id)
        return Response(connection_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all connection requests for a specific user with a specific status',
            description='Get all connection requests for a specific user with a specific status',
            value={
                'from_user': 'from_user',
                'to_user': 'to_user',
                'status': 'status',
                'created_at': 'created_at',
                'updated_at': 'updated_at'
            }
        )
    ],
    request=ConnectionRequestSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of connection requests')}
)
@api_view(['GET'])
def get_user_connection_requests_by_status(request, user_id, status):
    """
    API endpoint that allows all connection requests for a specific user with a specific status to be retrieved.
    """
    if request.method == 'GET':
        connection_requests = connection_controller.get_user_connection_requests_by_status(user_id, status)
        return Response(connection_requests, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# urlpatterns = [
#     path('', views.get_companies, name='get_companies'),
#     path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
#     path('companies/create/', views.create_company, name='create_company'),
#     path('companies/update/<int:company_id>/', views.update_company, name='update_company'),
#     path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
#     path('companies/delete/all/', views.delete_all_companies, name='delete_all_companies'),
#     path('companies/updates/<int:company_id>/', views.get_company_updates, name='get_company_updates'),
#     path('<int:update_id>/', views.get_specific_company_update, name='get_specific_company_update'),
#     path('companies/updates/create/<int:company_id>/', views.create_company_update, name='create_company_update'),
#     path('companies/updates/update/<int:company_id>/<int:update_id>/', views.update_company_update, name='update_company_update'),
#     path('companies/updates/delete/<int:update_id>/', views.delete_company_update, name='delete_company_update'),
#     # path('events/', views.get_events),
#     # path('events/<int:event_id>/', views.get_event),
#     # path('events/create/', views.create_event),
# ]

# Generate url patterns for all the views above following this format.
# the functions SHOULD be imported from the views.functions file
    


    
    
    


    