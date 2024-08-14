import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Company, CompanyUpdate

User = get_user_model()

class CompanyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"company_updates_{self.user.id}"
            
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
        
        if event == 'create_update':
            await self.create_update(data)
        elif event == 'follow_company':
            await self.follow_company(data)

    @database_sync_to_async
    def db_create_update(self, company_id, title, content):
        company = Company.objects.get(id=company_id)
        update = CompanyUpdate.objects.create(
            company=company,
            title=title,
            content=content
        )
        return update

    async def create_update(self, data):
        company_id = data['company_id']
        title = data['title']
        content = data['content']
        update = await self.db_create_update(company_id, title, content)
        
        # Notify all followers
        followers = Company.followers.all()
        for follower in followers:
            follower_group_name = f"company_updates_{follower.id}"
            await self.channel_layer.group_send(
                follower_group_name,
                {
                    'type': 'company_update',
                    'message': f'New update from {update.company.name}: {title}'
                }
            )

    @database_sync_to_async
    def db_follow_company(self, company_id, user):
        company = Company.objects.get(id=company_id)
        company.followers.add(user)
        return company.name

    async def follow_company(self, data):
        company_id = data['company_id']
        company_name = await self.db_follow_company(company_id, self.user)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'followed_company',
                'message': f'You are now following {company_name}'
            }
        )

    async def company_update(self, event):
        await self.send(text_data=json.dumps({
            'event': 'company_update',
            'message': event['message']
        }))
    
    async def followed_company(self, event):
        await self.send(text_data=json.dumps({
            'event': 'followed_company',
            'message': event['message']
        }))
