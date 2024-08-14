import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

class PostConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"post_updates_{self.user.id}"
            
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
        
        if event == 'create_post':
            await self.create_post(data)
        elif event == 'comment_on_post':
            await self.comment_on_post(data)
        elif event == 'like_post':
            await self.like_post(data)

    @database_sync_to_async
    def db_create_post(self, author, content):
        post = Post.objects.create(author=author, content=content)
        return post

    async def create_post(self, data):
        content = data['content']
        post = await self.db_create_post(self.user, content)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'post_created',
                'message': f'New post created by {self.user.username}: {post.content[:50]}'
            }
        )

    @database_sync_to_async
    def db_comment_on_post(self, post_id, author, content):
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(post=post, author=author, content=content)
        return comment

    async def comment_on_post(self, data):
        post_id = data['post_id']
        content = data['content']
        comment = await self.db_comment_on_post(post_id, self.user, content)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'post_commented',
                'message': f'New comment by {self.user.username} on post {post_id}: {comment.content[:50]}'
            }
        )

    @database_sync_to_async
    def db_like_post(self, post_id, user):
        post = Post.objects.get(id=post_id)
        post.likes.add(user)
        return post

    async def like_post(self, data):
        post_id = data['post_id']
        await self.db_like_post(post_id, self.user)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'post_liked',
                'message': f'{self.user.username} liked post {post_id}'
            }
        )

    async def post_created(self, event):
        await self.send(text_data=json.dumps({
            'event': 'post_created',
            'message': event['message']
        }))
    
    async def post_commented(self, event):
        await self.send(text_data=json.dumps({
            'event': 'post_commented',
            'message': event['message']
        }))
    
    async def post_liked(self, event):
        await self.send(text_data=json.dumps({
            'event': 'post_liked',
            'message': event['message']
        }))
