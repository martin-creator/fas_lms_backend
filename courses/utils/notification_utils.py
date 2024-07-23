# utils/notification_utils.py 

from notifications.services.notification_service import NotificationService
from notifications.models import NotificationType
from django.contrib.auth.models import User

class NotificationUtils:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_or_create_notification_type(self, type_name):
        """
        Get or create a notification type.
        """
        try:
            notification_type, created = NotificationType.objects.get_or_create(type_name=type_name)
            return notification_type
        except Exception as e:
            raise ValueError(f"Failed to get or create notification type: {str(e)}")

    def send_notification(self, user, notification_type_name, content, url=''):
        """
        Send a notification to a specific user.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            notification_data = {
                'recipient': user.id,
                'notification_type': notification_type.id,
                'content': content,
                'url': url
            }
            self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to send notification to user {user.username}: {str(e)}")

    def notify_all_users(self, notification_type_name, content, url=''):
        """
        Notify all users.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            users = User.objects.all()
            for user in users:
                notification_data = {
                    'recipient': user.id,
                    'notification_type': notification_type.id,
                    'content': content,
                    'url': url
                }
                self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to notify all users: {str(e)}")

    def notify_admins(self, notification_type_name, content, url=''):
        """
        Notify all admin users.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                notification_data = {
                    'recipient': admin.id,
                    'notification_type': notification_type.id,
                    'content': content,
                    'url': url
                }
                self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to notify admins: {str(e)}")
