from rest_framework import serializers
from .models import UserActivity, Analytics, Category, Reaction, Share, Attachment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')

class UserActivitySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = UserActivity
        fields = ('id', 'user', 'activity_type', 'timestamp', 'details', 'categories')

class AnalyticsSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Analytics
        fields = ('id', 'activity_type', 'engagement_rate', 'trending_topics', 'categories')
        
        
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'type', 'user', 'message', 'post', 'comment', 'job_post', 'group')
        
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'attachment_type', 'file', 'uploaded_at', 'content_type', 'object_id', 'content_object')

class ShareSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Share
        fields = ('id', 'user', 'shared_at', 'content_type', 'object_id', 'content_object', 'shared_to', 'attachments')