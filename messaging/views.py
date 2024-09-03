from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from messaging.models import Message, ChatRoom, ChatRoomNotification
from messaging.serializers import MessageSerializer, ChatRoomSerializer, ChatRoomNotificationSerializer
from messaging.controllers.messaging_controller import MessagingController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

message_controller = MessagingController()


# Message views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all messages',
            description='Get all messages',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of messages')}
)
@api_view(['GET'])
def get_messages(request):
    """
    API endpoint that allows all messages to be retrieved.
    """
    if request.method == 'GET':
        messages = message_controller.get_all_messages()
        return Response(messages, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific message',
            description='Get a specific message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['GET'])
def get_specific_message(request, message_id):
    """
    API endpoint that allows a specific message to be retrieved.
    """
    if request.method == 'GET':
        message = message_controller.get_message(message_id)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_room', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='sender', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_read', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='parent_message', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_edited', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_deleted', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='reactions', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new message',
            description='Create a new message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['POST'])
def create_message(request):
    """
    API endpoint that allows a new message to be created.
    """
    if request.method == 'POST':
        message = message_controller.create_message(request.data)
        return Response(message, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='chat_room', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='sender', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_read', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='parent_message', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_edited', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='is_deleted', type=bool, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='reactions', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shares', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a message',
            description='Update a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['PUT'])
def update_message(request, message_id):
    """
    API endpoint that allows a message to be updated.
    """
    if request.method == 'PUT':
        message = message_controller.update_message(message_id, request.data)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a message',
            description='Delete a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message deleted')}
)
@api_view(['DELETE'])
def delete_message(request, message_id):
    """
    API endpoint that allows a message to be deleted.
    """
    if request.method == 'DELETE':
        message_controller.delete_message(message_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all messages in a chat',
            description='Get all messages in a chat',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of messages')}
)
@api_view(['GET'])
def get_messages_by_chat(request, chat_id):
    """
    API endpoint that allows all messages in a specific chat to be retrieved.
    """
    if request.method == 'GET':
        messages = message_controller.get_messages_by_chat(chat_id)
        return Response(messages, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='sender_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all messages sent by a user',
            description='Get all messages sent by a user',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of messages')}
)
@api_view(['GET'])
def get_messages_by_sender(request, sender_id):
    """
    API endpoint that allows all messages sent by a specific user to be retrieved.
    """
    if request.method == 'GET':
        messages = message_controller.get_messages_by_sender(sender_id)
        return Response(messages, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Mark a message as read',
            description='Mark a message as read',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['PUT'])
def mark_message_as_read(request, message_id):
    """
    API endpoint that allows a message to be marked as read.
    """
    if request.method == 'PUT':
        message = message_controller.mark_message_as_read(message_id)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='new_content', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Edit a message',
            description='Edit a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['PUT'])
