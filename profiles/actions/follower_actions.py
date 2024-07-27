# profiles/actions/follower_actions.py

from followers.models import Follower, FollowRequest

class FollowerActions:

    @staticmethod
    def create_follow_request(from_user, to_user):
        if not FollowerActions.is_follow_request_exists(from_user, to_user):
            FollowRequest.objects.create(from_user=from_user, to_user=to_user)
            return {'status': 'Follow request sent'}, 200
        return {'status': 'Follow request already exists'}, 400

    @staticmethod
    def accept_follow_request(from_user, to_user):
        try:
            follow_request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            follow_request.accept()
            return {'status': 'Follow request accepted'}, 200
        except FollowRequest.DoesNotExist:
            return {'status': 'Follow request does not exist'}, 404

    @staticmethod
    def reject_follow_request(from_user, to_user):
        try:
            follow_request = FollowRequest.objects.get(from_user=from_user, to_user=to_user)
            follow_request.reject()
            return {'status': 'Follow request rejected'}, 200
        except FollowRequest.DoesNotExist:
            return {'status': 'Follow request does not exist'}, 404

    @staticmethod
    def is_follow_request_exists(from_user, to_user):
        return FollowRequest.objects.filter(from_user=from_user, to_user=to_user).exists()

    @staticmethod
    def create_follower(user, follower):
        Follower.objects.create(user=user, follower=follower)

    @staticmethod
    def delete_follower(user, follower):
        Follower.objects.filter(user=user, follower=follower).delete()
