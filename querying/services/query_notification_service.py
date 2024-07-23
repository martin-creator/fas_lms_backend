# services/query_notification_service.py
from notifications.services.notification_service import NotificationService
from utils.logging import Logger
from notifications.models import NotificationType
from profiles.models import UserProfile

class QueryNotificationService:
    def __init__(self):
        self.logger = Logger()
        self.notification_service = NotificationService()

    def notify_admins(self, message):
        """
        Notify administrators of critical errors.
        """
        try:
            admin_users = UserProfile.objects.filter(user__is_staff=True)
            notification_type, created = NotificationType.objects.get_or_create(type_name='critical_error')
            notifications = []
            for admin in admin_users:
                notification_data = {
                    'recipient': admin.user.id,
                    'notification_type': notification_type.id,
                    'content': message,
                    'url': '/admin/notifications/'
                }
                notification = self.notification_service.send_notification(notification_data)
                notifications.append(notification)
            self.logger.info(f"Sent notifications to admins: {notifications}")
        except Exception as e:
            self.logger.error(f"Failed to notify admins: {str(e)}")
            raise ValueError(f"Failed to notify admins: {str(e)}")

    def notify_user(self, user, notification_type, content, url=''):
        """
        Notify a specific user.

        Args:
        - user (User): The user to notify.
        - notification_type (str): The type of notification to send.
        - content (str): The content of the notification.
        - url (str): The URL related to the notification.
        """
        try:
            notification_type_obj, created = NotificationType.objects.get_or_create(type_name=notification_type)
            notification_data = {
                'recipient': user.id,
                'notification_type': notification_type_obj.id,
                'content': content,
                'url': url
            }
            notification = self.notification_service.send_notification(notification_data)
            self.logger.info(f"Sent notification to user {user.username}: {notification}")
        except Exception as e:
            self.logger.error(f"Failed to notify user {user.username}: {str(e)}")
            raise ValueError(f"Failed to notify user {user.username}: {str(e)}")

    def notify_all_users(self, notification_type, content, url=''):
        """
        Notify all users.

        Args:
        - notification_type (str): The type of notification to send.
        - content (str): The content of the notification.
        - url (str): The URL related to the notification.
        """
        try:
            notification_type_obj, created = NotificationType.objects.get_or_create(type_name=notification_type)
            all_users = UserProfile.objects.all()
            notifications = []
            for user_profile in all_users:
                notification_data = {
                    'recipient': user_profile.user.id,
                    'notification_type': notification_type_obj.id,
                    'content': content,
                    'url': url
                }
                notification = self.notification_service.send_notification(notification_data)
                notifications.append(notification)
            self.logger.info(f"Sent notifications to all users: {notifications}")
        except Exception as e:
            self.logger.error(f"Failed to notify all users: {str(e)}")
            raise ValueError(f"Failed to notify all users: {str(e)}")

    def notify_followers(self, user_profile, notification_type, content_object=None, content='', url=''):
        """
        Notifies followers of a user profile about an action.

        Args:
        - user_profile (UserProfile): The user profile whose followers are to be notified.
        - notification_type (str): The type of notification to create.
        - content_object (Model): The content object related to the notification.
        - content (str): The notification content.
        - url (str): The URL related to the notification.
        """
        try:
            notification_type_obj, created = NotificationType.objects.get_or_create(type_name=notification_type)
            followers = user_profile.followers.all()
            notifications = []
            for follower in followers:
                notification_data = {
                    'recipient': follower.user.id,
                    'notification_type': notification_type_obj.id,
                    'content': content,
                    'url': url
                }
                notification = self.notification_service.send_notification(notification_data)
                notifications.append(notification)
            self.logger.info(f"Sent notifications to followers of {user_profile.user.username}: {notifications}")
        except Exception as e:
            self.logger.error(f"Failed to notify followers of {user_profile.user.username}: {str(e)}")
            raise ValueError(f"Failed to notify followers of {user_profile.user.username}: {str(e)}")

    def generate_user_report(self, user_id):
        """
        Generate a notification report for a specific user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - dict: The user notification report.
        """
        try:
            report = self.notification_service.generate_user_report(user_id)
            self.logger.info(f"Generated notification report for user {user_id}")
            return report
        except Exception as e:
            self.logger.error(f"Failed to generate notification report for user {user_id}: {str(e)}")
            raise ValueError(f"Failed to generate notification report for user {user_id}: {str(e)}")

    def generate_summary_report(self):
        """
        Generate a summary report of notifications.

        Returns:
        - dict: The notification summary report.
        """
        try:
            report = self.notification_service.generate_summary_report()
            self.logger.info(f"Generated summary notification report")
            return report
        except Exception as e:
            self.logger.error(f"Failed to generate summary notification report: {str(e)}")
            raise ValueError(f"Failed to generate summary notification report: {str(e)}")
