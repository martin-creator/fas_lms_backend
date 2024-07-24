from django.contrib.auth import get_user_model

User = get_user_model()

class UserUtils:
    """
    Utility functions related to users.
    """
    @staticmethod
    def get_current_user(user_id):
        """
        Get the current user.
        """
        return User.objects.get(id=user_id)