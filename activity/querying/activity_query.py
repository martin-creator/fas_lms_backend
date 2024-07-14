from django.db.models import Count
from activity.models import UserActivity, Reaction, Share, Attachment, Category
from activity.serializers import UserActivitySerializer, ReactionSerializer, ShareSerializer, AttachmentSerializer, CategorySerializer

class ActivityQuery:

    @staticmethod
    def get_activities_by_user(user_id):
        """
        Retrieve activities for a specific user.
        """
        activities = UserActivity.objects.filter(user_id=user_id).order_by('-timestamp')
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data

    @staticmethod
    def search_activities(query):
        """
        Search activities based on a query string.
        """
        activities = UserActivity.objects.filter(details__icontains=query).order_by('-timestamp')
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
    def get_reactions_for_activity(activity_id):
        """
        Retrieve reactions for a specific activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            reactions = Reaction.objects.filter(activity=activity)
            serializer = ReactionSerializer(reactions, many=True)
            return serializer.data
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}

    @staticmethod
    def get_shares_for_activity(activity_id):
        """
        Retrieve shares for a specific activity.
        """
        try:
            activity = UserActivity.objects.get(id=activity_id)
            shares = Share.objects.filter(content_object=activity)
            serializer = ShareSerializer(shares, many=True)
            return serializer.data
        except UserActivity.DoesNotExist:
            return {"error": "Activity not found."}
