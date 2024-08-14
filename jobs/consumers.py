import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import JobListing, JobApplication, JobNotification

User = get_user_model()

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"job_notifications_{self.user.id}"
            
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
        
        if event == 'create_job_listing':
            await self.create_job_listing(data)
        elif event == 'apply_to_job':
            await self.apply_to_job(data)
        elif event == 'update_application_status':
            await self.update_application_status(data)

    @database_sync_to_async
    def db_create_job_listing(self, data):
        job_listing = JobListing.objects.create(
            company_id=data['company_id'],
            title=data['title'],
            description=data['description'],
            location=data['location'],
            closing_date=data['closing_date'],
            employment_type=data['employment_type'],
            experience_level=data['experience_level']
        )
        # Notify users who are interested in such listings
        JobNotification.objects.create(
            job_listing=job_listing,
            user=self.user,
            read=False
        )
        return job_listing

    async def create_job_listing(self, data):
        job_listing = await self.db_create_job_listing(data)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'job_listing_created',
                'message': f'New job listing created: {job_listing.title}'
            }
        )

    @database_sync_to_async
    def db_apply_to_job(self, job_id, user, resume, cover_letter):
        job_listing = JobListing.objects.get(id=job_id)
        job_application = JobApplication.objects.create(
            job_listing=job_listing,
            applicant=user,
            resume=resume,
            cover_letter=cover_letter
        )
        JobNotification.objects.create(
            job_listing=job_listing,
            user=user,
            read=False
        )
        return job_application

    async def apply_to_job(self, data):
        job_id = data['job_id']
        resume = data['resume']
        cover_letter = data['cover_letter']
        job_application = await self.db_apply_to_job(job_id, self.user, resume, cover_letter)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'job_application_submitted',
                'message': f'{self.user.username} applied for {job_application.job_listing.title}'
            }
        )

    @database_sync_to_async
    def db_update_application_status(self, application_id, status):
        job_application = JobApplication.objects.get(id=application_id)
        job_application.status = status
        job_application.save()
        JobNotification.objects.create(
            job_listing=job_application.job_listing,
            user=job_application.applicant,
            read=False
        )
        return job_application

    async def update_application_status(self, data):
        application_id = data['application_id']
        status = data['status']
        job_application = await self.db_update_application_status(application_id, status)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'job_application_status_updated',
                'message': f'Status updated for {job_application.applicant.username}: {status}'
            }
        )

    async def job_listing_created(self, event):
        await self.send(text_data=json.dumps({
            'event': 'job_listing_created',
            'message': event['message']
        }))
    
    async def job_application_submitted(self, event):
        await self.send(text_data=json.dumps({
            'event': 'job_application_submitted',
            'message': event['message']
        }))
    
    async def job_application_status_updated(self, event):
        await self.send(text_data=json.dumps({
            'event': 'job_application_status_updated',
            'message': event['message']
        }))
