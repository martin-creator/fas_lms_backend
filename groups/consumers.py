import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import Share, Reaction, Group, GroupMember, GroupPost

User = get_user_model()

class GroupActivityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"user_{self.user.id}_group_activity"
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
        
        if event == 'join_group':
            await self.join_group(data)
        elif event == 'leave_group':
            await self.leave_group(data)
        elif event == 'post_to_group':
            await self.post_to_group(data)
        elif event == 'share_post':
            await self.share_post(data)
        elif event == 'react_to_post':
            await self.react_to_post(data)

    @database_sync_to_async
    def join_group(self, data):
        group = Group.objects.get(id=data['group_id'])
        GroupMember.objects.create(user=self.user, group=group)
        return f"{self.user.username} joined the group {group.name}"

    @database_sync_to_async
    def leave_group(self, data):
        group = Group.objects.get(id=data['group_id'])
        GroupMember.objects.filter(user=self.user, group=group).delete()
        return f"{self.user.username} left the group {group.name}"

    @database_sync_to_async
    def post_to_group(self, data):
        group = Group.objects.get(id=data['group_id'])
        post = GroupPost.objects.create(user=self.user, group=group, content=data['content'])
        return f"{self.user.username} posted to group {group.name}"

    @database_sync_to_async
    def share_post(self, data):
        post = GroupPost.objects.get(id=data['post_id'])
        share = Share.objects.create(
            user=self.user,
            content_object=post
        )
        return f"{self.user.username} shared a post in group {post.group.name}"

    @database_sync_to_async
    def react_to_post(self, data):
        post = GroupPost.objects.get(id=data['post_id'])
        reaction = Reaction.objects.create(
            user=self.user,
            content_object=post,
            type=data['reaction_type']
        )
        return f"{self.user.username} reacted with {data['reaction_type']} to a post in group {post.group.name}"

    # Handling the broadcasting of messages to the user's group
    async def send_group_update(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'group_activity.message',
                'message': message
            }
        )

    async def group_activity_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'event': 'group_activity_update',
            'message': message
        }))
