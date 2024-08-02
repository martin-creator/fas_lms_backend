from rest_framework import serializers
from .models import Event, EventRegistration, EventFeedback

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'


class EventFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventFeedback
        fields = '__all__'

