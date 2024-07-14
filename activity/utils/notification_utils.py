class NotificationUtils:

    @staticmethod
    def send_activity_notification(user, activity):
        """
        Send a notification to a user about an activity.
        
        Args:
            user (User): The user to notify.
            activity (UserActivity): The activity to notify about.
            
        Returns:
            None
        """
        # Implement the logic to send a notification
        pass
    
    @staticmethod
    def send_bulk_notifications(users, activity):
        """
        Send notifications to multiple users about an activity.
        
        Args:
            users (list): The list of users to notify.
            activity (UserActivity): The activity to notify about.
            
        Returns:
            None
        """
        for user in users:
            NotificationUtils.send_activity_notification(user, activity)
