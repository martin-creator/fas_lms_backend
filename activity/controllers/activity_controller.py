from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer, ReactionSerializer, ShareSerializer
from activity.querying.activity_query import ActivityQuery
from activity.settings.activity_settings import ActivitySettings
from activity.reports.activity_report import ActivityReport
from activity.services.activity_services import ActivityService
from activity.utils import UserUtils, DateTimeUtils


class ActivityController:
        
        def __init__(self):
            self.activity_query = ActivityQuery()
            self.activity_report = ActivityReport()
            self.activity_settings = ActivitySettings()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
            self.activity_service = ActivityService()
        
        def get_all_categories(self):
            """
            Get all categories.
            """
            return self.activity_service.get_categories()
        
        def get_category(self, category_id):
            """
            Get a specific category.
            """
            return self.activity_service.get_category(category_id)
        
        def create_category(self, category_data):
            """
            Create a new category.
            """
            return self.activity_service.create_category(category_data)
        
        def update_category(self, category_id, category_data):
            """
            Update a category.
            """
            return self.activity_service.update_category(category_id, category_data)
        
        def delete_category(self, category_id):
            """
            Delete a category.
            """
            return self.activity_service.delete_category(category_id)
        
        def delete_all_categories(self):
            """
            Delete all categories.
            """
            return self.activity_service.delete_all_categories()
        
        def get_all_attachments(self):
            """
            Get all attachments.
            """
            return self.activity_service.get_attachments()
        
        def get_attachment(self, attachment_id):
            """
            Get a specific attachment.
            """
            return self.activity_service.get_attachment(attachment_id)
        
        def create_attachment(self, attachment_data):
            """
            Create a new attachment.
            """
            return self.activity_service.create_attachment(attachment_data)
        
        def update_attachment(self, attachment_id, attachment_data):
            """
            Update an attachment.
            """
            return self.activity_service.update_attachment(attachment_id, attachment_data)
        
        def delete_attachment(self, attachment_id):
            """
            Delete an attachment.
            """
            return self.activity_service.delete_attachment(attachment_id)
        
        def delete_all_attachments(self):
            """
            Delete all attachments.
            """
            return self.activity_service.delete_all_attachments()
        
        def get_all_marketing_campaigns(self):
            """
            Get all marketing campaigns.
            """
            return self.activity_service.get_marketing_campaigns()
        
        def get_marketing_campaign(self, marketing_campaign_id):
            """
            Get a specific marketing campaign.
            """
            return self.activity_service.get_marketing_campaign(marketing_campaign_id)
        
        def create_marketing_campaign(self, marketing_campaign_data):
            """
            Create a new marketing campaign.
            """
            return self.activity_service.create_marketing_campaign(marketing_campaign_data)
        
        def update_marketing_campaign(self, marketing_campaign_id, marketing_campaign_data):
            """
            Update a marketing campaign.
            """
            return self.activity_service.update_marketing_campaign(marketing_campaign_id, marketing_campaign_data)
        
        def delete_marketing_campaign(self, marketing_campaign_id):
            """
            Delete a marketing campaign.
            """
            return self.activity_service.delete_marketing_campaign(marketing_campaign_id)
        
        def delete_all_marketing_campaigns(self):
            """
            Delete all marketing campaigns.
            """
            return self.activity_service.delete_all_marketing_campaigns()
        
        def get_all_learning_services(self):
            """
            Get all learning services.
            """
            return self.activity_service.get_learning_services()
        
        def get_learning_service(self, learning_service_id):
            """
            Get a specific learning service.
            """
            return self.activity_service.get_learning_service(learning_service_id)
        
        def create_learning_service(self, learning_service_data):
            """
            Create a new learning service.
            """
            return self.activity_service.create_learning_service(learning_service_data)
        
        def update_learning_service(self, learning_service_id, learning_service_data):
            """
            Update a learning service.
            """
            return self.activity_service.update_learning_service(learning_service_id, learning_service_data)
        
        def delete_learning_service(self, learning_service_id):
            """
            Delete a learning service.
            """
            return self.activity_service.delete_learning_service(learning_service_id)
        
        def delete_all_learning_services(self):
            """
            Delete all learning services.
            """
            return self.activity_service.delete_all_learning_services()
        
        def get_all_analytics(self):
            """
            Get all analytics.
            """
            return self.activity_service.get_analytics()
        
        def get_analytic(self, analytic_id):
            """
            Get a specific analytic.
            """
            return self.activity_service.get_analytic(analytic_id)
        
        def create_analytic(self, analytic_data):
            """
            Create a new analytic.
            """
            return self.activity_service.create_analytic(analytic_data)
        
        def update_analytic(self, analytic_id, analytic_data):
            """
            Update an analytic.
            """
            return self.activity_service.update_analytic(analytic_id, analytic_data)
        
        def delete_analytic(self, analytic_id):
            """
            Delete an analytic.
            """
            return self.activity_service.delete_analytic(analytic_id)
        
        def delete_all_analytics(self):
            """
            Delete all analytics.
            """
            return self.activity_service.delete_all_analytics()
        
        def get_all_user_activities(self):
            """
            Get all user activities.
            """
            return self.activity_service.get_user_activities()
        
        def get_user_activity(self, user_activity_id):
            """
            Get a specific user activity.
            """
            return self.activity_service.get_user_activity(user_activity_id)
        
        def create_user_activity(self, user_activity_data):
            """
            Create a new user activity.
            """
            return self.activity_service.create_user_activity(user_activity_data)
        
        def update_user_activity(self, user_activity_id, user_activity_data):
            """
            Update a user activity.
            """
            return self.activity_service.update_user_activity(user_activity_id, user_activity_data)
        
        def delete_user_activity(self, user_activity_id):
            """
            Delete a user activity.
            """
            return self.activity_service.delete_user_activity(user_activity_id)
        
        def delete_all_user_activities(self):
            """
            Delete all user activities.
            """
            return self.activity_service.delete_all_user_activities()
        
        def get_all_user_statistics(self):
            """
            Get all user statistics.
            """
            return self.activity_service.get_user_statistics()
        
        def get_user_statistic(self, user_statistic_id):
            """
            Get a specific user statistic.
            """
            return self.activity_service.get_user_statistic(user_statistic_id)
        
        def create_user_statistic(self, user_statistic_data):
            """
            Create a new user statistic.
            """
            return self.activity_service.create_user_statistic(user_statistic_data)
        
        def update_user_statistic(self, user_statistic_id, user_statistic_data):
            """
            Update a user statistic.
            """
            return self.activity_service.update_user_statistic(user_statistic_id, user_statistic_data)
        
        def delete_user_statistic(self, user_statistic_id):
            """
            Delete a user statistic.
            """
            return self.activity_service.delete_user_statistic(user_statistic_id)
        
        def delete_all_user_statistics(self):
            """
            Delete all user statistics.
            """
            return self.activity_service.delete_all_user_statistics()
        
        def get_all_threads(self):
            """
            Get all threads.
            """
            return self.activity_service.get_threads()
        
        def get_thread(self, thread_id):
            """
            Get a specific thread.
            """
            return self.activity_service.get_thread(thread_id)
        
        def create_thread(self, thread_data):
            """
            Create a new thread.
            """
            return self.activity_service.create_thread(thread_data)
        
        def update_thread(self, thread_id, thread_data):
            """
            Update a thread.
            """
            return self.activity_service.update_thread(thread_id, thread_data)
        
        def delete_thread(self, thread_id):
            """
            Delete a thread.
            """
            return self.activity_service.delete_thread(thread_id)
        
        def delete_all_threads(self):
            """
            Delete all threads.
            """
            return self.activity_service.delete_all_threads()
        
        def get_all_reactions(self):
            """
            Get all reactions.
            """
            return self.activity_service.get_reactions()
        
        def get_reaction(self, reaction_id):
            """
            Get a specific reaction.
            """
            return self.activity_service.get_reaction(reaction_id)
        
        def create_reaction(self, reaction_data):
            """
            Create a new reaction.
            """
            return self.activity_service.create_reaction(reaction_data)
        
        def update_reaction(self, reaction_id, reaction_data):
            """
            Update a reaction.
            """
            return self.activity_service.update_reaction(reaction_id, reaction_data)
        
        def delete_reaction(self, reaction_id):
            """
            Delete a reaction.
            """
            return self.activity_service.delete_reaction(reaction_id)
        
        def delete_all_reactions(self):
            """
            Delete all reactions.
            """
            return self.activity_service.delete_all_reactions()
        
        def get_all_shares(self):
            """
            Get all shares.
            """
            return self.activity_service.get_shares()
        
        def get_share(self, share_id):
            """
            Get a specific share.
            """
            return self.activity_service.get_share(share_id)
        
        def create_share(self, share_data):
            """
            Create a new share.
            """
            return self.activity_service.create_share(share_data)
        
        def update_share(self, share_id, share_data):
            """
            Update a share.
            """
            return self.activity_service.update_share(share_id, share_data)
        
        def delete_share(self, share_id):
            """
            Delete a share.
            """
            return self.activity_service.delete_share(share_id)
        
        def delete_all_shares(self):
            """
            Delete all shares.
            """
            return self.activity_service.delete_all_shares()
        
      
        
