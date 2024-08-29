from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer, ReactionSerializer, ShareSerializer
from activity.querying.activity_query import ActivityQuery
from activity.helpers.activity_helpers import ActivityHelpers
from activity.reports.activity_report import ActivityReport
from activity.settings.activity_settings import ActivitySettings
from activity.utils import UserUtils, DateTimeUtils


class ActivityService:
    # Category Services
    @staticmethod
    def get_categories():
        """
        Get all categories.
        """
        categories = ActivityQuery.get_categories()
        return categories
    
    @staticmethod
    def get_category(category_id):
        """
        Get a specific category.
        """
        category = ActivityQuery.get_category(category_id)
        return category
    
    @staticmethod
    def create_category(category_data):
        """
        Create a new category.
        """
        category = ActivityHelpers.process_category_data(category_data)
        category.save()
        serializer = CategorySerializer(category)
        return serializer.data
    

    @staticmethod
    def update_category(category_id, category_data):
        """
        Update a category.
        """
        category = ActivityQuery.get_category(category_id)
        category = ActivityHelpers.process_category_update_data(category, category_data)
        category.save()
        serializer = CategorySerializer(category)
        return serializer.data
    

    @staticmethod
    def delete_category(category_id):
        """
        Delete a category.
        """
        category = ActivityQuery.get_category(category_id)
        category.delete()
        return True
    

    @staticmethod
    def delete_all_categories():
        """
        Delete all categories.
        """
        categories = ActivityQuery.get_categories()
        categories.delete()
        return True
    

    # Attachment Services
    @staticmethod
    def get_attachments():
        """
        Get all attachments.
        """
        attachments = ActivityQuery.get_attachments()
        return attachments
    
    @staticmethod
    def get_attachment(attachment_id):
        """
        Get a specific attachment.
        """
        attachment = ActivityQuery.get_attachment(attachment_id)
        return attachment
    
    @staticmethod
    def create_attachment(attachment_data):
        """
        Create a new attachment.
        """
        attachment = ActivityHelpers.process_attachment_data(attachment_data)
        attachment.save()
        serializer = AttachmentSerializer(attachment)
        return serializer.data
    

    @staticmethod
    def update_attachment(attachment_id, attachment_data):
        """
        Update an attachment.
        """
        attachment = ActivityQuery.get_attachment(attachment_id)
        attachment = ActivityHelpers.process_attachment_data_update(attachment, attachment_data)
        attachment.save()
        serializer = AttachmentSerializer(attachment)
        return serializer.data
    

    @staticmethod
    def delete_attachment(attachment_id):
        """
        Delete an attachment.
        """
        attachment = ActivityQuery.get_attachment(attachment_id)
        attachment.delete()
        return True
    

    @staticmethod
    def delete_all_attachments():
        """
        Delete all attachments.
        """
        attachments = ActivityQuery.get_attachments()
        attachments.delete()
        return True
    


    # Marketing Campaign Services
    @staticmethod
    def get_marketing_campaigns():
        """
        Get all marketing campaigns.
        """
        marketing_campaigns = ActivityQuery.get_marketing_campaigns()
        return marketing_campaigns
    

    @staticmethod
    def get_marketing_campaign(marketing_campaign_id):
        """
        Get a specific marketing campaign.
        """
        marketing_campaign = ActivityQuery.get_marketing_campaign(marketing_campaign_id)
        return marketing_campaign
    

    @staticmethod
    def create_marketing_campaign(marketing_campaign_data):
        """
        Create a new marketing campaign.
        """
        marketing_campaign = ActivityHelpers.process_marketing_campaign_data(marketing_campaign_data)
        marketing_campaign.save()
        serializer = MarketingCampaignSerializer(marketing_campaign)
        return serializer.data
    

    @staticmethod
    def update_marketing_campaign(marketing_campaign_id, marketing_campaign_data):
        """
        Update a marketing campaign.
        """
        marketing_campaign = ActivityQuery.get_marketing_campaign(marketing_campaign_id)
        marketing_campaign = ActivityHelpers.process_marketing_campaign_data_update(marketing_campaign, marketing_campaign_data)
        marketing_campaign.save()
        serializer = MarketingCampaignSerializer(marketing_campaign)
        return serializer.data
    

    @staticmethod
    def delete_marketing_campaign(marketing_campaign_id):
        """
        Delete a marketing campaign.
        """
        marketing_campaign = ActivityQuery.get_marketing_campaign(marketing_campaign_id)
        marketing_campaign.delete()
        return True
    

    @staticmethod
    def delete_all_marketing_campaigns():
        """
        Delete all marketing campaigns.
        """
        marketing_campaigns = ActivityQuery.get_marketing_campaigns()
        marketing_campaigns.delete()
        return True
    

    # Learning Service Services
    @staticmethod
    def get_learning_services():
        """
        Get all learning services.
        """
        learning_services = ActivityQuery.get_learning_services()
        return learning_services
    

    @staticmethod
    def get_learning_service(learning_service_id):
        """
        Get a specific learning service.
        """
        learning_service = ActivityQuery.get_learning_service(learning_service_id)
        return learning_service
    

    @staticmethod
    def create_learning_service(learning_service_data):
        """
        Create a new learning service.
        """
        learning_service = ActivityHelpers.process_learning_service_data(learning_service_data)
        learning_service.save()
        serializer = LearningServiceSerializer(learning_service)
        return serializer.data
    

    @staticmethod
    def update_learning_service(learning_service_id, learning_service_data):
        """
        Update a learning service.
        """
        learning_service = ActivityQuery.get_learning_service(learning_service_id)
        learning_service = ActivityHelpers.process_learning_service_data_update(learning_service, learning_service_data)
        learning_service.save()
        serializer = LearningServiceSerializer(learning_service)
        return serializer.data
    

    @staticmethod
    def delete_learning_service(learning_service_id):
        """
        Delete a learning service.
        """
        learning_service = ActivityQuery.get_learning_service(learning_service_id)
        learning_service.delete()
        return True
    

    @staticmethod
    def delete_all_learning_services():
        """
        Delete all learning services.
        """
        learning_services = ActivityQuery.get_learning_services()
        learning_services.delete()
        return True
    


    # Analytics Services
    @staticmethod
    def get_analytics():
        """
        Get all analytics.
        """
        analytics = ActivityQuery.get_analytics()
        return analytics
    

    @staticmethod
    def get_analytic(analytic_id):
        """
        Get a specific analytic.
        """
        analytic = ActivityQuery.get_analytic(analytic_id)
        return analytic
    

    @staticmethod
    def create_analytic(analytic_data):
        """
        Create a new analytic.
        """
        analytic = ActivityHelpers.process_analytics_data(analytic_data)
        analytic.save()
        serializer = AnalyticsSerializer(analytic)
        return serializer.data
    

    @staticmethod
    def update_analytic(analytic_id, analytic_data):
        """
        Update an analytic.
        """
        analytic = ActivityQuery.get_analytic(analytic_id)
        analytic = ActivityHelpers.process_analytics_data_update(analytic, analytic_data)
        analytic.save()
        serializer = AnalyticsSerializer(analytic)
        return serializer.data
    

    @staticmethod
    def delete_analytic(analytic_id):
        """
        Delete an analytic.
        """
        analytic = ActivityQuery.get_analytic(analytic_id)
        analytic.delete()
        return True
    

    @staticmethod
    def delete_all_analytics():
        """
        Delete all analytics.
        """
        analytics = ActivityQuery.get_analytics()
        analytics.delete()
        return True
    

    # User Activity Services
    @staticmethod
    def get_user_activities():
        """
        Get all user activities.
        """
        user_activities = ActivityQuery.get_user_activities()
        return user_activities
    

    @staticmethod
    def get_user_activity(user_activity_id):
        """
        Get a specific user activity.
        """
        user_activity = ActivityQuery.get_user_activity(user_activity_id)
        return user_activity
    

    @staticmethod
    def create_user_activity(user_activity_data):
        """
        Create a new user activity.
        """
        user_activity = ActivityHelpers.process_user_activity_data(user_activity_data)
        user_activity.save()
        serializer = UserActivitySerializer(user_activity)
        return serializer.data
    

    @staticmethod
    def update_user_activity(user_activity_id, user_activity_data):
        """
        Update a user activity.
        """
        user_activity = ActivityQuery.get_user_activity(user_activity_id)
        user_activity = ActivityHelpers.process_user_activity_data_update(user_activity, user_activity_data)
        user_activity.save()
        serializer = UserActivitySerializer(user_activity)
        return serializer.data
    


    @staticmethod
    def delete_user_activity(user_activity_id):
        """
        Delete a user activity.
        """
        user_activity = ActivityQuery.get_user_activity(user_activity_id)
        user_activity.delete()
        return True
    

    @staticmethod
    def delete_all_user_activities():
        """
        Delete all user activities.
        """
        user_activities = ActivityQuery.get_user_activities()
        user_activities.delete()
        return True
    


    # User Statistics Services
    @staticmethod
    def get_user_statistics():
        """
        Get all user statistics.
        """
        user_statistics = ActivityQuery.get_user_statistics()
        return user_statistics
    

    @staticmethod
    def get_user_statistic(user_statistic_id):
        """
        Get a specific user statistic.
        """
        user_statistic = ActivityQuery.get_user_statistic(user_statistic_id)
        return user_statistic
    


    @staticmethod
    def create_user_statistic(user_statistic_data):
        """
        Create a new user statistic.
        """
        user_statistic = ActivityHelpers.process_user_statistics_data(user_statistic_data)
        user_statistic.save()
        serializer = UserStatisticsSerializer(user_statistic)
        return serializer.data
    


    @staticmethod
    def update_user_statistic(user_statistic_id, user_statistic_data):
        """
        Update a user statistic.
        """
        user_statistic = ActivityQuery.get_user_statistic(user_statistic_id)
        user_statistic = ActivityHelpers.process_user_statistics_data_update(user_statistic, user_statistic_data)
        user_statistic.save()
        serializer = UserStatisticsSerializer(user_statistic)
        return serializer.data
    

    @staticmethod
    def delete_user_statistic(user_statistic_id):
        """
        Delete a user statistic.
        """
        user_statistic = ActivityQuery.get_user_statistic(user_statistic_id)
        user_statistic.delete()
        return True
    

    @staticmethod
    def delete_all_user_statistics():
        """
        Delete all user statistics.
        """
        user_statistics = ActivityQuery.get_user_statistics()
        user_statistics.delete()
        return True
    


    # Thread Services
    @staticmethod
    def get_threads():
        """
        Get all threads.
        """
        threads = ActivityQuery.get_threads()
        return threads
    

    @staticmethod
    def get_thread(thread_id):
        """
        Get a specific thread.
        """
        thread = ActivityQuery.get_thread(thread_id)
        return thread
    

    @staticmethod
    def create_thread(thread_data):
        """
        Create a new thread.
        """
        thread = ActivityHelpers.process_thread_data(thread_data)
        thread.save()
        serializer = ThreadSerializer(thread)
        return serializer.data
    

    @staticmethod
    def update_thread(thread_id, thread_data):
        """
        Update a thread.
        """
        thread = ActivityQuery.get_thread(thread_id)
        thread = ActivityHelpers.process_thread_data_update(thread, thread_data)
        thread.save()
        serializer = ThreadSerializer(thread)
        return serializer.data
    

    @staticmethod
    def delete_thread(thread_id):
        """
        Delete a thread.
        """
        thread = ActivityQuery.get_thread(thread_id)
        thread.delete()
        return True
    

    @staticmethod
    def delete_all_threads():
        """
        Delete all threads.
        """
        threads = ActivityQuery.get_threads()
        threads.delete()
        return True
    

    # Reaction Services
    @staticmethod
    def get_reactions():
        """
        Get all reactions.
        """
        reactions = ActivityQuery.get_reactions()
        return reactions
    

    @staticmethod
    def get_reaction(reaction_id):
        """
        Get a specific reaction.
        """
        reaction = ActivityQuery.get_reaction(reaction_id)
        return reaction
    

    @staticmethod
    def create_reaction(reaction_data):
        """
        Create a new reaction.
        """
        reaction = ActivityHelpers.process_reaction_data(reaction_data)
        reaction.save()
        serializer = ReactionSerializer(reaction)
        return serializer.data
    

    @staticmethod
    def update_reaction(reaction_id, reaction_data):
        """
        Update a reaction.
        """
        reaction = ActivityQuery.get_reaction(reaction_id)
        reaction = ActivityHelpers.process_reaction_data_update(reaction, reaction_data)
        reaction.save()
        serializer = ReactionSerializer(reaction)
        return serializer.data
    

    @staticmethod
    def delete_reaction(reaction_id):
        """
        Delete a reaction.
        """
        reaction = ActivityQuery.get_reaction(reaction_id)
        reaction.delete()
        return True
    

    @staticmethod
    def delete_all_reactions():
        """
        Delete all reactions.
        """
        reactions = ActivityQuery.get_reactions()
        reactions.delete()
        return True
    

    # Share Services
    @staticmethod
    def get_shares():
        """
        Get all shares.
        """
        shares = ActivityQuery.get_shares()
        return shares
    

    @staticmethod
    def get_share(share_id):
        """
        Get a specific share.
        """
        share = ActivityQuery.get_share(share_id)
        return share
    

    @staticmethod
    def create_share(share_data):
        """
        Create a new share.
        """
        share = ActivityHelpers.process_share_data(share_data)
        share.save()
        serializer = ShareSerializer(share)
        return serializer.data
    

    @staticmethod
    def update_share(share_id, share_data):
        """
        Update a share.
        """
        share = ActivityQuery.get_share(share_id)
        share = ActivityHelpers.process_share_data_update(share, share_data)
        share.save()
        serializer = ShareSerializer(share)
        return serializer.data
    

    @staticmethod
    def delete_share(share_id):
        """
        Delete a share.
        """
        share = ActivityQuery.get_share(share_id)
        share.delete()
        return True
    

    @staticmethod
    def delete_all_shares():
        """
        Delete all shares.
        """
        shares = ActivityQuery.get_shares()
        shares.delete()
        return True
    

    
