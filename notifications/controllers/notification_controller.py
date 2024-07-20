from notifications.services.notification_service import NotificationService

class NotificationController:
    
    def __init__(self):
        self.notification_service = NotificationService()

    def create_notification(self, data):
        """
        Create a new notification.

        Args:
        - data (dict): Data for creating the notification.

        Returns:
        - Notification: The created Notification object.
        """
        return self.notification_service.send_notification(data)

    def get_notification(self, notification_id):
        """
        Retrieve a specific notification by its ID.

        Args:
        - notification_id (int): ID of the notification to retrieve.

        Returns:
        - dict: Serialized data of the notification.
        """
        return self.notification_service.get_notification(notification_id)

    def update_notification(self, notification_id, data):
        """
        Update an existing notification.

        Args:
        - notification_id (int): ID of the notification to update.
        - data (dict): Updated data for the notification.

        Returns:
        - dict: Serialized data of the updated notification.
        """
        return self.notification_service.update_notification(notification_id, data)

    def delete_notification(self, notification_id):
        """
        Delete a notification.

        Args:
        - notification_id (int): ID of the notification to delete.
        """
        self.notification_service.delete_notification(notification_id)

    def mark_notification_as_read(self, notification_id):
        """
        Mark a notification as read.

        Args:
        - notification_id (int): ID of the notification to mark as read.
        """
        self.notification_service.mark_notification_as_read(notification_id)

    def get_user_notifications(self, user_id):
        """
        Retrieve all notifications for a specific user.

        Args:
        - user_id (int): ID of the user to retrieve notifications for.

        Returns:
        - QuerySet: A queryset of notifications for the user.
        """
        return self.notification_service.get_user_notifications(user_id)

    def generate_user_report(self, user_id):
        """
        Generate a notification report for a specific user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - dict: The user notification report.
        """
        return self.notification_service.generate_user_report(user_id)

    def generate_summary_report(self):
        """
        Generate a summary report of notifications.

        Returns:
        - dict: The notification summary report.
        """
        return self.notification_service.generate_summary_report()

    def update_notification_settings(self, user_id, settings_data):
        """
        Update notification settings for a user.

        Args:
        - user_id (int): ID of the user.
        - settings_data (dict): Dictionary containing the settings to update.

        Returns:
        - dict: The updated settings.
        """
        return self.notification_service.update_notification_settings(user_id, settings_data)

    def get_notification_settings(self, user_id):
        """
        Get notification settings for a user.

        Args:
        - user_id (int): ID of the user.

        Returns:
        - dict: The user's notification settings.
        """
        return self.notification_service.get_notification_settings(user_id)
        
    def get_unread_notifications_count(self, user):
        """
        Retrieve the count of unread notifications for a user.

        Args:
        - user (User): The user to retrieve the unread notifications count for.

        Returns:
        - int: The count of unread notifications.
        """
        return self.notification_service.get_unread_notifications_count(user)

    def create_notification_template(self, notification_type, template):
        """
        Create or update a notification template for a notification type.

        Args:
        - notification_type (NotificationType): The type of notification.
        - template (str): The template content.

        Returns:
        - NotificationTemplate: The created or updated NotificationTemplate object.
        """
        return self.notification_service.create_notification_template(notification_type, template)

    def get_notification_template(self, notification_type):
        """
        Retrieve the notification template for a notification type.

        Args:
        - notification_type (NotificationType): The type of notification.

        Returns:
        - str: The template content.
        """
        return self.notification_service.get_notification_template(notification_type)

    def get_notification_types(self):
        """
        Retrieve all notification types available in the system.

        Returns:
        - QuerySet: A queryset of all notification types.
        """
        return self.notification_service.get_notification_types()

    def subscribe_to_notifications(self, user, notification_types):
        """
        Subscribe a user to receive notifications of specific types.

        Args:
        - user (User): The user to subscribe.
        - notification_types (list): List of NotificationType objects to subscribe to.
        """
        self.notification_service.subscribe_to_notifications(user, notification_types)

    def unsubscribe_from_notifications(self, user, notification_types):
        """
        Unsubscribe a user from receiving notifications of specific types.

        Args:
        - user (User): The user to unsubscribe.
        - notification_types (list): List of NotificationType objects to unsubscribe from.
        """
        self.notification_service.unsubscribe_from_notifications(user, notification_types)

    def notify_followers(self, user_profile, notification_type, content_object=None, content='', url=''):
        """
        Notify followers of a user profile about an action.

        Args:
        - user_profile (UserProfile): The user profile whose followers will be notified.
        - notification_type (NotificationType): The type of notification.
        - content_object (Model, optional): The object related to the notification.
        - content (str, optional): The content of the notification.
        - url (str, optional): The URL related to the notification.
        """
        self.notification_service.notify_followers(user_profile, notification_type, content_object, content, url)

    def notify_all_users(self, notification_type, content_object=None, content='', url=''):
        """
        Notify all users about an action.

        Args:
        - notification_type (NotificationType): The type of notification.
        - content_object (Model, optional): The object related to the notification.
        - content (str, optional): The content of the notification.
        - url (str, optional): The URL related to the notification.
        """
        self.notification_service.notify_all_users(notification_type, content_object, content, url)