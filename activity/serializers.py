from rest_framework import serializers
from .models import Category, Attachment, MarketingCampaign, LearningService, Analytics


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class MarketingCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingCampaign
        fields = '__all__'


class LearningServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningService
        fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = '__all__'
