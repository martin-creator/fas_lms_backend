# notifications/querying/notification_query.py

from django.db.models import Q
from notifications.models import Notification

def get_notifications_by_user(user_id, read_status=None):
    """
    Fetch notifications for a specific user.

    Args:
    - user_id (int): ID of the user.
    - read_status (bool, optional): Filter by read/unread status. None means no filter.

    Returns:
    - QuerySet: A QuerySet of notifications for the user.
    """
    query = Notification.objects.filter(recipient_id=user_id)
    if read_status is not None:
        query = query.filter(read=read_status)
    return query.order_by('-timestamp')

def search_notifications(user_id, query):
    """
    Search notifications for a user based on a query string.

    Args:
    - user_id (int): ID of the user.
    - query (str): Search query string.

    Returns:
    - QuerySet: A QuerySet of notifications matching the search query.
    """
    search_query = Q(message__icontains=query) | Q(additional_data__icontains=query)
    return Notification.objects.filter(recipient_id=user_id).filter(search_query).order_by('-timestamp')

def get_unread_notifications_count(user_id):
    """
    Get the count of unread notifications for a user.

    Args:
    - user_id (int): ID of the user.

    Returns:
    - int: Number of unread notifications.
    """
    return Notification.objects.filter(recipient_id=user_id, read=False).count()

def get_notifications_by_type(user_id, notification_type):
    """
    Fetch notifications for a user filtered by type.

    Args:
    - user_id (int): ID of the user.
    - notification_type (str): Type of the notification.

    Returns:
    - QuerySet: A QuerySet of notifications of the specified type for the user.
    """
    return Notification.objects.filter(recipient_id=user_id, notification_type=notification_type).order_by('-timestamp')
