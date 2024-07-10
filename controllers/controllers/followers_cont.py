from followers.models import Follower, FollowRequest, FollowNotification
from django.conf import settings


class FollowerSystemController:
    def __init__(self):
        pass

    def follow_user(self, user, follower):
        if not Follower.is_follower(user, follower):
            new_follower = Follower(user=user, follower=follower)
            new_follower.save()
        return True

    def unfollow_user(self, user, follower):
        try:
            existing_follower = Follower.objects.get(user=user, follower=follower)
            existing_follower.delete()
            return True
        except Follower.DoesNotExist:
            return False

    def send_follow_request(self, from_user, to_user, message=""):
        follow_request = FollowRequest(
            from_user=from_user,
            to_user=to_user,
            message=message
        )
        follow_request.save()
        return follow_request

    def accept_follow_request(self, request_id):
        follow_request = FollowRequest.objects.get(id=request_id)
        follow_request.accept()
        return follow_request

    def reject_follow_request(self, request_id):
        follow_request = FollowRequest.objects.get(id=request_id)
        follow_request.reject()
        return follow_request

    def notify_user(self, user, message):
        notification = FollowNotification(user=user, message=message)
        notification.save()
        return notification

    def mark_notification_as_read(self, notification_id):
        notification = FollowNotification.objects.get(id=notification_id)
        notification.read = True
        notification.save()
        return notification