def edit_message(request, message_id):
    """
    API endpoint that allows a message to be edited.
    """
    if request.method == 'PUT':
        message = message_controller.edit_message(message_id, request.data)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a message',
            description='Delete a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message deleted')}
)
@api_view(['DELETE'])
def delete_message(request, message_id):
    """
    API endpoint that allows a message to be deleted.
    """
    if request.method == 'DELETE':
        message_controller.delete_message(message_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the reply chain for a message',
            description='Get the reply chain for a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of messages')}
)
@api_view(['GET'])
def get_reply_chain(request, message_id):
    """
    API endpoint that allows the reply chain for a specific message to be retrieved.
    """
    if request.method == 'GET':
        replies = message_controller.get_reply_chain(message_id)
        return Response(replies, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a preview of a message',
            description='Get a preview of a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['GET'])
def get_preview(request, message_id):
    """
    API endpoint that allows a preview of a specific message to be retrieved.
    """
    if request.method == 'GET':
        preview = message_controller.get_preview(message_id)
        return Response(preview, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a summary of reactions for a message',
            description='Get a summary of reactions for a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['GET'])
def get_reactions_summary(request, message_id):
    """
    API endpoint that allows a summary of reactions for a specific message to be retrieved.
    """
    if request.method == 'GET':
        reactions = message_controller.get_reactions_summary(message_id)
        return Response(reactions, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the content of a message',
            description='Get the content of a message',
            value={
                'chat_room': 'chat_room',
                'sender': 'sender',
                'content': 'content',
                'timestamp': 'timestamp',
                'is_read': 'is_read',
                'message_type': 'message_type',
                'attachments': 'attachments',
                'parent_message': 'parent_message',
                'is_edited': 'is_edited',
                'is_deleted': 'is_deleted',
                'reactions': 'reactions',
                'shares': 'shares'
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['GET'])
def get_content(request, message_id):
    """
    API endpoint that allows the content of a specific message to be retrieved.
    """
    if request.method == 'GET':
        content = message_controller.get_content(message_id)
        return Response(content, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# ChatRoom views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all chat rooms',
            description='Get all chat rooms',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of chat rooms')}
)
@api_view(['GET'])
def get_chat_rooms(request):
    """
    API endpoint that allows all chat rooms to be retrieved.
    """
    if request.method == 'GET':
        chat_rooms = message_controller.get_chat_rooms()
        return Response(chat_rooms, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific chat room',
            description='Get a specific chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room data')}
)
@api_view(['GET'])
def get_specific_chat_room(request, chat_id):
    """
    API endpoint that allows a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        chat_room = message_controller.get_chat_room(chat_id)
        return Response(chat_room, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='roomId', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_at', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new chat room',
            description='Create a new chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room data')}
)
@api_view(['POST'])
def create_chat_room(request):
    """
    API endpoint that allows a new chat room to be created.
    """
    if request.method == 'POST':
        chat_room = message_controller.create_chat_room(request.data)
        return Response(chat_room, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='roomId', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_at', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a chat room',
            description='Update a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room data')}
)
@api_view(['PUT'])
def update_chat_room(request, chat_id):
    """
    API endpoint that allows a chat room to be updated.
    """
    if request.method == 'PUT':
        chat_room = message_controller.update_chat_room(chat_id, request.data)
        return Response(chat_room, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a chat room',
            description='Delete a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room deleted')}
)
@api_view(['DELETE'])
def delete_chat_room(request, chat_id):
    """
    API endpoint that allows a chat room to be deleted.
    """
    if request.method == 'DELETE':
        message_controller.delete_chat_room(chat_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add a member to a chat room',
            description='Add a member to a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room data')}
)
@api_view(['PUT'])
def add_member_to_chat_room(request, chat_id, user_id):
    """
    API endpoint that allows a member to be added to a chat room.
    """
    if request.method == 'PUT':
        chat_room = message_controller.add_member_to_chat_room(chat_id, user_id)
        return Response(chat_room, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Remove a member from a chat room',
            description='Remove a member from a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Chat room data')}
)
@api_view(['PUT'])
def remove_member_from_chat_room(request, chat_id, user_id):
    """
    API endpoint that allows a member to be removed from a chat room.
    """
    if request.method == 'PUT':
        chat_room = message_controller.remove_member_from_chat_room(chat_id, user_id)
        return Response(chat_room, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all members in a chat room',
            description='Get all members in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of members')}
)
@api_view(['GET'])
def get_chat_room_members(request, chat_id):
    """
    API endpoint that allows all members in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        members = message_controller.get_chat_room_members(chat_id)
        return Response(members, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of messages in a chat room',
            description='Get the count of messages in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message count')}
)
@api_view(['GET'])
def get_chat_room_messages_count(request, chat_id):
    """
    API endpoint that allows the count of messages in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_messages_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of members in a chat room',
            description='Get the count of members in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Member count')}
)
@api_view(['GET'])
def get_chat_room_members_count(request, chat_id):
    """
    API endpoint that allows the count of members in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_members_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of unread messages in a chat room',
            description='Get the count of unread messages in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Unread message count')}
)
@api_view(['GET'])
def get_chat_room_unread_messages_count(request, chat_id):
    """
    API endpoint that allows the count of unread messages in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_unread_messages_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of read messages in a chat room',
            description='Get the count of read messages in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Read message count')}
)
@api_view(['GET'])
def get_chat_room_read_messages_count(request, chat_id):
    """
    API endpoint that allows the count of read messages in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_read_messages_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of unread messages in a chat room',
            description='Get the count of unread messages in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Unread message count')}
)
@api_view(['GET'])
def get_chat_room_unread_messages_count(request, chat_id):
    """
    API endpoint that allows the count of unread messages in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_unread_messages_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get the count of messages in a chat room',
            description='Get the count of messages in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message count')}
)
@api_view(['GET'])
def get_chat_room_messages_count(request, chat_id):
    """
    API endpoint that allows the count of messages in a specific chat room to be retrieved.
    """
    if request.method == 'GET':
        count = message_controller.get_chat_room_messages_count(chat_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all notifications for a user in a chat room',
            description='Get all notifications for a user in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of notifications')}
)
@api_view(['GET'])
def get_chat_room_notifications(request, chat_id, user_id):
    """
    API endpoint that allows all notifications for a user in a chat room to be retrieved.
    """
    if request.method == 'GET':
        notifications = message_controller.get_chat_room_notifications(chat_id, user_id)
        return Response(notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='notification_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Mark a notification as read',
            description='Mark a notification as read',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],

    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['PUT'])
def mark_chat_room_notification_as_read(request, notification_id):
    """
    API endpoint that allows a notification to be marked as read.
    """
    if request.method == 'PUT':
        notification = message_controller.mark_chat_room_notification_as_read(notification_id)
        return Response(notification, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new notification for a user in a chat room',
            description='Create a new notification for a user in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Notification data')}
)
@api_view(['POST'])
def create_chat_room_notification(request):
    """
    API endpoint that allows a new notification for a user in a chat room to be created.
    """
    if request.method == 'POST':
        notification = message_controller.create_chat_room_notification(request.data)
        return Response(notification, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='chat_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all unread notifications for a user in a chat room',
            description='Get all unread notifications for a user in a chat room',
            value={
                'roomId': 'roomId',
                'members': 'members',
                'name': 'name',
                'created_at': 'created_at'
            }
        )
    ],
    request=ChatRoomSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of notifications')}
)
@api_view(['GET'])
def get_unread_notifications(request, chat_id, user_id):
    """
    API endpoint that allows all unread notifications for a user in a chat room to be retrieved.
    """
    if request.method == 'GET':
        notifications = message_controller.get_unread_notifications(chat_id, user_id)
        return Response(notifications, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


    


# Generare url patterns for all the views above following this format.
# the functions SHOULD be imported from the views.function
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
    


    


