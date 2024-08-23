from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from followers.models import Follower, FollowRequest, FollowNotification
from followers.serializers import FollowerSerializer, FollowRequestSerializer, FollowNotificationSerializer
from followers.settings.followers_settings import FollowersSettings
from followers.querying.followers_query import FollowerQuery
from followers.helpers.followers_helpers import FollowerHelpers
from followers.utils import UserUtils, DateTimeUtils
from followers.reports.followers_report import FollowerReport
from followers.services.followers_services import FollowerService


class FollowerController:
        
        def __init__(self):
            self.follower_query = FollowerQuery()
            self.follower_report = FollowerReport()
            self.follower_service = FollowerService()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
    
    
        def get_all_followers(self):
            """
            Get all followers.
            """
            return self.follower_service.get_followers()
    
    
        def get_follower_by_id(self, follower_id):
            """
            Get a specific follower.
            """
            return self.follower_service.get_follower(follower_id)
    
    
        def get_followers_by_user(self, user_id):
            """
            Get all followers of a specific user.
            """
            return self.follower_service.get_followers_by_user(user_id)
    
    
        def get_followers_by_company(self, company_id):
            """
            Get all followers of a specific company.
            """
            return self.follower_service.get_followers_by_company(company_id)
    
    
        def get_followers_by_user_and_company(self, user_id, company_id):
            """
            Get all followers of a specific user for a specific company.
            """
            return self.follower_service.get_followers_by_user_and_company(user_id, company_id)
        

        # Follower Requests

        def get_all_follow_requests(self):
            """
            Get all follow requests.
            """
            return self.follower_service.get_follow_requests()
        

        def get_follow_request_by_id(self, request_id):
            """
            Get a specific follow request.
            """
            return self.follower_service.get_follow_request(request_id)
        

        def get_follow_requests_by_user(self, user_id):
            """
            Get all follow requests for a user.
            """
            return self.follower_service.get_follow_requests_by_user(user_id)
        

        def get_follow_requests_by_company(self, company_id):
            """
            Get all follow requests for a company.
            """
            return self.follower_service.get_follow_requests_by_company(company_id)
        
        

        def get_follow_requests_by_user_and_company(self, user_id, company_id):
            """
            Get all follow requests for a user for a company.
            """
            return self.follower_service.get_follow_requests_by_user_and_company(user_id, company_id)
        

        def create_follow_request(self, request_data):
            """
            Create a follow request.
            """
            return self.follower_service.create_follow_request(request_data)
        

        
        

        def update_follow_request(self, request_id, request_data):
            """
            Update a follow request.
            """
            return self.follower_service.update_follow_request(request_id, request_data)
        

        def delete_follow_request(self, request_id):
            """
            Delete a follow request.
            """
            return self.follower_service.delete_follow_request(request_id)
        

        # Follow Notifications

        def get_all_follow_notifications(self):
            """
            Get all follow notifications.
            """
            return self.follower_service.get_follow_notifications()
        

        def get_follow_notification_by_id(self, notification_id):
            """
            Get a specific follow notification.
            """
            return self.follower_service.get_follow_notification(notification_id)
        

        def create_follow_notification(self, notification_data):
            """
            Create a follow notification.
            """
            return self.follower_service.create_follow_notification(notification_data)
        

        def update_follow_notification(self, notification_id, notification_data):
            """
            Update a follow notification.
            """
            return self.follower_service.update_follow_notification(notification_id, notification_data)
        

        def delete_follow_notification(self, notification_id):
            """
            Delete a follow notification.
            """
            return self.follower_service.delete_follow_notification(notification_id)
        

        def delete_all_follow_notifications(self):
            """
            Delete all follow notifications.
            """
            return self.follower_service.delete_all_follow_notifications()
        

        def get_follow_notifications_by_user(self, user_id):
            """
            Get all follow notifications for a user.
            """
            return self.follower_service.get_follow_notifications_by_user(user_id)
        

        def get_follow_notifications_by_company(self, company_id):
            """
            Get all follow notifications for a company.
            """
            return self.follower_service.get_follow_notifications_by_company(company_id)
        

