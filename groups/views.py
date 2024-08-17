from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from groups.models import Group, GroupMembership, Discussion, Message, Announcement, Meeting, Task, Project, Milestone
from groups.serializers import GroupSerializer, GroupMembershipSerializer, DiscussionSerializer, MessageSerializer, AnnouncementSerializer, MeetingSerializer, TaskSerializer, ProjectSerializer, MilestoneSerializer
from groups.controllers.group_controller import GroupController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

group_controller = GroupController()


@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all groups',
            description='Get all groups',
            value={}
        )
    ],
    request=GroupSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of groups')}
)
@api_view(['GET'])
def get_groups(request):
    """
    API endpoint that allows all groups to be retrieved.
    """
    if request.method == 'GET':
        groups = group_controller.get_all_groups()
        return Response(groups, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific group',
            description='Get a specific group',
            value={
                "group_id": 1
            }
        )
    ],
    request=GroupSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_specific_group(request, group_id):
    """
    API endpoint that allows a specific group to be retrieved.
    """
    if request.method == 'GET':
        group = group_controller.get_group_by_id(group_id)
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='group_type', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new group',
            description='Create a new group',
            value={
                "name": "name",
                "description": "description",
                "owner": 1,
                "members": "members",
                "categories": "categories",
                "group_type": "public"
            }
        )
    ],
    request=GroupSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['POST'])
def create_group(request):
    """
    API endpoint that allows a group to be created.
    """
    if request.method == 'POST':
        group_data = request.data
        group = group_controller.create_group(group_data)
        return Response(group, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='group_type', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing group',
            description='Update an existing group',
            value={
                "name": "name",
                "description": "description",
                "owner": 1,
                "members": "members",
                "categories": "categories",
                "group_type": "public"
            }
        )
    ],
    request=GroupSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['PUT','GET'])
def update_group(request, group_id):
    """
    API endpoint that allows an existing group to be updated.
    """
    if request.method == 'PUT':
        group_data = request.data
        group = group_controller.update_group(group_id, group_data)
        return Response(group, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        group = group_controller.get_group_by_id(group_id)
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific group',
            description='Delete a specific group',
            value={}
        )
    ],
    request=GroupSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['DELETE'])
def delete_group(request, group_id):
    """
    API endpoint that allows a specific group to be deleted.
    """
    if request.method == 'DELETE':
        group = group_controller.delete_specific_group(group_id)
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all groups',
            description='Delete all groups',
            value={}
        )
    ],
    request=GroupSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['DELETE'])
