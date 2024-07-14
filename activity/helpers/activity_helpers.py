from django.core.exceptions import ValidationError
from activity.models import UserActivity, Category
from activity.serializers import CategorySerializer

class ActivityHelpers:

    @staticmethod
    def process_activity_data(activity_data):
        """
        Process and validate activity data before saving.
        """
        # Example validation: Ensure required fields are present
        if 'user_id' not in activity_data or 'activity_type' not in activity_data or 'details' not in activity_data:
            raise ValidationError("Missing required fields in activity data.")

        # Additional processing logic can be added here

    @staticmethod
    def validate_activity_permissions(user, activity):
        """
        Validate if the user has permissions for the activity.
        """
        if user != activity.user:
            raise PermissionError("You do not have permission to perform this action on the activity.")

    @staticmethod
    def get_or_create_category(name):
        """
        Get or create a category based on the name.
        """
        category, created = Category.objects.get_or_create(name=name)
        return category

    @staticmethod
    def format_category_data(category):
        """
        Format category data for display or serialization.
        """
        serializer = CategorySerializer(category)
        return serializer.data
    
    @staticmethod
    def format_activity_data(activity):
        """
        Format activity data for display.
        """
        # Implement formatting logic
        formatted_data = {
            'id': activity.id,
            'user': activity.user.username,
            'activity_type': activity.activity_type,
            'timestamp': activity.timestamp.isoformat(),
            'details': activity.details,
        }
        return formatted_data

    @staticmethod
    def validate_activity_data(activity_data):
        """
        Validate activity data before processing.
        """
        # Implement validation logic
        if not isinstance(activity_data, dict):
            raise TypeError("Activity data should be a dictionary.")
        required_fields = ['user', 'activity_type', 'details']
        for field in required_fields:
            if field not in activity_data:
                raise ValueError(f"Missing required field: {field}")
        return True
