from django.db.models import Q
from activity.models import UserActivity

class SearchUtils:

    @staticmethod
    def search_activities(query):
        """
        Search activities based on a query.
        
        Args:
            query (str): The search query.
            
        Returns:
            QuerySet: A queryset of matching activities.
        """
        return UserActivity.objects.filter(
            Q(activity_type__icontains=query) |
            Q(details__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
