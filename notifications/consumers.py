import json
import redis
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # Generate a unique group name based on the username or user ID
        self.group_name = f"notifications_{self.scope['user'].username}"
        
        # Join the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave the group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        """
        Handle received WebSocket messages. This can be used for testing or control messages.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', 'No message content')
        
        # For demonstration: Echo the message back
        self.send(text_data=json.dumps({
            'message': message
        }))

    def send_notification(self, event):
        """
        Receive notification from the channel layer and send it to WebSocket.
        """
        notification = event['notification']
        self.send(text_data=json.dumps({
            'type': notification['type'],
            'content': notification['content'],
            'url': notification['url'],
            'timestamp': notification['timestamp'],
        }))

        

class NotificationSubscriber:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)  # Adjust settings as needed
        self.pubsub = self.r.pubsub()
        self.pubsub.subscribe('notifications')
        self.channel_layer = get_channel_layer()

    def listen(self):
        """
        Listen to Redis channel and send notifications to WebSocket consumers.
        """
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                # Parse the message from Redis
                notification = json.loads(message['data'])
                # Broadcast the notification to the appropriate WebSocket group
                async_to_sync(self.channel_layer.group_send)(
                    f"notifications_{notification['user']}",
                    {
                        'type': 'send_notification',
                        'notification': notification
                    }
                )
