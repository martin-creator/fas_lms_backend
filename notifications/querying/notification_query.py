# notifications/querying/notification_query.py

from django.db.models import Q
from django.apps import apps

class NotificationQueryService:
    @staticmethod
    def get_notifications_by_user(user_id, read_status=None):
        """
        Fetch notifications for a specific user.
        """
        Notification = apps.get_model('notifications', 'Notification')  # Use apps.get_model to avoid circular imports
        query = Notification.objects.by_user(user_id)
        if read_status is not None:
            query = query.filter(is_read=read_status)
        return query.order_by('-timestamp')

    @staticmethod
    def search_notifications(user_id, query):
        """
        Search notifications for a user based on a query string.
        """
        Notification = apps.get_model('notifications', 'Notification')  # Use apps.get_model to avoid circular imports
        search_query = Q(message__icontains=query) | Q(additional_data__icontains=query)
        return Notification.objects.by_user(user_id).filter(search_query).order_by('-timestamp')

    @staticmethod
    def get_unread_notifications_count(user_id):
        """
        Get the count of unread notifications for a user.
        """
        Notification = apps.get_model('notifications', 'Notification')  # Use apps.get_model to avoid circular imports
        return Notification.objects.by_user(user_id).unread().count()

    @staticmethod
    def get_notifications_by_type(user_id, notification_type):
        """
        Fetch notifications for a user filtered by type.
        """
        Notification = apps.get_model('notifications', 'Notification')  # Use apps.get_model to avoid circular imports
        return Notification.objects.by_user(user_id).filter(notification_type=notification_type).order_by('-timestamp')
