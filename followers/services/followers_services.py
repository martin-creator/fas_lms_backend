from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from followers.models import Follower, FollowRequest, FollowNotification
from followers.serializers import FollowerSerializer, FollowRequestSerializer, FollowNotificationSerializer
from followers.settings.followers_settings import FollowersSettings
from followers.querying.followers_query import FollowerQuery
from followers.helpers.followers_helpers import FollowerHelpers
from followers.utils import UserUtils, DateTimeUtils
from followers.reports.followers_report import FollowerReport



class FollowerService:
    
        @staticmethod
        def get_followers():
            """
            Get all followers.
            """
            followers = FollowerQuery.get_followers()
            return followers
        
    
        @staticmethod
        def get_follower(follower_id):
            """
            Get a specific follower.
            """
            follower = FollowerQuery.get_follower(follower_id)
            return follower
        
    
        @staticmethod
        def get_followers_by_user(user_id):
            """
            Get all followers of a specific user.
            """
            followers = FollowerQuery.get_followers_by_user(user_id)
            return followers
        
    
        @staticmethod
        def get_followers_by_company(company_id):
            """
            Get all followers of a specific company.
            """
            followers = FollowerQuery.get_followers_by_company(company_id)
            return followers
        
    
        @staticmethod
        def get_followers_by_user_and_company(user_id, company_id):
            """
            Get all followers of a specific user for a specific company.
            """
            followers = FollowerQuery.get_followers_by_user_and_company(user_id, company_id)
            return followers
        
    
        @staticmethod
        def get_followers_by_status(status):
            """
            Get all followers with a specific status.
            """
            followers = FollowerQuery.get_followers_by_status(status)
            return followers
        
    
        @staticmethod
        def create_follower(follower_data):
            """
            Create a new follower.
            """
            follower = FollowerHelpers.process_follower_data(follower_data)
            follower.save()
    
            serializer = FollowerSerializer(follower)
    
            return serializer.data
        
    
        @staticmethod
        def update_follower(follower_id, follower_data):
            """
            Update a follower.
            """
            follower = FollowerHelpers.process_follower_data_update(follower_id, follower_data)
            follower.save()
    
            serializer = FollowerSerializer(follower)
    
            return serializer.data
        
    
        @staticmethod
        def delete_follower(follower_id):
            """
            Delete a follower.
            """
            follower = FollowerQuery.get_follower(follower_id)
            follower.delete()
    
            return True
        
    
        @staticmethod
        def delete_all_followers():
            """
            Delete all followers.
            """
            followers = FollowerQuery.get_followers()
            followers.delete()
    
            return True
        
    
        @staticmethod
        def get_follower_report(follower_id):
            """
            Get a report for a specific follower.
            """
            follower = FollowerQuery.get_follower(follower_id)
            report = FollowerReport.get_follower_report(follower)

            return report
        
        # followeRequest

        @staticmethod
        def get_follow_requests():
            """
            Get all follow requests.
            """
            follow_requests = FollowerQuery.get_follow_requests()
            return follow_requests
        

        @staticmethod
        def get_follow_request(request_id):
            """
            Get a specific follow request.
            """
            follow_request = FollowerQuery.get_follow_request(request_id)
            return follow_request
        

        @staticmethod
        def get_follow_requests_by_user(user_id):
            """
            Get all follow requests for a specific user.
            """
            follow_requests = FollowerQuery.get_follow_requests_by_user(user_id)
            return follow_requests
        

        @staticmethod
        def get_follow_requests_by_company(company_id):
            """
            Get all follow requests for a specific company.
            """
            follow_requests = FollowerQuery.get_follow_requests_by_company(company_id)
            return follow_requests
        

        @staticmethod
        def get_follow_requests_by_user_and_company(user_id, company_id):
            """
            Get all follow requests for a specific user for a specific company.
            """
            follow_requests = FollowerQuery.get_follow_requests_by_user_and_company(user_id, company_id)
            return follow_requests
        
        @staticmethod
        def get_follow_requests_by_status(status):
            """
            Get all follow requests with a specific status.
            """
            follow_requests = FollowerQuery.get_follow_requests_by_status(status)
            return follow_requests
        

        @staticmethod
        def create_follow_request(request_data):
            """
            Create a new follow request.
            """
            follow_request = FollowerHelpers.process_follow_request_data(request_data)
            follow_request.save()

            serializer = FollowRequestSerializer(follow_request)

            return serializer.data
        
        @staticmethod
        def update_follow_request(request_id, request_data):
            """
            Update a follow request.
            """
            follow_request = FollowerHelpers.process_follow_request_data_update(request_id, request_data)
            follow_request.save()

            serializer = FollowRequestSerializer(follow_request)

            return serializer.data
        

        @staticmethod
        def delete_follow_request(request_id):
            """
            Delete a follow request.
            """
            follow_request = FollowerQuery.get_follow_request(request_id)
            follow_request.delete()

            return True
        
        @staticmethod
        def delete_all_follow_requests():
            """
            Delete all follow requests.
            """
            follow_requests = FollowerQuery.get_follow_requests()
            follow_requests.delete()

            return True
        

        # FollowNotification

        @staticmethod
        def get_follow_notifications():
            """
            Get all follow notifications.
            """
            follow_notifications = FollowerQuery.get_follow_notifications()
            return follow_notifications
        

        @staticmethod
        def get_follow_notification(notification_id):
            """
            Get a specific follow notification.
            """
            follow_notification = FollowerQuery.get_follow_notification(notification_id)
            return follow_notification
        
        @staticmethod
        def create_follow_notification(notification_data):
            """
            Create a new follow notification.
            """
            follow_notification = FollowerHelpers.process_follow_notification_data(notification_data)
            follow_notification.save()

            serializer = FollowNotificationSerializer(follow_notification)

            return serializer.data
        

        @staticmethod
        def update_follow_notification(notification_id, notification_data):
            """
            Update a follow notification.
            """
            follow_notification = FollowerHelpers.process_follow_notification_data_update(notification_id, notification_data)
            follow_notification.save()

            serializer = FollowNotificationSerializer(follow_notification)

            return serializer.data
        
        @staticmethod
        def delete_follow_notification(notification_id):
            """
            Delete a follow notification.
            """
            follow_notification = FollowerQuery.get_follow_notification(notification_id)
            follow_notification.delete()

            return True
        
        @staticmethod
        def delete_all_follow_notifications():
            """
            Delete all follow notifications.
            """
            follow_notifications = FollowerQuery.get_follow_notifications()
            follow_notifications.delete()

            return True
        
        @staticmethod
        def get_user_report(user_id):
            """
            Get a report for a specific user.
            """
            user = UserUtils.get_user(user_id)
            report = FollowerReport.get_user_report(user)

            return report
        

        @staticmethod
        def get_company_report(company_id):
            """
            Get a report for a specific company.
            """
            company = CompanyService.get_company(company_id)
            report = FollowerReport.get_company_report(company)

            return report
        