from rest_framework import serializers
from .models import JobListing, JobApplication, JobNotification


class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = '__all__'


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'


class JobNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobNotification
        fields = '__all__'
