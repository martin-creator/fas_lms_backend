from rest_framework import serializers
from .models import RegisteredController

class RegisteredControllerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisteredController
        fields = '__all__'