def delete_all_groups(request):
    """
    API endpoint that allows all groups to be deleted.
    """
    if request.method == 'DELETE':
        group = group_controller.delete_all_groups()
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group members',
            description='Get group members',
            value={
                "group_id": 1,
                "members": "members"
            }
        )
    ],
    request=GroupMembershipSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_members(request, group_id):
    """
    API endpoint that allows all members in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_members = group_controller.get_group_members(group_id)
        return Response(group_members, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group discussions',
            description='Get group discussions',
            value={
                "group_id": 1,
                "discussions": "discussions"
            }

        )
    ],
    request=DiscussionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_discussions(request, group_id):
    """
    API endpoint that allows all discussions in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_discussions = group_controller.get_group_discussions(group_id)
        return Response(group_discussions, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group messages',
            description='Get group messages',
            value={
                "group_id": 1,
                "messages": "messages"
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_messages(request, group_id):
    """
    API endpoint that allows all messages in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_messages = group_controller.get_group_messages(group_id)
        return Response(group_messages, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Join a group',
            description='Join a group',
            value={}
        )
    ],
    request=GroupMembershipSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['POST'])
def join_group(request, group_id, user_id):
    """
    API endpoint that allows a user to join a group.
    """
    if request.method == 'POST':
        group = group_controller. add_member_to_group(group_id, user_id)
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Leave a group',
            description='Leave a group',
            value={}
        )
    ],
    request=GroupMembershipSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['POST'])
def leave_group(request, group_id, user_id):
    """
    API endpoint that allows a user to leave a group.
    """
    if request.method == 'POST':
        group = group_controller.remove_member_from_group(group_id, user_id)
        return Response(group, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group announcements',
            description='Get group announcements',
            value={}
        )
    ],
    request=AnnouncementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_announcements(request, group_id):
    """
    API endpoint that allows all announcements in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_announcements = group_controller.get_group_announcements(group_id)
        return Response(group_announcements, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group meetings',
            description='Get group meetings',
            value={}
        )
    ],
    request=MeetingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_meetings(request, group_id):
    """
    API endpoint that allows all meetings in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_meetings = group_controller.get_group_meetings(group_id)
        return Response(group_meetings, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group tasks',
            description='Get group tasks',
            value={}
        )
    ],
    request=TaskSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_tasks(request, group_id):
    """
    API endpoint that allows all tasks in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_tasks = group_controller.get_group_tasks(group_id)
        return Response(group_tasks, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group projects',
            description='Get group projects',
            value={}
        )
    ],
    request=ProjectSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_projects(request, group_id):
    """
    API endpoint that allows all projects in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_projects = group_controller.get_group_projects(group_id)
        return Response(group_projects, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@extend(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get group milestones',
            description='Get group milestones',
            value={}
        )
    ],
    request=MilestoneSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Group data')}
)
@api_view(['GET'])
def get_group_milestones(request, group_id):
    """
    API endpoint that allows all milestones in a specific group to be retrieved.
    """
    if request.method == 'GET':
        group_milestones = group_controller.get_group_milestones(group_id)
        return Response(group_milestones, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# create discussion
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new discussion',
            description='Create a new discussion',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants"
            }
        )
    ],
    request=DiscussionSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Discussion data')}
)
@api_view(['POST'])
def create_discussion(request, group_id):
    """
    API endpoint that allows a discussion to be created.
    """
    if request.method == 'POST':
        discussion_data = request.data
        discussion = group_controller.create_discussion(group_id, discussion_data)
        return Response(discussion, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific discussion',
            description='Get a specific discussion',
            value={}
        )
    ],
    request=DiscussionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Discussion data')}
)
@api_view(['GET'])
def get_specific_discussion(request, group_id, discussion_id):
    """
    API endpoint that allows a specific discussion to be retrieved.
    """
    if request.method == 'GET':
        discussion = group_controller.get_discussion_by_id(group_id, discussion_id)
        return Response(discussion, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing discussion',
            description='Update an existing discussion',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants"
            }
        )
    ],
    request=DiscussionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Discussion data')}
)
@api_view(['PUT','GET'])
def update_discussion(request, group_id, discussion_id):
    """
    API endpoint that allows an existing discussion to be updated.
    """
    if request.method == 'PUT':
        discussion_data = request.data
        discussion = group_controller.update_discussion(group_id, discussion_id, discussion_data)
        return Response(discussion, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        discussion = group_controller.get_discussion_by_id(group_id, discussion_id)
        return Response(discussion, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    



@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific discussion',
            description='Delete a specific discussion',
            value={}
        )
    ],
    request=DiscussionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Discussion data')}
)
@api_view(['DELETE'])
def delete_discussion(request, group_id, discussion_id):
    """
    API endpoint that allows a specific discussion to be deleted.
    """
    if request.method == 'DELETE':
        discussion = group_controller.delete_discussion(group_id, discussion_id)
        return Response(discussion, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# create message

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='sender', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new message',
            description='Create a new message',
            value={
                "content": "content",
                "sender": 1
            }
        )
    ],
    request=MessageSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['POST'])
def create_message(request, group_id, discussion_id):
    """
    API endpoint that allows a message to be created.
    """
    if request.method == 'POST':
        message_data = request.data
        message = group_controller.create_message(group_id, discussion_id, message_data)
        return Response(message, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific message',
            description='Get a specific message',
            value={}
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['GET'])
def get_specific_message(request, group_id, discussion_id, message_id):
    """
    API endpoint that allows a specific message to be retrieved.
    """
    if request.method == 'GET':
        message = group_controller.get_message_by_id(group_id, discussion_id, message_id)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='sender', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing message',
            description='Update an existing message',
            value={
                "content": "content",
                "sender": 1
            }
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['PUT','GET'])
def update_message(request, group_id, discussion_id, message_id):
    """
    API endpoint that allows an existing message to be updated.
    """
    if request.method == 'PUT':
        message_data = request.data
        message = group_controller.update_message(group_id, discussion_id, message_id, message_data)
        return Response(message, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        message = group_controller.get_message_by_id(group_id, discussion_id, message_id)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='discussion_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='message_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific message',
            description='Delete a specific message',
            value={}
        )
    ],
    request=MessageSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Message data')}
)
@api_view(['DELETE'])
def delete_message(request, group_id, discussion_id, message_id):
    """
    API endpoint that allows a specific message to be deleted.
    """
    if request.method == 'DELETE':
        message = group_controller.delete_message(group_id, discussion_id, message_id)
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# create announcement
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new announcement',
            description='Create a new announcement',
            value={
                "title": "title",
                "content": "content",
                "owner": 1
            }
        )
    ],
    request=AnnouncementSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Announcement data')}
)
@api_view(['POST'])
def create_announcement(request, group_id):
    """
    API endpoint that allows an announcement to be created.
    """
    if request.method == 'POST':
        announcement_data = request.data
        announcement = group_controller.create_announcement(group_id, announcement_data)
        return Response(announcement, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='announcement_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific announcement',
            description='Get a specific announcement',
            value={
                "group_id": 1,
                "announcement_id": 1
            }
        )
    ],
    request=AnnouncementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Announcement data')}
)
@api_view(['GET'])
def get_specific_announcement(request, group_id, announcement_id):
    """
    API endpoint that allows a specific announcement to be retrieved.
    """
    if request.method == 'GET':
        announcement = group_controller.get_announcement_by_id(group_id, announcement_id)
        return Response(announcement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='announcement_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing announcement',
            description='Update an existing announcement',
            value={
                "title": "title",
                "content": "content",
                "owner": 1
            }
        )
    ],
    request=AnnouncementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Announcement data')}
)
@api_view(['PUT','GET'])
def update_announcement(request, group_id, announcement_id):
    """
    API endpoint that allows an existing announcement to be updated.
    """
    if request.method == 'PUT':
        announcement_data = request.data
        announcement = group_controller.update_announcement(group_id, announcement_id, announcement_data)
        return Response(announcement, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        announcement = group_controller.get_announcement_by_id(group_id, announcement_id)
        return Response(announcement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='announcement_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific announcement',
            description='Delete a specific announcement',
            value={}
        )
    ],
    request=AnnouncementSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Deleted announcement data')}
)
@api_view(['DELETE'])
def delete_announcement(request, group_id, announcement_id):
    """
    API endpoint that allows a specific announcement to be deleted.
    """
    if request.method == 'DELETE':
        announcement = group_controller.delete_announcement(group_id, announcement_id)
        return Response(announcement, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



# create meeting

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_time', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_time', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new meeting',
            description='Create a new meeting',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants",
                "start_time": "2021-09-01 12:00:00",
                "end_time": "2021-09-01 13:00:00"
            }
        )
    ],
    request=MeetingSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Meeting data')}
)
@api_view(['POST'])
def create_meeting(request, group_id):
    """
    API endpoint that allows a meeting to be created.
    """
    if request.method == 'POST':
        meeting_data = request.data
        meeting = group_controller.create_meeting(group_id, meeting_data)
        return Response(meeting, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='meeting_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific meeting',
            description='Get a specific meeting',
            value={}
        )
    ],
    request=MeetingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Meeting data')}
)
@api_view(['GET'])
def get_specific_meeting(request, group_id, meeting_id):
    """
    API endpoint that allows a specific meeting to be retrieved.
    """
    if request.method == 'GET':
        meeting = group_controller.get_meeting_by_id(group_id, meeting_id)
        return Response(meeting, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='meeting_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='start_time', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='end_time', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing meeting',
            description='Update an existing meeting',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants",
                "start_time": "2021-09-01 12:00:00",
                "end_time": "2021-09-01 13:00:00"
            }
        )
    ],
    request=MeetingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Meeting data')}
)
@api_view(['PUT','GET'])
def update_meeting(request, group_id, meeting_id):
    """
    API endpoint that allows an existing meeting to be updated.
    """
    if request.method == 'PUT':
        meeting_data = request.data
        meeting = group_controller.update_meeting(group_id, meeting_id, meeting_data)
        return Response(meeting, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        meeting = group_controller.get_meeting_by_id(group_id, meeting_id)
        return Response(meeting, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='meeting_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific meeting',
            description='Delete a specific meeting',
            value={}
        )
    ],
    request=MeetingSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Meeting data')}
)
@api_view(['DELETE'])
def delete_meeting(request, group_id, meeting_id):
    """
    API endpoint that allows a specific meeting to be deleted.
    """
    if request.method == 'DELETE':
        meeting = group_controller.delete_meeting(group_id, meeting_id)
        return Response(meeting, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# create project

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new project',
            description='Create a new project',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants",
                "start_date": "2021-09-01",
                "end_date": "2021-09-30"
            }
        )
    ],
    request=ProjectSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Project data')}
)
@api_view(['POST'])
def create_project(request, group_id):
    """
    API endpoint that allows a project to be created.
    """
    if request.method == 'POST':
        project_data = request.data
        project = group_controller.create_project(group_id, project_data)
        return Response(project, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific project',
            description='Get a specific project',
            value={}
        )
    ],
    request=ProjectSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Project data')}
)
@api_view(['GET'])
def get_specific_project(request, group_id, project_id):
    """
    API endpoint that allows a specific project to be retrieved.
    """
    if request.method == 'GET':
        project = group_controller.get_project_by_id(group_id, project_id)
        return Response(project, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='owner', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='participants', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing project',
            description='Update an existing project',
            value={
                "title": "title",
                "description": "description",
                "owner": 1,
                "participants": "participants",
                "start_date": "2021-09-01",
                "end_date": "2021-09-30"
            }
        )
    ],
    request=ProjectSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Project data')}
)
@api_view(['PUT','GET'])
def update_project(request, group_id, project_id):
    """
    API endpoint that allows an existing project to be updated.
    """
    if request.method == 'PUT':
        project_data = request.data
        project = group_controller.update_project(group_id, project_id, project_data)
        return Response(project, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        project = group_controller.get_project_by_id(group_id, project_id)
        return Response(project, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific project',
            description='Delete a specific project',
            value={}
        )
    ],
    request=ProjectSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Project data')}
)
@api_view(['DELETE'])
def delete_project(request, group_id, project_id):
    """
    API endpoint that allows a specific project to be deleted.
    """
    if request.method == 'DELETE':
        project = group_controller.delete_project(group_id, project_id)
        return Response(project, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




# create task
# class Task(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled')
#     ]

#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateTimeField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     assigned_to = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE, 
#         related_name='assigned_tasks', 
#         blank=True, null=True
#     )
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE, 
#         related_name='created_tasks'
#     )
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks_in_project')
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='due_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='assigned_to', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_by', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new task',
            description='Create a new task',
            value={
                "title": "title",
                "description": "description",
                "due_date": "2021-09-01 12:00:00",
                "status": "pending",
                "assigned_to": 1,
                "created_by": 1
            }
        )
    ],
    request=TaskSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Task data')}
)
@api_view(['POST'])
def create_task(request, group_id, project_id):
    """
    API endpoint that allows a task to be created.
    """
    if request.method == 'POST':
        task_data = request.data
        task = group_controller.create_task(group_id, project_id, task_data)
        return Response(task, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='task_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific task',
            description='Get a specific task',
            value={}
        )
    ],
    request=TaskSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Task data')}
)
@api_view(['GET'])
def get_specific_task(request, group_id, project_id, task_id):
    """
    API endpoint that allows a specific task to be retrieved.
    """
    if request.method == 'GET':
        task = group_controller.get_task_by_id(group_id, project_id, task_id)
        return Response(task, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='task_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='due_date', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='assigned_to', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='created_by', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing task',
            description='Update an existing task',
            value={
                "title": "title",
                "description": "description",
                "due_date": "2021-09-01 12:00:00",
                "status": "pending",
                "assigned_to": 1,
                "created_by": 1
            }
        )
    ],
    request=TaskSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Task data')}

)
@api_view(['PUT','GET'])
def update_task(request, group_id, project_id, task_id):
    """
    API endpoint that allows an existing task to be updated.
    """
    if request.method == 'PUT':
        task_data = request.data
        task = group_controller.update_task(group_id, project_id, task_id, task_data)
        return Response(task, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        task = group_controller.get_task_by_id(group_id, project_id, task_id)
        return Response(task, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='task_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific task',
            description='Delete a specific task',
            value={}
        )
    ],
    request=TaskSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Task data')}
)
@api_view(['DELETE'])
def delete_task(request, group_id, project_id, task_id):
    """
    API endpoint that allows a specific task to be deleted.
    """
    if request.method == 'DELETE':
        task = group_controller.delete_task(group_id, project_id, task_id)
        return Response(task, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    


# create milestone

@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='due_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='assigned_to', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='created_by', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new milestone',
            description='Create a new milestone',
            value={
                "title": "title",
                "description": "description",
                "due_date": "2021-09-01 12:00:00",
                "status": "pending",
                "assigned_to": 1,
                "created_by": 1
            }
        )
    ],
    request=MilestoneSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Milestone data')}
)
@api_view(['POST'])
def create_milestone(request, group_id, project_id):
    """
    API endpoint that allows a milestone to be created.
    """
    if request.method == 'POST':
        milestone_data = request.data
        milestone = group_controller.create_milestone(group_id, project_id, milestone_data)
        return Response(milestone, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='milestone_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific milestone',
            description='Get a specific milestone',
            value={}
        )
    ],
    request=MilestoneSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Milestone data')}
)
@api_view(['GET'])
def get_specific_milestone(request, group_id, project_id, milestone_id):
    """
    API endpoint that allows a specific milestone to be retrieved.
    """
    if request.method == 'GET':
        milestone = group_controller.get_milestone_by_id(group_id, project_id, milestone_id)
        return Response(milestone, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='milestone_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='due_date', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='status', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='assigned_to', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='created_by', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an existing milestone',
            description='Update an existing milestone',
            value={
                "title": "title",
                "description": "description",
                "due_date": "2021-09-01 12:00:00",
                "status": "pending",
                "assigned_to": 1,
                "created_by": 1
            }
        )
    ],
    request=MilestoneSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Milestone data')}
)
@api_view(['PUT','GET'])
def update_milestone(request, group_id, project_id, milestone_id):
    """
    API endpoint that allows an existing milestone to be updated.
    """
    if request.method == 'PUT':
        milestone_data = request.data
        milestone = group_controller.update_milestone(group_id, project_id, milestone_id, milestone_data)
        return Response(milestone, status=status.HTTP_200_OK)
    elif request.method == 'GET':
        milestone = group_controller.get_milestone_by_id(group_id, project_id, milestone_id)
        return Response(milestone, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@extend_schema(
    parameters=[
        OpenApiParameter(name='group_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='project_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='milestone_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a specific milestone',
            description='Delete a specific milestone',
            value={}
        )
    ],
    request=MilestoneSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Milestone data')}
)
@api_view(['DELETE'])
def delete_milestone(request, group_id, project_id, milestone_id):
    """
    API endpoint that allows a specific milestone to be deleted.
    """
    if request.method == 'DELETE':
        milestone = group_controller.delete_milestone(group_id, project_id, milestone_id)
        return Response(milestone, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    










# course_controller = CourseController()

# # Create your views here.
# # Ony the title, description, instructor, categories and tags are required to create a course
# # should return the id of the created course plus the other fields


# @extend_schema(
#     parameters=[],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get all courses',
#             description='Get all courses',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of courses')}
# )
# @api_view(['GET'])
# def get_courses(request):
#     """
#     API endpoint that allows all courses to be retrieved.
#     """
#     if request.method == 'GET':
#         courses = course_controller.get_all_courses()
#         return Response(courses, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Get a specific course',
#             description='Get a specific course',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['GET'])
# def get_specific_course(request, course_id):
#     """
#     API endpoint that allows a specific course to be retrieved.
#     """
#     if request.method == 'GET':
#         course = course_controller.get_course_by_id(course_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# @csrf_exempt
# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='instructor', type=int, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=True),
#         OpenApiParameter(name='duration', type=int, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='level', type=str, location=OpenApiParameter.QUERY, required=False),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Create a new course',
#             description='Create a new course',
#             value={
#                 "title": "title",
#                 "description": "description",
#                 "instructor_id": 1,
#                 "categories": "categories",
#                 "tags": "tags"
#             }
#         )
#     ],
#     request=CourseCreateSerializer,
#     responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}

