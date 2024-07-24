from django.core.exceptions import ValidationError
from notifications.utils.delivery_method import DeliveryMethod
from notifications.settings.config.constances import SEVERITY_CHOICES



class ActionChecker:
    @staticmethod
    def update_priority(notification, new_priority):
        """
        Update the priority of the notification.

        Args:
            notification (Notification): The notification instance to update.
            new_priority (int): The new priority value to set.

        Raises:
            ValueError: If the priority value is invalid.
        """
        ActionChecker.validate_priority(new_priority)
        notification.priority = new_priority
        notification.save()

    @staticmethod
    def add_share(notification, share):
        """
        Add a share to the notification.

        Args:
            notification (Notification): The notification instance to update.
            share (Share): The share to add.
        """
        notification.shares.add(share)
        notification.save()

    @staticmethod
    def update_html_content(notification, new_html_content):
        """
        Update the HTML content of the notification.

        Args:
            notification (Notification): The notification instance to update.
            new_html_content (str): The new HTML content to set.
        """
        notification.html_content = new_html_content
        notification.save()

    @staticmethod
    def validate_priority(priority):
        """
        Validate the priority value.

        Args:
            priority (int): The priority value to validate.

        Raises:
            ValueError: If the priority value is invalid.
        """
        if not isinstance(priority, int) or priority < 1:
            raise ValueError("Priority must be a positive integer.")
    
    @staticmethod
    def update_delivery_method(notification, new_delivery_method):
        """
        Update the delivery method of the notification.

        Args:
            notification (Notification): The notification instance to update.
            new_delivery_method (str): The new delivery method to set.
        
        Raises:
            ValueError: If the delivery method is invalid.
        """
        if new_delivery_method not in dict(DeliveryMethod.choices):
            raise ValueError("Invalid delivery method.")
        notification.delivery_method = new_delivery_method
        notification.save()
    
    @staticmethod
    def update_severity(notification, new_severity):
        """
        Update the severity of the notification.

        Args:
            notification (Notification): The notification instance to update.
            new_severity (str): The new severity level to set.
        
        Raises:
            ValueError: If the severity level is invalid.
        """
        if new_severity not in dict(SEVERITY_CHOICES):
            raise ValueError("Invalid severity level.")
        notification.severity = new_severity
        notification.save()
    
    @staticmethod
    def update_notification_type(notification, new_notification_type):
        """
        Update the notification type of the notification.

        Args:
            notification (Notification): The notification instance to update.
            new_notification_type (NotificationType): The new notification type to set.
        
        Raises:
            ValueError: If the notification type is invalid.
        """
        from notifications.models import NotificationType
        if not isinstance(new_notification_type, NotificationType):
            raise ValueError("Invalid notification type.")
        notification.notification_type = new_notification_type
        notification.save()
