from activity.models import UserActivity, Reaction, Share
from django.db.models import Q

class StatsUtils:

    @staticmethod
    def calculate_engagement_rate(user):
        """
        Calculate the engagement rate for a user.
        
        Args:
            user (User): The user to calculate the engagement rate for.
            
        Returns:
            float: The engagement rate.
        """
        posts_count = UserActivity.objects.filter(user=user, activity_type='post').count()
        reactions_count = Reaction.objects.filter(user=user).count()
        shares_count = Share.objects.filter(user=user).count()

        if posts_count + reactions_count + shares_count == 0:
            return 0

        engagement_rate = (posts_count + reactions_count + shares_count) / 3  # Example calculation
        return engagement_rate
    
    @staticmethod
    def generate_activity_statistics(activity):
        """
        Generate statistics for a specific activity.
        
        Args:
            activity (UserActivity): The activity to generate statistics for.
            
        Returns:
            dict: A dictionary containing activity statistics.
        """
        reactions_count = Reaction.objects.filter(
            Q(message__activity=activity) |
            Q(post__activity=activity) |
            Q(comment__activity=activity) |
            Q(job_post__activity=activity) |
            Q(group__activity=activity)
        ).count()

        shares_count = Share.objects.filter(content_type=ContentType.objects.get_for_model(activity), object_id=activity.id).count()

        return {
            'reactions_count': reactions_count,
            'shares_count': shares_count,
        }
