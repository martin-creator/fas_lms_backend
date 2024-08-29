from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer, ReactionSerializer, ShareSerializer
from activity.querying.activity_query import ActivityQuery



class ActivityReport:
    # Report for all categories
    @staticmethod
    def get_categories_report():
        """
        Get a report for all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return serializer.data
    
    # Report for all attachments
    @staticmethod
    def get_attachments_report():
        """
        Get a report for all attachments.
        """
        attachments = Attachment.objects.all()
        serializer = AttachmentSerializer(attachments, many=True)
        return serializer.data
    
    # Report for all marketing campaigns
    @staticmethod
    def get_marketing_campaigns_report():
        """
        Get a report for all marketing campaigns.
        """
        marketing_campaigns = MarketingCampaign.objects.all()
        serializer = MarketingCampaignSerializer(marketing_campaigns, many=True)
        return serializer.data
    
    # Report for all learning services
    @staticmethod
    def get_learning_services_report():
        """
        Get a report for all learning services.
        """
        learning_services = LearningService.objects.all()
        serializer = LearningServiceSerializer(learning_services, many=True)
        return serializer.data
    
    # Report for all analytics
    @staticmethod
    def get_analytics_report():
        """
        Get a report for all analytics.
        """
        analytics = Analytics.objects.all()
        serializer = AnalyticsSerializer(analytics, many=True)
        return serializer.data
    
    # Report for all user activities
    @staticmethod
    def get_user_activities_report():
        """
        Get a report for all user activities.
        """
        user_activities = UserActivity.objects.all()
        serializer = UserActivitySerializer(user_activities, many=True)
        return serializer.data
    
    # Report for all user statistics
    @staticmethod
    def get_user_statistics_report():
        """
        Get a report for all user statistics.
        """
        user_statistics = UserStatistics.objects.all()
        serializer = UserStatisticsSerializer(user_statistics, many=True)
        return serializer.data
    
    # Report for all threads
    @staticmethod
    def get_threads_report():
        """
        Get a report for all threads.
        """
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return serializer.data
    
    # Report for all reactions
    @staticmethod
    def get_reactions_report():
        """
        Get a report for all reactions.
        """
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return serializer.data
    
    # Report for all shares
    @staticmethod
    def get_shares_report():
        """
        Get a report for all shares.
        """
        shares = Share.objects.all()
        serializer = ShareSerializer(shares, many=True)
        return serializer.data
    
    # Report for all reactions by user
    @staticmethod
    def get_reactions_by_user_report(user):
        """
        Get a report for all reactions by a specific user.
        """
        reactions = Reaction.objects.filter(user=user)
        serializer = ReactionSerializer(reactions, many=True)
        return serializer.data
    
    # Report for all shares by user
    @staticmethod
    def get_shares_by_user_report(user):
        """
        Get a report for all shares by a specific user.
        """
        shares = Share.objects.filter(user=user)
        serializer = ShareSerializer(shares, many=True)
        return serializer.data
    
    # Report for all reactions by post
    @staticmethod
    def get_reactions_by_post_report(post):
        """
        Get a report for all reactions by a specific post.
        """
        reactions = Reaction.objects.filter(post=post)
        serializer = ReactionSerializer(reactions, many=True)
        return serializer.data
    
    # Report for all shares by post
    @staticmethod
    def get_shares_by_post_report(post):
        """
        Get a report for all shares by a specific post.
        """
        shares = Share.objects.filter(post=post)
        serializer = ShareSerializer(shares, many=True)
        return serializer.data
    

