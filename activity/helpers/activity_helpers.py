from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()





class ActivityHelpers:
    
        @staticmethod
        def process_category_data(data):
            """
            Process category data before saving it to the database.
            """
            name = data.get('name')
            description = data.get('description')
    
            category = Category(
                name=name,
                description=description
            )
    
            return category
        
    
        @staticmethod
        def process_category_data_update(category_id, data):
            """
            Process category data before updating it in the database.
            """
            category = Category.objects.get(id=category_id)
            
            name = data.get('name')
            description = data.get('description')
    
            if name is not None:
                category.name = name
    
            if description is not None:
                category.description = description
    
            return category
        
        @staticmethod
        def process_attachment_data(data):
            """
            Process attachment data before saving it to the database.
            """
            attachment_type = data.get('attachment_type')
            file = data.get('file')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
    
            attachment = Attachment(
                attachment_type=attachment_type,
                file=file,
                content_type=content_type,
                object_id=object_id
            )
    
            return attachment
        
    
        @staticmethod
        def process_attachment_data_update(attachment_id, data):
            """
            Process attachment data before updating it in the database.
            """
            attachment = Attachment.objects.get(id=attachment_id)
            
            attachment_type = data.get('attachment_type')
            file = data.get('file')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
    
            if attachment_type is not None:
                attachment.attachment_type = attachment_type
    
            if file is not None:
                attachment.file = file
    
            if content_type is not None:
                attachment.content_type = content_type
    
            if object_id is not None:
                attachment.object_id = object_id
    
            return attachment
        
        @staticmethod
        def process_marketing_campaign_data(data):
            """
            Process marketing campaign data before saving it to the database.
            """
            campaign_name = data.get('campaign_name')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            target_audience = data.get('target_audience')
            categories = data.get('categories')
            attachments = data.get('attachments')
    
            campaign = MarketingCampaign(
                campaign_name=campaign_name,
                start_date=start_date,
                end_date=end_date,
                target_audience=target_audience
            )

            return campaign, categories, attachments
        


        @staticmethod
        def process_marketing_campaign_data_update(campaign_id, data):
            """
            Process marketing campaign data before updating it in the database.
            """
            campaign = MarketingCampaign.objects.get(id=campaign_id)
            
            campaign_name = data.get('campaign_name')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            target_audience = data.get('target_audience')
            categories = data.get('categories')
            attachments = data.get('attachments')
    
            if campaign_name is not None:
                campaign.campaign_name = campaign_name
    
            if start_date is not None:
                campaign.start_date = start_date
    
            if end_date is not None:
                campaign.end_date = end_date
    
            if target_audience is not None:
                campaign.target_audience = target_audience
    
            if categories is not None:
                campaign.categories.set(categories)
    
            if attachments is not None:
                campaign.attachments.set(attachments)
    
            return campaign, categories, attachments
        

        @staticmethod
        def process_learning_service_data(data):
            """
            Process learning service data before saving it to the database.
            """
            service_name = data.get('service_name')
            description = data.get('description')
            categories = data.get('categories')
            resources = data.get('resources')
            attachments = data.get('attachments')
    
            service = LearningService(
                service_name=service_name,
                description=description,
                resources=resources
            )
    
            return service, categories, attachments
        

        @staticmethod
        def process_learning_service_data_update(service_id, data):
            """
            Process learning service data before updating it in the database.
            """
            service = LearningService.objects.get(id=service_id)
            
            service_name = data.get('service_name')
            description = data.get('description')
            categories = data.get('categories')
            resources = data.get('resources')
            attachments = data.get('attachments')
    
            if service_name is not None:
                service.service_name = service_name
    
            if description is not None:
                service.description = description
    
            if resources is not None:
                service.resources = resources
    
            if categories is not None:
                service.categories.set(categories)
    
            if attachments is not None:
                service.attachments.set(attachments)
    
            return service, categories, attachments
        

        @staticmethod
        def process_analytics_data(data):
            """
            Process analytics data before saving it to the database.
            """
            activity_type = data.get('activity_type')
            engagement_rate = data.get('engagement_rate')
            trending_topics = data.get('trending_topics')
            categories = data.get('categories')
    
            analytics = Analytics(
                activity_type=activity_type,
                engagement_rate=engagement_rate,
                trending_topics=trending_topics
            )
    
            return analytics, categories
        

        @staticmethod
        def process_analytics_data_update(analytics_id, data):
            """
            Process analytics data before updating it in the database.
            """
            analytics = Analytics.objects.get(id=analytics_id)
            
            activity_type = data.get('activity_type')
            engagement_rate = data.get('engagement_rate')
            trending_topics = data.get('trending_topics')
            categories = data.get('categories')
    
            if activity_type is not None:
                analytics.activity_type = activity_type
    
            if engagement_rate is not None:
                analytics.engagement_rate = engagement_rate
    
            if trending_topics is not None:
                analytics.trending_topics = trending_topics
    
            if categories is not None:
                analytics.categories.set(categories)
    
            return analytics, categories
        

        @staticmethod
        def process_user_activity_data(data):
            """
            Process user activity data before saving it to the database.
            """
            user_id = data.get('user_id')
            activity_type = data.get('activity_type')
            details = data.get('details')
            categories = data.get('categories')
    
            user = User.objects.get(id=user_id)
    
            user_activity = UserActivity(
                user=user,
                activity_type=activity_type,
                details=details
            )
    
            return user_activity, categories
        

        @staticmethod
        def process_user_activity_data_update(activity_id, data):
            """
            Process user activity data before updating it in the database.
            """
            user_activity = UserActivity.objects.get(id=activity_id)
            
            activity_type = data.get('activity_type')
            details = data.get('details')
            categories = data.get('categories')
    
            if activity_type is not None:
                user_activity.activity_type = activity_type
    
            if details is not None:
                user_activity.details = details
    
            if categories is not None:
                user_activity.categories.set(categories)
    
            return user_activity, categories
        

        @staticmethod
        def process_user_statistics_data(data):
            """
            Process user statistics data before saving it to the database.
            """
            user_id = data.get('user_id')
            connections_count = data.get('connections_count')
            posts_count = data.get('posts_count')
            engagement_rate = data.get('engagement_rate')
    
            user = User.objects.get(id=user_id)
    
            user_statistics = UserStatistics(
                user=user,
                connections_count=connections_count,
                posts_count=posts_count,
                engagement_rate=engagement_rate
            )
    
            return user_statistics
        

        @staticmethod
        def process_user_statistics_data_update(statistics_id, data):
            """
            Process user statistics data before updating it in the database.
            """
            user_statistics = UserStatistics.objects.get(id=statistics_id)
            
            connections_count = data.get('connections_count')
            posts_count = data.get('posts_count')
            engagement_rate = data.get('engagement_rate')
    
            if connections_count is not None:
                user_statistics.connections_count = connections_count
    
            if posts_count is not None:
                user_statistics.posts_count = posts_count
    
            if engagement_rate is not None:
                user_statistics.engagement_rate = engagement_rate
    
            return user_statistics
        

        @staticmethod
        def process_thread_data(data):
            """
            Process thread data before saving it to the database.
            """
            participants = data.get('participants')
            subject = data.get('subject')
            last_message_at = data.get('last_message_at')
    
            thread = Thread(
                subject=subject,
                last_message_at=last_message_at
            )
    
            return thread, participants
        

        @staticmethod
        def process_thread_data_update(thread_id, data):
            """
            Process thread data before updating it in the database.
            """
            thread = Thread.objects.get(id=thread_id)
            
            participants = data.get('participants')
            subject = data.get('subject')
            last_message_at = data.get('last_message_at')
    
            if participants is not None:
                thread.participants.set(participants)
    
            if subject is not None:
                thread.subject = subject
    
            if last_message_at is not None:
                thread.last_message_at = last_message_at
    
            return thread, participants
        

    
        @staticmethod
        def process_reaction_data(data):
            """
            Process reaction data before saving it to the database.
            """
            type = data.get('type')
            user_id = data.get('user_id')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
    
            user = User.objects.get(id=user_id)
    
            reaction = Reaction(
                type=type,
                user=user,
                content_type=content_type,
                object_id=object_id
            )
    
            return reaction
        

        @staticmethod
        def process_reaction_data_update(reaction_id, data):
            """
            Process reaction data before updating it in the database.
            """
            reaction = Reaction.objects.get(id=reaction_id)
            
            type = data.get('type')
            user_id = data.get('user_id')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
    
            if type is not None:
                reaction.type = type
    
            if user_id is not None:
                user = User.objects.get(id=user_id)
                reaction.user = user
    
            if content_type is not None:
                reaction.content_type = content_type
    
            if object_id is not None:
                reaction.object_id = object_id
    
            return reaction
        


        @staticmethod
        def process_share_data(data):
            """
            Process share data before saving it to the database.
            """
            user_id = data.get('user_id')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
            shared_to = data.get('shared_to')
    
            user = User.objects.get(id=user_id)
    
            share = Share(
                user=user,
                content_type=content_type,
                object_id=object_id
            )
    
            return share, shared_to
        

        @staticmethod
        def process_share_data_update(share_id, data):
            """
            Process share data before updating it in the database.
            """
            share = Share.objects.get(id=share_id)
            
            user_id = data.get('user_id')
            content_type = data.get('content_type')
            object_id = data.get('object_id')
            shared_to = data.get('shared_to')
    
            if user_id is not None:
                user = User.objects.get(id=user_id)
                share.user = user
    
            if content_type is not None:
                share.content_type = content_type
    
            if object_id is not None:
                share.object_id = object_id
    
            if shared_to is not None:
                share.shared_to.set(shared_to)
    
            return share, shared_to
        
