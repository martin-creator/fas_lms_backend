from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from notifications.controllers.notification_controller import NotificationController

notification_controller = NotificationController()

@api_view(['POST'])
def create_notification(request):
    """
    Create a new notification.
    """
    notification_data = request.data
    try:
        notification = notification_controller.create_notification(notification_data)
        return Response(notification, status=status.HTTP_201_CREATED)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_notification(request, notification_id):
    """
    Retrieve a specific notification by its ID.
    """
    try:
        notification = notification_controller.get_notification(notification_id)
        return Response(notification, status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT', 'PATCH'])
def update_notification(request, notification_id):
    """
    Update an existing notification.
    """
    notification_data = request.data
    try:
        notification = notification_controller.update_notification(notification_id, notification_data)
        return Response(notification, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_notification(request, notification_id):
    """
    Delete a notification.
    """
    try:
        notification_controller.delete_notification(notification_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_notifications(request):
    """
    Retrieve all notifications for the authenticated user.
    """
    user = request.user  # Assuming authenticated user
    notifications = notification_controller.get_user_notifications(user.id)
    return Response(notifications, status=status.HTTP_200_OK)

@api_view(['POST'])
def mark_notification_as_read(request, notification_id):
    """
    Mark a notification as read.
    """
    try:
        notification_controller.mark_notification_as_read(notification_id)
        return Response(status=status.HTTP_200_OK)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def update_notification_settings(request):
    """
    Update notification settings for the authenticated user.
    """
    user = request.user  # Assuming authenticated user
    settings_data = request.data
    try:
        settings = notification_controller.update_notification_settings(user.id, settings_data)
        return Response(settings, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_notification_settings(request):
    """
    Retrieve notification settings for the authenticated user.
    """
    user = request.user  # Assuming authenticated user
    try:
        settings = notification_controller.get_notification_settings(user.id)
        return Response(settings, status=status.HTTP_200_OK)
    except NotificationSettings.DoesNotExist:
        return Response({"error": "Notification settings not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def generate_user_report(request, user_id):
    """
    Generate a notification report for a specific user.
    """
    try:
        report = notification_controller.generate_user_report(user_id)
        return Response(report, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def generate_summary_report(request):
    """
    Generate a summary report of notifications.
    """
    try:
        summary = notification_controller.generate_summary_report()
        return Response(summary, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@ratelimit(key='user', rate='5/m', method='POST', block=True)
def send_notification_view(request):
    # Logic to send notification
    pass



def manage_notification_preferences(request):
    # Endpoint to manage user notification preferences
    pass

def set_do_not_disturb_mode(request):
    # Endpoint to set user's Do Not Disturb mode
    pass