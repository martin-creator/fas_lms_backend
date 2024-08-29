from django.db.models import Count, Q
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer, ReactionSerializer, ShareSerializer
from django.utils import timezone

class ActivityQuery:
    # Category Queries
    @staticmethod
    def get_categories():
        """
        Get all categories.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return serializer.data
    
    @staticmethod
    def get_category(category_id):
        """
        Get a specific category.
        """
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return serializer.data
    
    @staticmethod
    def get_category_by_name(name):
        """
        Get a specific category by name.
        """
        category = Category.objects.get(name=name)
        serializer = CategorySerializer(category)
        return serializer.data
    
    @staticmethod
    def get_category_by_description(description):
        """
        Get a specific category by description.
        """
        category = Category.objects.get(description=description)
        serializer = CategorySerializer(category)
        return serializer.data
    
    @staticmethod
    def get_category_by_date_created(date_created):
        """
        Get a specific category by date created.
        """
        category = Category.objects.get(date_created=date_created)
        serializer = CategorySerializer(category)
        return serializer.data
    
    @staticmethod
    def get_category_by_id(category_id):
        """
        Get a specific category by id.
        """
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        return serializer.data
    

    # Attachment Queries
    @staticmethod
    def get_attachments():
        """
        Get all attachments.
        """
        attachments = Attachment.objects.all()
        serializer = AttachmentSerializer(attachments, many=True)
        return serializer.data
    
    @staticmethod
    def get_attachment(attachment_id):
        """
        Get a specific attachment.
        """
        attachment = Attachment.objects.get(id=attachment_id)
        serializer = AttachmentSerializer(attachment)
        return serializer.data
    
    @staticmethod
    def get_attachment_by_name(name):
        """
        Get a specific attachment by name.
        """
        attachment = Attachment.objects.get(name=name)
        serializer = AttachmentSerializer(attachment)
        return serializer.data
    

    # Marketing Campaign Queries
    @staticmethod
    def get_marketing_campaigns():
        """
        Get all marketing campaigns.
        """
        campaigns = MarketingCampaign.objects.all()
        serializer = MarketingCampaignSerializer(campaigns, many=True)
        return serializer.data
    
    @staticmethod
    def get_marketing_campaign(campaign_id):
        """
        Get a specific marketing campaign.
        """
        campaign = MarketingCampaign.objects.get(id=campaign_id)
        serializer = MarketingCampaignSerializer(campaign)
        return serializer.data
    
    @staticmethod
    def get_marketing_campaign_by_name(name):
        """
        Get a specific marketing campaign by name.
        """
        campaign = MarketingCampaign.objects.get(name=name)
        serializer = MarketingCampaignSerializer(campaign)
        return serializer.data
    

    # Learning Service Queries
    @staticmethod
    def get_learning_services():
        """
        Get all learning services.
        """
        services = LearningService.objects.all()
        serializer = LearningServiceSerializer(services, many=True)
        return serializer.data
    
    @staticmethod
    def get_learning_service(service_id):
        """
        Get a specific learning service.
        """
        service = LearningService.objects.get(id=service_id)
        serializer = LearningServiceSerializer(service)
        return serializer.data
    
    @staticmethod
    def get_learning_service_by_name(name):
        """
        Get a specific learning service by name.
        """
        service = LearningService.objects.get(name=name)
        serializer = LearningServiceSerializer(service)
        return serializer.data
    

    # Analytics Queries
    @staticmethod
    def get_analytics():
        """
        Get all analytics.
        """
        analytics = Analytics.objects.all()
        serializer = AnalyticsSerializer(analytics, many=True)
        return serializer.data
    
    @staticmethod
    def get_analytic(analytic_id):
        """
        Get a specific analytic.
        """
        analytic = Analytics.objects.get(id=analytic_id)
        serializer = AnalyticsSerializer(analytic)
        return serializer.data
    
    @staticmethod
    def get_analytic_by_name(name):
        """
        Get a specific analytic by name.
        """
        analytic = Analytics.objects.get(name=name)
        serializer = AnalyticsSerializer(analytic)
        return serializer.data
    

    # User Activity Queries
    @staticmethod
    def get_user_activities():
        """
        Get all user activities.
        """
        activities = UserActivity.objects.all()
        serializer = UserActivitySerializer(activities, many=True)
        return serializer.data
    
    @staticmethod
    def get_user_activity(activity_id):
        """
        Get a specific user activity.
        """
        activity = UserActivity.objects.get(id=activity_id)
        serializer = UserActivitySerializer(activity)
        return serializer.data
    
    @staticmethod
    def get_user_activity_by_user(user_id):
        """
        Get a specific user activity by user.
        """
        activity = UserActivity.objects.get(user=user_id)
        serializer = UserActivitySerializer(activity)
        return serializer.data
    
    @staticmethod
    def get_user_activity_by_date(date):
        """
        Get a specific user activity by date.
        """
        activity = UserActivity.objects.get(date=date)
        serializer = UserActivitySerializer(activity)
        return serializer.data
    

    # User Statistics Queries
    @staticmethod
    def get_user_statistics():
        """
        Get all user statistics.
        """
        statistics = UserStatistics.objects.all()
        serializer = UserStatisticsSerializer(statistics, many=True)
        return serializer.data
    
    @staticmethod
    def get_user_statistic(statistic_id):
        """
        Get a specific user statistic.
        """
        statistic = UserStatistics.objects.get(id=statistic_id)
        serializer = UserStatisticsSerializer(statistic)
        return serializer.data
    
    @staticmethod
    def get_user_statistic_by_user(user_id):
        """
        Get a specific user statistic by user.
        """
        statistic = UserStatistics.objects.get(user=user_id)
        serializer = UserStatisticsSerializer(statistic)
        return serializer.data
    
    @staticmethod
    def get_user_statistic_by_date(date):
        """
        Get a specific user statistic by date.
        """
        statistic = UserStatistics.objects.get(date=date)
        serializer = UserStatisticsSerializer(statistic)
        return serializer.data
    

    # Thread Queries
    @staticmethod
    def get_threads():
        """
        Get all threads.
        """
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return serializer.data
    
    @staticmethod
    def get_thread(thread_id):
        """
        Get a specific thread.
        """
        thread = Thread.objects.get(id=thread_id)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_title(title):
        """
        Get a specific thread by title.
        """
        thread = Thread.objects.get(title=title)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_date_created(date_created):
        """
        Get a specific thread by date created.
        """
        thread = Thread.objects.get(date_created=date_created)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_date_updated(date_updated):
        """
        Get a specific thread by date updated.
        """
        thread = Thread.objects.get(date_updated=date_updated)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_user(user_id):
        """
        Get a specific thread by user.
        """
        thread = Thread.objects.get(user=user_id)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_category(category_id):
        """
        Get a specific thread by category.
        """
        thread = Thread.objects.get(category=category_id)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_tags(tags):
        """
        Get a specific thread by tags.
        """
        thread = Thread.objects.get(tags=tags)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_views(views):
        """
        Get a specific thread by views.
        """
        thread = Thread.objects.get(views=views)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_replies(replies):
        """
        Get a specific thread by replies.
        """
        thread = Thread.objects.get(replies=replies)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_likes(likes):
        """
        Get a specific thread by likes.
        """
        thread = Thread.objects.get(likes=likes)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_dislikes(dislikes):
        """
        Get a specific thread by dislikes.
        """
        thread = Thread.objects.get(dislikes=dislikes)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_reports(reports):
        """
        Get a specific thread by reports.
        """
        thread = Thread.objects.get(reports=reports)
        serializer = ThreadSerializer(thread)
        return serializer.data
    
    @staticmethod
    def get_thread_by_status(status):
        """
        Get a specific thread by status.
        """
        thread = Thread.objects.get(status=status)
        serializer = ThreadSerializer(thread)
        return serializer.data
    

    # Reaction Queries
    @staticmethod
    def get_reactions():
        """
        Get all reactions.
        """
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True)
        return serializer.data
    
    @staticmethod
    def get_reaction(reaction_id):
        """
        Get a specific reaction.
        """
        reaction = Reaction.objects.get(id=reaction_id)
        serializer = ReactionSerializer(reaction)
        return serializer.data
    
    @staticmethod
    def get_reaction_by_user(user_id):
        """
        Get a specific reaction by user.
        """
        reaction = Reaction.objects.get(user=user_id)
        serializer = ReactionSerializer(reaction)
        return serializer.data
    
    @staticmethod
    def get_reaction_by_type(type):
        """
        Get a specific reaction by type.
        """
        reaction = Reaction.objects.get(type=type)
        serializer = ReactionSerializer(reaction)
        return serializer.data
    
    @staticmethod
    def get_reaction_by_date(date):
        """
        Get a specific reaction by date.
        """
        reaction = Reaction.objects.get(date=date)
        serializer = ReactionSerializer(reaction)
        return serializer.data
    

    # Share Queries
    @staticmethod
    def get_shares():
        """
        Get all shares.
        """
        shares = Share.objects.all()
        serializer = ShareSerializer(shares, many=True)
        return serializer.data
    
    @staticmethod
    def get_share(share_id):
        """
        Get a specific share.
        """
        share = Share.objects.get(id=share_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_user(user_id):
        """
        Get a specific share by user.
        """
        share = Share.objects.get(user=user_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_date(date):
        """
        Get a specific share by date.
        """
        share = Share.objects.get(date=date)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_content_type(content_type):
        """
        Get a specific share by content type.
        """
        share = Share.objects.get(content_type=content_type)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_object_id(object_id):
        """
        Get a specific share by object id.
        """
        share = Share.objects.get(object_id=object_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_content_object(content_object):
        """
        Get a specific share by content object.
        """
        share = Share.objects.get(content_object=content_object)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_attachment(attachment_id):
        """
        Get a specific share by attachment.
        """
        share = Share.objects.get(attachment=attachment_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_thread(thread_id):
        """
        Get a specific share by thread.
        """
        share = Share.objects.get(thread=thread_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_reaction(reaction_id):
        """
        Get a specific share by reaction.
        """
        share = Share.objects.get(reaction=reaction_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_report(report_id):
        """
        Get a specific share by report.
        """
        share = Share.objects.get(report=report_id)
        serializer = ShareSerializer(share)
        return serializer.data
    
    @staticmethod
    def get_share_by_status(status):
        """
        Get a specific share by status.
        """
        share = Share.objects.get(status=status)
        serializer = ShareSerializer(share)
        return serializer.data
    