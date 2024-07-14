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
        return self.activity_query.get_activities_by_user(user_id)

    def search_activities(self, query):
        """
        Search activities based on a query.
        """
        return self.activity_query.search_activities(query)

    def generate_user_activity_report(self, user_id):
        """
        Generate a user activity report.
        """
        return self.activity_report.generate_user_activity_report(user_id)

    def generate_activity_summary(self):
        """
        Generate a summary of activities.
        """
        return self.activity_report.generate_activity_summary()

    def format_activity_data(self, activity):
        """
        Format activity data for display.
        """
        return self.activity_helpers.format_activity_data(activity)

    def validate_activity_data(self, activity_data):
        """
        Validate activity data before processing.
        """
        return self.activity_helpers.validate_activity_data(activity_data)

    def get_activity_settings(self):
        """
        Retrieve activity settings.
        """
        return self.activity_settings.get_activity_settings()

    def update_activity_settings(self, settings_data):
        """
        Update activity settings.
        """
        return self.activity_settings.update_activity_settings(settings_data)
    
    
