from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from activity.models import (
    UserActivity,
    Analytics,
    Category,
    Reaction,
    Share,
    Attachment,
    UserStatistics,
    MarketingCampaign,
    LearningService,
    Activity,
)
from activity.serializers import (
    UserActivitySerializer,
    AnalyticsSerializer,
    CategorySerializer,
    ReactionSerializer,
    ShareSerializer,
    AttachmentSerializer,
)
from activity.utils import (
    NotificationUtils,
    PermissionUtils,
    SearchUtils,
    DateTimeUtils,
    FileUtils,
    StatsUtils,
    ActivityValidators,
    ActivityConstants,
)
from activity.services.activity_services import ActivityService
from activity.querying.activity_query import ActivityQuery
from activity.reports.activity_report import ActivityReport
from activity.settings.activity_settings import ActivitySettings

class ActivityService:

    @staticmethod
    def create_activity(user, activity_data):
        """
        Create a new activity.
        """
        serializer = UserActivitySerializer(data=activity_data)
        if serializer.is_valid():
            activity = serializer.save(user=user)
            NotificationUtils.send_notification(user, 'New activity created', activity.details)
            return serializer.data
        return serializer.errors

    @staticmethod
    def update_activity(activity_id, activity_data):
        """
        Update an existing activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

        serializer = UserActivitySerializer(instance=activity, data=activity_data, partial=True)
        if serializer.is_valid():
            updated_activity = serializer.save()
            NotificationUtils.send_notification(updated_activity.user, 'Activity updated', updated_activity.details)
            return serializer.data
        return serializer.errors

    @staticmethod
    def delete_activity(activity_id):
        """
        Delete an activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            if not PermissionUtils.check_user_permissions(activity.user, 'delete_activity'):
                return {"error": "Permission denied."}
            activity.delete()
            return {"message": "Activity deleted successfully."}
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def get_user_activities(user_id):
        """
        Retrieve activities for a specific user.
        """
        activities = UserActivity.objects.filter(user_id=user_id).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def get_activity_by_id(activity_id):
        """
        Retrieve a specific activity by its ID.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            serializer = UserActivitySerializer(activity)
            return serializer.data
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def get_activities_by_category(category_name):
        """
        Retrieve activities based on category.
        """
        activities = UserActivity.objects.filter(categories__name=category_name).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def get_popular_categories():
        """
        Retrieve popular activity categories.
        """
        categories = Category.objects.annotate(num_activities=Count('user_activity_categories')).order_by('-num_activities')
        serializer = CategorySerializer(categories, many=True)
        return serializer.data

    @staticmethod
    def add_reaction(user, activity_id, reaction_type):
        """
        Add a reaction to an activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            reaction, created = Reaction.objects.get_or_create(user=user, activity=activity, type=reaction_type)
            if created:
                activity.reactions.add(reaction)
                return ReactionSerializer(reaction).data
            else:
                return {"error": "Reaction already exists."}
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def share_activity(user, activity_id, shared_to):
        """
        Share an activity with other users.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            share = Share.objects.create(user=user, content_object=activity)
            share.shared_to.add(*shared_to)
            return ShareSerializer(share).data
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def add_attachment(content_object, attachment_data):
        """
        Add an attachment to an activity.
        """
        serializer = AttachmentSerializer(data=attachment_data)
        if serializer.is_valid():
            attachment = serializer.save(content_object=content_object)
            return serializer.data
        return serializer.errors

    @staticmethod
    def get_attachments_for_activity(activity_id):
        """
        Retrieve attachments for a specific activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            attachments = Attachment.objects.filter(content_object=activity)
            serializer = AttachmentSerializer(attachments, many=True)
            return serializer.data
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def analyze_user_engagement(user):
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
        
    @staticmethod
    def log_user_activity(user, activity_type, details, categories=None):
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

    @staticmethod
    def log_system_event(event_type, details):
        """
        Log system-wide events and interactions.
        """
        # Implement system event logging logic here
        pass

    @staticmethod
    def get_user_activities(user):
        """
        Retrieve user activity logs.
        """
        activities = UserActivity.objects.filter(user=user).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def get_activities_by_category(category_name):
        """
        Retrieve activities based on category.
        """
        activities = UserActivity.objects.filter(categories__name=category_name).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def get_popular_categories():
        """
        Retrieve popular activity categories.
        """
        categories = Category.objects.annotate(num_activities=Count('user_activity_categories')).order_by('-num_activities')
        serializer = CategorySerializer(categories, many=True)
        return serializer.data

    @staticmethod
    def analyze_user_engagement(user):
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

    @staticmethod
    def get_trending_topics():
        """
        Retrieve trending topics based on analytics.
        """
        trending_topics = Analytics.objects.order_by('-engagement_rate').values_list('trending_topics', flat=True)[:5]
        return list(trending_topics)

    @staticmethod
    def log_attachment(content_object, attachment_type, file):
        """
        Log attachments related to an object (post, message, etc.).
        """
        attachment = Attachment.objects.create(
            content_object=content_object,
            attachment_type=attachment_type,
            file=file
        )
        return attachment

    @staticmethod
    def get_attachments_for_object(content_object):
        """
        Retrieve attachments related to a specific object.
        """
        attachments = Attachment.objects.filter(content_object=content_object)
        serializer = AttachmentSerializer(attachments, many=True)
        return serializer.data
