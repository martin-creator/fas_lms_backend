from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from activity.models import UserActivity, Analytics, Category, Reaction, Share, Attachment
from activity.controllers.activity_controller import ActivityController

activity_controller = ActivityController()

@api_view(['GET'])
def get_user_activities(request):
    """
    Retrieve user activities.
    """
    user = request.user  # Assuming authenticated user
    activities = activity_controller.get_user_activities(user.id)
    return Response(activities, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_activity(request):
    """
    Create a new activity.
    """
    activity_data = request.data
    result = activity_controller.create_activity(request.user, activity_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'PATCH'])
def update_activity(request, id):
    """
    Update an activity.
    """
    activity_data = request.data
    result = activity_controller.update_activity(id, activity_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_activity(request, id):
    """
    Delete an activity.
    """
    result = activity_controller.delete_activity(id)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_activity_by_id(request, id):
    """
    Retrieve a specific activity by its ID.
    """
    result = activity_controller.get_activity_by_id(id)
    if "error" in result:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_activities_by_category(request, category_name):
    """
    Retrieve activities based on category.
    """
    activities = activity_controller.get_activities_by_category(category_name)
    return Response(activities, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_popular_categories(request):
    """
    Retrieve popular activity categories.
    """
    categories = activity_controller.get_popular_categories()
    return Response(categories, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_reaction(request):
    """
    Add a reaction to an activity.
    """
    user = request.user  # Assuming authenticated user
    activity_id = request.data.get('activity_id')
    reaction_type = request.data.get('reaction_type')
    result = activity_controller.add_reaction(user, activity_id, reaction_type)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def share_activity(request):
    """
    Share an activity with other users.
    """
    user = request.user  # Assuming authenticated user
    activity_id = request.data.get('activity_id')
    shared_to = request.data.get('shared_to')
    result = activity_controller.share_activity(user, activity_id, shared_to)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def add_attachment(request):
    """
    Add an attachment to an activity.
    """
    content_object = request.data.get('content_object')  # Assuming it's a reference to the content object
    attachment_data = request.data
    result = activity_controller.add_attachment(content_object, attachment_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_attachments_for_activity(request, activity_id):
    """
    Retrieve attachments for a specific activity.
    """
    result = activity_controller.get_attachments_for_activity(activity_id)
    if "error" in result:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def analyze_user_engagement(request):
    """
    Analyze user engagement based on activities.
    """
    user = request.user  # Assuming authenticated user
    result = activity_controller.analyze_user_engagement(user)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_trending_topics(request):
    """
    Retrieve trending topics based on analytics.
    """
    result = activity_controller.get_trending_topics()
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_activity_settings(request):
    """
    Retrieve activity settings.
    """
    settings = activity_controller.get_activity_settings()
    return Response(settings, status=status.HTTP_200_OK)

@api_view(['PUT', 'PATCH'])
def update_activity_settings(request):
    """
    Update activity settings.
    """
    settings_data = request.data
    result = activity_controller.update_activity_settings(settings_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def log_user_activity(request):
    """
    Log user activity across the platform.
    """
    user = request.user  # Assuming authenticated user
    activity_type = request.data.get('activity_type')
    details = request.data.get('details')
    categories = request.data.get('categories', None)
    result = activity_controller.log_user_activity(user, activity_type, details, categories)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def log_system_event(request):
    """
    Log system-wide events and interactions.
    """
    event_type = request.data.get('event_type')
    details = request.data.get('details')
    result = activity_controller.log_system_event(event_type, details)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def log_attachment(request):
    """
    Log attachments related to an object (post, message, etc.).
    """
    content_object = request.data.get('content_object')
    attachment_type = request.data.get('attachment_type')
    file = request.FILES.get('file')
    result = activity_controller.log_attachment(content_object, attachment_type, file)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_attachments_for_object(request, content_object):
    """
    Retrieve attachments related to a specific object.
    """
    result = activity_controller.get_attachments_for_object(content_object)
    if "error" in result:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def generate_user_activity_report(request, user_id):
    """
    Generate a report for user activities.
    """
    result = activity_controller.generate_user_activity_report(user_id)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def process_activity_data(request):
    """
    Process activity data before saving or updating.
    """
    activity_data = request.data
    result = activity_controller.process_activity_data(activity_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)