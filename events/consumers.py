import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Event

class EventConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_profile = self.scope['user']
        if self.user_profile.is_authenticated:
            self.room_group_name = f"event_updates_{self.user_profile.id}"
            
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user_profile.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get('event', None)
        
        if event == 'register_for_event':
            await self.register_for_event(data)
        elif event == 'update_event':
            await self.update_event(data)

    @database_sync_to_async
    def db_register_for_event(self, event_id):
        event = Event.objects.get(id=event_id)
        # Add the user profile to the event attendees
        event.attendees.add(self.user_profile)
        return event.title

    async def register_for_event(self, data):
        event_id = data['event_id']
        event_title = await self.db_register_for_event(event_id)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'event_registration',
                'message': f'You are registered for {event_title}'
            }
        )

    @database_sync_to_async
    def db_update_event(self, event_id, updates):
        event = Event.objects.get(id=event_id)
        for attr, value in updates.items():
            setattr(event, attr, value)
        event.save()
        return event.title

    async def update_event(self, data):
        event_id = data['event_id']
        updates = data['updates']
        event_title = await self.db_update_event(event_id, updates)
        
        # Notify all attendees
        attendees = Event.attendees.all()
        for attendee in attendees:
            attendee_group_name = f"event_updates_{attendee.id}"
            await self.channel_layer.group_send(
                attendee_group_name,
                {
                    'type': 'event_updated',
                    'message': f'Event {event_title} has been updated'
                }
            )

    async def event_registration(self, event):
        await self.send(text_data=json.dumps({
            'event': 'event_registration',
            'message': event['message']
        }))
    
    async def event_updated(self, event):
        await self.send(text_data=json.dumps({
            'event': 'event_updated',
            'message': event['message']
        }))
