# serializers.py

from rest_framework import serializers
from .models import ConnectionRequest, Connection

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at']

class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'user', 'connection', 'created_at']
