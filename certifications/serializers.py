from rest_framework import serializers
from .models import Certification, LinkedInBadge

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class LinkedInBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinkedInBadge
        fields = '__all__'

