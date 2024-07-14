from django.db.models import Count, Q
from activity.models import UserActivity, Analytics, Category, Reaction, Share, Attachment
from activity.services.activity_services import ActivityService
from activity.querying.activity_query import ActivityQuery
from activity.reports.activity_report import ActivityReport
from activity.helpers.activity_helpers import ActivityHelpers
from activity.settings.activity_settings import ActivitySettings

class ActivityController:
    
    def __init__(self):
        self.activity_service = ActivityService()
        self.activity_query = ActivityQuery()
        self.activity_report = ActivityReport()
        self.activity_helpers = ActivityHelpers()
        self.activity_settings = ActivitySettings()

    def create_activity(self, user, activity_data):
        """
        Create a new activity.
        """
        return self.activity_service.create_activity(user, activity_data)

    def update_activity(self, activity_id, activity_data):
        """
        Update an existing activity.
        """
        return self.activity_service.update_activity(activity_id, activity_data)

    def delete_activity(self, activity_id):
        """
        Delete an activity.
        """
        return self.activity_service.delete_activity(activity_id)

    def get_user_activities(self, user_id):
        """
        Retrieve activities for a specific user.
        """
        return self.activity_service.get_user_activities(user_id)

    def get_activity_by_id(self, activity_id):
        """
        Retrieve a specific activity by its ID.
        """
        return self.activity_service.get_activity_by_id(activity_id)

    def get_activities_by_category(self, category_name):
        """
        Retrieve activities based on category.
        """
        return self.activity_service.get_activities_by_category(category_name)

    def get_popular_categories(self):
        """
        Retrieve popular activity categories.
        """
        return self.activity_service.get_popular_categories()

    def add_reaction(self, user, activity_id, reaction_type):
        """
        Add a reaction to an activity.
        """
        return self.activity_service.add_reaction(user, activity_id, reaction_type)

    def share_activity(self, user, activity_id, shared_to):
        """
        Share an activity with other users.
        """
        return self.activity_service.share_activity(user, activity_id, shared_to)

    def add_attachment(self, content_object, attachment_data):
        """
        Add an attachment to an activity.
        """
        return self.activity_service.add_attachment(content_object, attachment_data)

    def get_attachments_for_activity(self, activity_id):
        """
        Retrieve attachments for a specific activity.
        """
        return self.activity_service.get_attachments_for_activity(activity_id)

    def analyze_user_engagement(self, user):
        """
        Analyze user engagement based on activities.
        """
        return self.activity_service.analyze_user_engagement(user)

    def log_user_activity(self, user, activity_type, details, categories=None):
        """
        Log user activity across the platform.
        """
        return self.activity_service.log_user_activity(user, activity_type, details, categories)

    def log_system_event(self, event_type, details):
        """
        Log system-wide events and interactions.
        """
        return self.activity_service.log_system_event(event_type, details)

    def get_trending_topics(self):
        """
        Retrieve trending topics based on analytics.
        """
        return self.activity_service.get_trending_topics()

    def log_attachment(self, content_object, attachment_type, file):
        """
        Log attachments related to an object (post, message, etc.).
        """
        return self.activity_service.log_attachment(content_object, attachment_type, file)

    def get_attachments_for_object(self, content_object):
        """
        Retrieve attachments related to a specific object.
        """
        return self.activity_service.get_attachments_for_object(content_object)

    def generate_user_activity_report(self, user_id):
        """
        Generate a report for user activities.
        """
        return self.activity_service.generate_user_activity_report(user_id)

    def get_activity_settings(self):
        """
        Get activity settings.
        """
        return self.activity_service.get_activity_settings()

    def update_activity_settings(self, settings_data):
        """
        Update activity settings.
        """
        return self.activity_service.update_activity_settings(settings_data)

    def process_activity_data(self, activity_data):
        """
        Process activity data before saving or updating.
        """
        return self.activity_service.process_activity_data(activity_data)
