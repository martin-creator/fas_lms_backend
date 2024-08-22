from rest_framework import serializers
from .models import Follower, FollowRequest, FollowNotification


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'


class FollowRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRequest
        fields = '__all__'


class FollowNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowNotification
        fields = '__all__'
