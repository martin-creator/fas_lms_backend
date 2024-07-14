from django.db.models import Count
from activity.models import UserActivity, Category
from activity.serializers import UserActivitySerializer, CategorySerializer

class ActivityReport:

    @staticmethod
    def generate_user_activity_report(user_id):
        """
        Generate a report of user activities.
        """
        activities = UserActivity.objects.filter(user_id=user_id).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def generate_activity_summary():
        """
        Generate a summary of activities.
        """
        activity_summary = {
            'total_activities': UserActivity.objects.count(),
            'total_categories': Category.objects.count(),
            'popular_categories': ActivityReport._get_popular_categories_summary(),
        }
        return activity_summary

    @staticmethod
    def _get_popular_categories_summary():
        """
        Get a summary of popular activity categories.
        """
        popular_categories = Category.objects.annotate(num_activities=Count('user_activity_categories')).order_by('-num_activities')[:5]
        serializer = CategorySerializer(popular_categories, many=True)
        return serializer.data
