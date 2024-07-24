import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import FollowRequest, Follower, FollowNotification
from profiles.models import UserProfile

class FollowerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_name = f"user_{self.user.id}"
            self.room_group_name = f"user_{self.user.id}_notifications"
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get('event', None)
        
        if event == 'send_follow_request':
            await self.send_follow_request(data)
        elif event == 'accept_follow_request':
            await self.accept_follow_request(data)
        elif event == 'reject_follow_request':
            await self.reject_follow_request(data)

    async def send_follow_request(self, data):
        from_user_id = data['from_user_id']
        to_user_id = data['to_user_id']
        message = data.get('message', '')

        from_user = await database_sync_to_async(UserProfile.objects.get)(id=from_user_id)
        to_user = await database_sync_to_async(UserProfile.objects.get)(id=to_user_id)

        follow_request = FollowRequest(from_user=from_user, to_user=to_user, message=message)
        await database_sync_to_async(follow_request.save)()

        await self.channel_layer.group_send(
            f"user_{to_user.id}_notifications",
            {
                'type': 'follow_request_received',
                'from_user': from_user.username,
                'to_user': to_user.username,
                'status': follow_request.status,
                'created_at': str(follow_request.created_at),
                'message': follow_request.message
            }
        )

    async def accept_follow_request(self, data):
        request_id = data['request_id']
        follow_request = await database_sync_to_async(FollowRequest.objects.get)(id=request_id)
        
        await database_sync_to_async(follow_request.accept)()
        
        # Explicitly create a Follower relationship
        follower_relationship = Follower(user=follow_request.to_user, follower=follow_request.from_user)
        await database_sync_to_async(follower_relationship.save)()

        # Create a follow notification if needed
        notification_message = f"{follow_request.from_user.username} is now following you."
        follow_notification = FollowNotification(user=follow_request.to_user, message=notification_message)
        await database_sync_to_async(follow_notification.save)()

        await self.channel_layer.group_send(
            f"user_{follow_request.from_user.id}_notifications",
            {
                'type': 'follow_request_accepted',
                'from_user': follow_request.from_user.username,
                'to_user': follow_request.to_user.username,
            }
        )

    async def reject_follow_request(self, data):
        request_id = data['request_id']
        follow_request = await database_sync_to_async(FollowRequest.objects.get)(id=request_id)
        
        await database_sync_to_async(follow_request.reject)()
        
        await self.channel_layer.group_send(
            f"user_{follow_request.from_user.id}_notifications",
            {
                'type': 'follow_request_rejected',
                'from_user': follow_request.from_user.username,
                'to_user': follow_request.to_user.username,
            }
        )

    async def follow_request_received(self, event):
        await self.send(text_data=json.dumps({
            'event': 'follow_request_received',
            'from_user': event['from_user'],
            'to_user': event['to_user'],
            'status': event['status'],
            'created_at': event['created_at'],
            'message': event['message']
        }))
    
    async def follow_request_accepted(self, event):
        await self.send(text_data=json.dumps({
            'event': 'follow_request_accepted',
            'from_user': event['from_user'],
            'to_user': event['to_user']
        }))
    
    async def follow_request_rejected(self, event):
        await self.send(text_data=json.dumps({
            'event': 'follow_request_rejected',
            'from_user': event['from_user'],
            'to_user': event['to_user']
        }))
