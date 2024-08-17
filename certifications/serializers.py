from rest_framework import serializers
from .models import Company, CompanyUpdate

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyUpdate
        fields = '__all__'

