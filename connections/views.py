from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import ConnectionRequest, Connection
from .serializers import ConnectionRequestSerializer, ConnectionSerializer

class ConnectionRequestViewSet(viewsets.ModelViewSet):
    queryset = ConnectionRequest.objects.all()
    serializer_class = ConnectionRequestSerializer

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
