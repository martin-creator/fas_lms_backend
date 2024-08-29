from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


# class Category(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
    
#     def get_related_objects(self):
#         related_objects = []
#         for related_name in self._meta.related_objects:
#             related_manager = getattr(self, related_name.get_accessor_name())
#             related_objects.extend(related_manager.all())
#         return related_objects

#     def __str__(self):
#         return self.name
    

    
# class Share(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
#     shared_at = models.DateTimeField(auto_now_add=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     shared_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='received_shares')
    
#     class Meta:
#         indexes = [
#             models.Index(fields=['user', 'shared_at']),
#             models.Index(fields=['content_type', 'object_id']),
#         ]
    
#     # def clean(self):
#     #     if self.user in self.shared_to.all():
#     #         raise ValidationError("Users cannot share content with themselves.")
#     #     super().clean()
        
#     def get_share_details(self):
#         return f"Shared by {self.user.username} on {self.shared_at}, content: {self.content_object}, shared with {self.shared_to.all()}"

#     def __str__(self):
#         return f"{self.user.username} shared {self.content_object} with {self.shared_to.count()} users"

# class Reaction(models.Model):
#     REACTION_CHOICES = [
#         ('like', 'Like'),
#         ('heart', 'Heart'),
#         ('laugh', 'Laugh'),
#         ('wow', 'Wow'),
#         ('sad', 'Sad'),
#         ('insight', 'Insight')
#     ]
#     type = models.CharField(max_length=20, choices=REACTION_CHOICES)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('user', 'content_type', 'object_id')

#     def save(self, *args, **kwargs):
#         if self.content_object is None:
#             logger.error(f"Reaction content_object is None for Reaction ID: {self.id}")
#         super().save(*args, **kwargs)
        
#     def get_reactions_summary(self):
#         summary = {}
#         for choice in dict(self.REACTION_CHOICES).keys():
#             summary[choice] = self.objects.filter(type=choice, content_type=self.content_type, object_id=self.object_id).count()
#         return summary

#     def __str__(self):
#         return f"{self.user.username} reacted with {self.type} to {self.content_object}"
    
# class Attachment(models.Model):
#     PHOTO = 'photo'
#     DOCUMENT = 'document'
#     VIDEO = 'video'
#     AUDIO = 'audio'
#     OTHER = 'other'

#     ATTACHMENT_TYPE_CHOICES = [
#         (PHOTO, 'Photo'),
#         (DOCUMENT, 'Document'),
#         (VIDEO, 'Video'),
#         (AUDIO, 'Audio'),
#         (OTHER, 'Other'),
#     ]

#     attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES, default=PHOTO)
#     file = models.FileField(upload_to='attachments/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)
#     content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
#     object_id = models.PositiveIntegerField()
#     content_object = GenericForeignKey('content_type', 'object_id')
#     share = GenericRelation(Share, related_name='shares_attachments')
    

#     def get_attachment_url(self):
#         if self.file:
#             return self.file.url
#         return None
    
#     def delete(self, *args, **kwargs):
#         self.file.delete(save=False)
#         super().delete(*args, **kwargs)
    
#     def __str__(self):
#         return f"Attachment for {self.content_object}"
    
    
# class Thread(models.Model):
#     participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='threads')
#     subject = models.CharField(max_length=255)
#     last_message_at = models.DateTimeField()
    
#     def get_last_message(self):
#         return self.messages.order_by('created_at').last()
    
#     def add_participant(self, user):
#         if user not in self.participants.all():
#             self.participants.add(user)

#     def __str__(self):
#         return self.subject
    
    
# class UserActivity(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     activity_type = models.CharField(max_length=50)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     details = models.TextField()
#     categories = models.ManyToManyField(Category, related_name='user_activity_categories')
    
#     @classmethod
#     def log_activity(cls, user, activity_type, details, categories=None):
#         activity = cls.objects.create(user=user, activity_type=activity_type, details=details)
#         if categories:
#             activity.categories.set(categories)
#         return activity

#     def __str__(self):
#         return f"{self.user.username} - {self.activity_type}"
    
    
# class UserStatistics(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     connections_count = models.IntegerField(default=0)
#     posts_count = models.IntegerField(default=0)
#     engagement_rate = models.FloatField(default=0.0)
    
#     def update_statistics(self, new_connections=None, new_posts=None, new_engagement=None):
#         if new_connections is not None:
#             self.connections_count += new_connections
#         if new_posts is not None:
#             self.posts_count += new_posts
#         if new_engagement is not None:
#             self.engagement_rate = (self.engagement_rate + new_engagement) / 2
#         self.save()

#     def __str__(self):
#         return f"Statistics for {self.user.username}"
    
    
# class MarketingCampaign(models.Model):
#     campaign_name = models.CharField(max_length=100)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     target_audience = models.TextField()
#     categories = models.ManyToManyField(Category, related_name='marketing_categories')
#     attachments = GenericRelation(Attachment)
    
#     def is_active(self):
#         today = timezone.now().date()
#         return self.start_date <= today <= self.end_date

#     def add_attachment(self, attachment):
#         self.attachments.add(attachment)
    
#     def __str__(self):
#         return self.campaign_name
    
    
# class LearningService(models.Model):
#     service_name = models.CharField(max_length=100)
#     description = models.TextField()
#     categories = models.ManyToManyField(Category, related_name='learning_service_categories')
#     resources = models.URLField()
#     attachments = GenericRelation(Attachment)

#     def get_related_resources(self):
#         return self.resources

#     def add_category(self, category):
#         self.categories.add(category)
    
#     def __str__(self):
#         return self.service_name
    
    
# class Analytics(models.Model):
#     activity_type = models.CharField(max_length=50)
#     engagement_rate = models.FloatField(default=0.0)
#     trending_topics = models.TextField()
#     categories = models.ManyToManyField(Category, related_name='analytics_categories')
    
#     def update_engagement_rate(self, new_rate):
#         self.engagement_rate = (self.engagement_rate + new_rate) / 2
#         self.save()
        
#     def add_trending_topic(self, topic):
#         self.trending_topics += f", {topic}"
#         self.save()

#     def __str__(self):
#         return self.activity_type



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
        
