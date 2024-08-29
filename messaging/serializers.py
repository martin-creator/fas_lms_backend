from rest_framework import serializers
from messaging.models import Message, ChatRoom, ChatRoomNotification


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'



class ChatRoomNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoomNotification
        fields = '__all__'