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