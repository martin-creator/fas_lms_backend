from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from activity.models import UserActivity, Analytics, Category, Reaction, Share, Attachment
from activity.controllers.activity_controller import ActivityController

@api_view(['GET'])
def get_user_activities(request):
    """
    Retrieve user activities.
    """
    user = request.user  # Assuming authenticated user
    activities = ActivityController.get_user_activities(user.id)
    return Response(activities, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_activity(request):
    """
    Create a new activity.
    """
    activity_data = request.data
    result = ActivityController.create_activity(request.user, activity_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_201_CREATED)

@api_view(['PUT', 'PATCH'])
def update_activity(request, id):
    """
    Update an activity.
    """
    activity_data = request.data
    result = ActivityController.update_activity(id, activity_data)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_activity(request, id):
    """
    Delete an activity.
    """
    result = ActivityController.delete_activity(id)
    if "error" in result:
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    return Response(result, status=status.HTTP_204_NO_CONTENT)
