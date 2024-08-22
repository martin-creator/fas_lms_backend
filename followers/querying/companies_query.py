from django.db.models import Count, Q
from followers.models import Follower, FollowRequest, FollowNotification
from followers.serializers import FollowerSerializer, FollowRequestSerializer, FollowNotificationSerializer
from django.utils import timezone


class FollowerQuery:
    @staticmethod
    def get_followers():
        """
        Get all followers.
        """
        followers = Follower.objects.all()
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_follower(follower_id):
        """
        Get a specific follower.
        """
        follower = Follower.objects.get(id=follower_id)
        serializer = FollowerSerializer(follower)
        return serializer.data

    @staticmethod
    def get_followers_by_user(user_id):
        """
        Get all followers of a specific user.
        """
        followers = Follower.objects.filter(user_id=user_id)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_company(company_id):
        """
        Get all followers of a specific company.
        """
        followers = Follower.objects.filter(company_id=company_id)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_user_and_company(user_id, company_id):
        """
        Get all followers of a specific user for a specific company.
        """
        followers = Follower.objects.filter(user_id=user_id, company_id=company_id)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_status(status):
        """
        Get all followers with a specific status.
        """
        followers = Follower.objects.filter(status=status)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_user_and_status(user_id, status):
        """
        Get all followers of a specific user with a specific status.
        """
        followers = Follower.objects.filter(user_id=user_id, status=status)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_company_and_status(company_id, status):
        """
        Get all followers of a specific company with a specific status.
        """
        followers = Follower.objects.filter(company_id=company_id, status=status)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data

    @staticmethod
    def get_followers_by_user_company_and_status(user_id, company_id, status):
        """
        Get all followers of a specific user for a specific company with a specific status.
        """
        followers = Follower.objects.filter(user_id=user_id, company_id=company_id, status=status)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data
    
    @staticmethod
    def get_followers_by_user_company_and_status(user_id, company_id, status):
        """
        Get all followers of a specific user for a specific company with a specific status.
        """
        followers = Follower.objects.filter(user_id=user_id, company_id=company_id, status=status)
        serializer = FollowerSerializer(followers, many=True)
        return serializer.data
    
    # Followrequest

    @staticmethod
    def get_follow_requests():
        """
        Get all follow requests.
        """
        follow_requests = FollowRequest.objects.all()
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_request(request_id):
        """
        Get a specific follow request.
        """
        follow_request = FollowRequest.objects.get(id=request_id)
        serializer = FollowRequestSerializer(follow_request)
        return serializer.data
    

    @staticmethod
    def get_follow_requests_by_user(user_id):
        """
        Get all follow requests for a specific user.
        """
        follow_requests = FollowRequest.objects.filter(user_id=user_id)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return serializer.data
    
    
    @staticmethod
    def get_follow_requests_by_company(company_id):
        """
        Get all follow requests for a specific company.
        """
        follow_requests = FollowRequest.objects.filter(company_id=company_id)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_requests_by_user_and_company(user_id, company_id):
        """
        Get all follow requests for a specific user for a specific company.
        """
        follow_requests = FollowRequest.objects.filter(user_id=user_id, company_id=company_id)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_requests_by_status(status):
        """
        Get all follow requests with a specific status.
        """
        follow_requests = FollowRequest.objects.filter(status=status)
        serializer = FollowRequestSerializer(follow_requests, many=True)
        return serializer.data
    

    # FollowNotificationSerializer

    @staticmethod
    def get_follow_notifications():
        """
        Get all follow notifications.
        """
        follow_notifications = FollowNotification.objects.all()
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_notification(notification_id):
        """
        Get a specific follow notification.
        """
        follow_notification = FollowNotification.objects.get(id=notification_id)
        serializer = FollowNotificationSerializer(follow_notification)
        return serializer.data
    

    @staticmethod
    def get_follow_notifications_by_user(user_id):
        """
        Get all follow notifications for a specific user.
        """
        follow_notifications = FollowNotification.objects.filter(user_id=user_id)
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_notifications_by_company(company_id):
        """
        Get all follow notifications for a specific company.
        """
        follow_notifications = FollowNotification.objects.filter(company_id=company_id)
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_notifications_by_user_and_company(user_id, company_id):
        """
        Get all follow notifications for a specific user for a specific company.
        """
        follow_notifications = FollowNotification.objects.filter(user_id=user_id, company_id=company_id)
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_notifications_by_status(status):
        """
        Get all follow notifications with a specific status.
        """
        follow_notifications = FollowNotification.objects.filter(status=status)
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_follow_notifications_by_user_and_status(user_id, status):
        """
        Get all follow notifications for a specific user with a specific status.
        """
        follow_notifications = FollowNotification.objects.filter(user_id=user_id, status=status)
        serializer = FollowNotificationSerializer(follow_notifications, many=True)
        return serializer.data



