import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Certification

User = get_user_model()

class CertificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"certification_updates_{self.user.id}"
            
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
        
        if event == 'add_certification':
            await self.add_certification(data)
        elif event == 'update_verification_status':
            await self.update_verification_status(data)

    @database_sync_to_async
    def db_add_certification(self, data):
        certification = Certification.objects.create(
            user=self.user,
            name=data['name'],
            issuing_organization=data['issuing_organization'],
            issue_date=data['issue_date'],
            expiration_date=data.get('expiration_date', None),
            credential_id=data.get('credential_id', ''),
            credential_url=data.get('credential_url', ''),
            description=data.get('description', '')
        )
        return certification

    async def add_certification(self, data):
        certification = await self.db_add_certification(data)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'certification_added',
                'message': f'New certification added: {certification.name}'
            }
        )

    @database_sync_to_async
    def db_update_verification_status(self, certification_id, status):
        certification = Certification.objects.get(id=certification_id)
        certification.verification_status = status
        certification.save()
        return certification

    async def update_verification_status(self, data):
        certification_id = data['certification_id']
        status = data['status']
        certification = await self.db_update_verification_status(certification_id, status)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'verification_status_updated',
                'message': f'Verification status updated for {certification.name} to {"verified" if status else "not verified"}'
            }
        )

    async def certification_added(self, event):
        await self.send(text_data=json.dumps({
            'event': 'certification_added',
            'message': event['message']
        }))
    
    async def verification_status_updated(self, event):
        await self.send(text_data=json.dumps({
            'event': 'verification_status_updated',
            'message': event['message']
        }))