# )
# @api_view(['POST'])
# def create_course(request):
#     """
#     API endpoint that allows a course to be created.

#     The following fields are required to create a course:
#     - title
#     - description
#     - instructor_id
#     - categories
#     - tags
#     - duration
#     - level

#     Examples of json data to be sent to the endpoint:
#     {
#         "title": "title",
#         "description": "description",
#         "instructor": 1,
#         "categories": "categories",
#         "tags": "tags",
#         "duration": 10,
#         "level": "Beginner"
#     }

#     Response:
#     {
#         "id": 1,
#         "title": "title",
#         "description": "description",
#         "instructor_id": 1,
#         "categories": "categories",
#         "tags": "tags"
#     }
#     """
#     if request.method == 'POST':
#         course_data = request.data
#         course = course_controller.create_course(course_data)
#         return Response(course, status=status.HTTP_201_CREATED)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    




# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='title', type=str, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='instructor', type=int, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='duration', type=int, location=OpenApiParameter.QUERY, required=False),
#         OpenApiParameter(name='level', type=str, location=OpenApiParameter.QUERY, required=False),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Update an existing course',
#             description='Update an existing course',
#             value={
#                 "title": "title",
#                 "description": "description",
#                 "instructor": 1,
#                 "categories": "categories",
#                 "tags": "tags",
#                 "duration": 10,
#                 "level": "Beginner"
#             }
#         )
#     ],
#     request=CourseCreateSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['PUT','GET'])
# def update_course(request, course_id):
#     """
#     API endpoint that allows an existing course to be updated.

