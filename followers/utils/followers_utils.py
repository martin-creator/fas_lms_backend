# followers/utils/followers_utils.py
from profiles.models import Follower, FollowRequest

class FollowerUtils:
    @staticmethod
    def follow_profile(profile, user_profile):
        if not user_profile.is_following(profile):
            if profile.is_private:
                FollowRequest.objects.create(from_user=user_profile, to_user=profile)
            else:
                Follower.objects.create(user=profile, follower=user_profile)

    @staticmethod
    def unfollow_profile(profile, user_profile):
        Follower.objects.filter(user=profile, follower=user_profile).delete()

    @staticmethod
    def is_following(user_profile, profile):
        return Follower.objects.filter(user=profile, follower=user_profile).exists()
