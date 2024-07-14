class PermissionUtils:

    @staticmethod
    def check_user_permission(user, action, activity):
        """
        Check if a user has permission to perform an action on an activity.
        
        Args:
            user (User): The user to check.
            action (str): The action to check (e.g., 'edit', 'delete').
            activity (UserActivity): The activity to check against.
            
        Returns:
            bool: True if the user has permission, False otherwise.
        """
        # Implement the logic to check permissions
        return True  # Example return