#     The following fields can be updated:
#     - title
#     - description
#     - instructor_id
#     - categories
#     - tags
#     - duration
#     - level

#     Examples of json data to be sent to the endpoint:
#     {
#         "title": "title",
#         "description": "description",
#         "instructor": 1,
#         "categories": "categories",
#         "tags": "tags",
#         "duration": 10,
#         "level": "Beginner"
#     }

#     Response:
#     {
#         "id": 1,
#         "title": "title",
#         "description": "description",
#         "instructor_id": 1,
#         "categories": "categories",
#         "tags": "tags"
#     }
#     """
#     if request.method == 'PUT':
#         course_data = request.data
#         course = course_controller.update_course(course_id, course_data)
#         return Response(course, status=status.HTTP_200_OK)
#     elif request.method == 'GET':
#         course = course_controller.get_course_by_id(course_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Delete a specific course',
#             description='Delete a specific course',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['DELETE'])
# def delete_specific_course(request, course_id):
#     """
#     API endpoint that allows a specific course to be deleted.
#     """
#     if request.method == 'DELETE':
#         course = course_controller.delete_specific_course(course_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Delete all courses',
#             description='Delete all courses',
#             value={}
#         )
#     ],
#     request=CourseSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['DELETE'])
# def delete_all_courses(request):
#     """
#     API endpoint that allows all courses to be deleted.
#     """
#     if request.method == 'DELETE':
#         course = course_controller.delete_all_courses()
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters=[
#         OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Enroll in a course',
#             description='Enroll in a course',
#             value={}
#         )
#     ],
#     request=CourseEnrollmentSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['POST'])
# def enroll_course(request, course_id, user_id):
#     """
#     API endpoint that allows a user to enroll in a course.
#     """
#     if request.method == 'POST':
#         course = course_controller.enroll_course(course_id, user_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# @extend_schema(
#     parameters = [
#          OpenApiParameter(name='course_id', type=int, location=OpenApiParameter.PATH, required=True),
#         OpenApiParameter(name='user_id', type=int, location=OpenApiParameter.QUERY, required=True),
#     ],
#     examples=[
#         OpenApiExample(
#             'Example 1',
#             summary='Update course progress',
#             description='Update course progress',
#             value={}
#         )
#     ],
#     request=CourseCompletionSerializer,
#     responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Course data')}
# )
# @api_view(['GET'])
# def update_course_progress(request, course_id, user_id):
#     """
#     API endpoint that allows a user to update course progress.
#     """
#     if request.method == 'GET':
#         course = course_controller.track_course_progress(course_id, user_id)
#         return Response(course, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
