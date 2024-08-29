from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from followers.models import Follower, FollowRequest, FollowNotification
from followers.serializers import FollowerSerializer, FollowRequestSerializer, FollowNotificationSerializer
from followers.querying.followers_query import FollowerQuery
from django.utils import timezone



class FollowerReport:
    @staticmethod
    def get_follower_report(follower):
        """
        Get a report for a specific follower.
        """
        follower_data = FollowerSerializer(follower).data
        follower_requests = FollowRequest.objects.filter(follower=follower)
        follower_data['requests'] = FollowRequestSerializer(follower_requests, many=True).data

        # return json data

        json_data = {
            'follower': follower_data,
            'requests': follower_data['requests']
        }

        return json_data

    @staticmethod
    def get_user_report(user):
        """
        Get a report for a specific user.
        """
        user_data = {}
        user_data['followers'] = FollowerQuery.get_followers_by_user(user).count()
        user_data['requests'] = FollowRequest.objects.filter(user=user).count()
        user_data['notifications'] = FollowNotification.objects.filter(user=user).count()

        return user_data

    @staticmethod
    def get_company_report(company):
        """
        Get a report for a specific company.
        """
        company_data = {}
        company_data['followers'] = FollowerQuery.get_followers_by_company(company).count()
        company_data['requests'] = FollowRequest.objects.filter(company=company).count()
        company_data['notifications'] = FollowNotification.objects.filter(company=company).count()

        return company_data

