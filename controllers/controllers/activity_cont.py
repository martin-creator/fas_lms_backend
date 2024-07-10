# controllers/activity_controller.py
from django.db.models import Count, Q
from activity.models import UserActivity, Analytics, Category, Reaction, Share, Attachment


class ActivityManagementController:
    def log_user_activity(self, user, activity_type, details, categories=None):
        """
        Log user activity across the platform.
        """
        if categories is None:
            categories = []
        
        activity = UserActivity.objects.create(
            user=user,
            activity_type=activity_type,
            details=details
        )
        activity.categories.add(*categories)
        return activity

    def log_system_event(self, event_type, details):
        """
        Log system-wide events and interactions.
        """
        # Implement system event logging logic here
        pass

    def get_user_activities(self, user):
        """
        Retrieve user activity logs.
        """
        return UserActivity.objects.filter(user=user).order_by('-timestamp')

    def get_activities_by_category(self, category_name):
        """
        Retrieve activities based on category.
        """
        return UserActivity.objects.filter(categories__name=category_name).order_by('-timestamp')

    def get_popular_categories(self):
        """
        Retrieve popular activity categories.
        """
        return Category.objects.annotate(num_activities=Count('user_activity_categories')).order_by('-num_activities')

    def analyze_user_engagement(self, user):
        """
        Analyze user engagement based on activities.
        """
        posts_count = UserActivity.objects.filter(user=user, activity_type='post').count()
        reactions_count = Reaction.objects.filter(user=user).count()
        shares_count = Share.objects.filter(user=user).count()

        engagement_rate = (posts_count + reactions_count + shares_count) / 3  # Example calculation

        return {
            'posts_count': posts_count,
            'reactions_count': reactions_count,
            'shares_count': shares_count,
            'engagement_rate': engagement_rate
        }

    def get_trending_topics(self):
        """
        Retrieve trending topics based on analytics.
        """
        return Analytics.objects.order_by('-engagement_rate').values_list('trending_topics', flat=True)[:5]

    def log_attachment(self, content_object, attachment_type, file):
        """
        Log attachments related to an object (post, message, etc.).
        """
        attachment = Attachment.objects.create(
            content_object=content_object,
            attachment_type=attachment_type,
            file=file
        )
        return attachment

    def get_attachments_for_object(self, content_object):
        """
        Retrieve attachments related to a specific object.
        """
        return Attachment.objects.filter(content_object=content_object)

    def get_user_statistics(self, user):
        """
        Retrieve statistics for a user.
        """
        # Example: Fetch or calculate user statistics
        return {
            'connections_count': 10,  # Example data
            'posts_count': 20,
            'engagement_rate': 0.75
        }
