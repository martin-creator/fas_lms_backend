# notifications/reports/notification_report.py

from django.db.models import Count
from notifications.models import Notification

def generate_user_notification_report(user_id):
    """
    Generate a detailed notification report for a specific user.

    Args:
    - user_id (int): ID of the user.

    Returns:
    - dict: A dictionary containing the notification report for the user.
    """
    notifications = Notification.objects.filter(recipient_id=user_id).order_by('-timestamp')
    unread_count = notifications.filter(read=False).count()
    read_count = notifications.filter(read=True).count()
    total_count = notifications.count()
    
    report = {
        'user_id': user_id,
        'total_notifications': total_count,
        'unread_notifications': unread_count,
        'read_notifications': read_count,
        'notifications': list(notifications.values('id', 'message', 'read', 'timestamp'))
    }
    return report

def generate_notification_summary():
    """
    Generate a summary of notifications across all users.

    Returns:
    - dict: A dictionary containing the summary of notifications.
    """
    total_notifications = Notification.objects.count()
    unread_notifications = Notification.objects.filter(read=False).count()
    read_notifications = Notification.objects.filter(read=True).count()
    
    notifications_by_type = Notification.objects.values('notification_type').annotate(count=Count('id')).order_by('-count')
    
    summary = {
        'total_notifications': total_notifications,
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
        'notifications_by_type': list(notifications_by_type)
    }
    return summary
