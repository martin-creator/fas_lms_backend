import logging
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class ProfilePermissionChecker:
    """
    Service for managing permissions related to profiles within the application.
    """

    @staticmethod
    def user_can_follow(user):
        """
        Check if the user has permission to follow other users.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('profiles.can_follow')

    @staticmethod
    def user_can_endorse(user):
        """
        Check if the user has permission to endorse skills.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('profiles.can_endorse')

    @staticmethod
    def user_can_manage_experience(user):
        """
        Check if the user has permission to manage experiences.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('profiles.can_manage_experience')

    @staticmethod
    def user_can_manage_education(user):
        """
        Check if the user has permission to manage education.

        Args:
            user (User): The user to check.

        Returns:
            bool: True if the user has the permission, False otherwise.
        """
        return user.has_perm('profiles.can_manage_education')

    @staticmethod
    def check_permission_for_action(user, action):
        """
        Check if the user has permission to perform the specified action on a profile.

        Args:
            user (User): The user performing the action.
            action (str): The action to perform (e.g., 'follow', 'endorse_skill', 'add_experience').

        Raises:
            PermissionDenied: If the user does not have permission for the action.
        """
        if action in ['follow', 'unfollow', 'is_following', 'has_follow_request', 'accept_follow_request', 'reject_follow_request']:
            if not ProfilePermissionChecker.user_can_follow(user):
                raise PermissionDenied(f"You do not have permission to {action.replace('_', ' ')}.")
        elif action in ['endorse_skill', 'has_endorsed']:
            if not ProfilePermissionChecker.user_can_endorse(user):
                raise PermissionDenied(f"You do not have permission to {action.replace('_', ' ')}.")
        elif action in ['add_experience', 'remove_experience']:
            if not ProfilePermissionChecker.user_can_manage_experience(user):
                raise PermissionDenied(f"You do not have permission to {action.replace('_', ' ')}.")
        elif action in ['add_education', 'remove_education']:
            if not ProfilePermissionChecker.user_can_manage_education(user):
                raise PermissionDenied(f"You do not have permission to {action.replace('_', ' ')}.")
        else:
            raise ValueError(f"Unknown action: {action}")