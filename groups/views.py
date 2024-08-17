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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)4
    


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
    
