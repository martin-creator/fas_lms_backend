import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Course, CourseEnrollment, CourseCompletion

User = get_user_model()

class CourseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.room_group_name = f"course_updates_{self.user.id}"
            
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
        
        if event == 'enroll_course':
            await self.enroll_course(data)
        elif event == 'complete_course':
            await self.complete_course(data)

    @database_sync_to_async
    def db_enroll_course(self, course_id):
        course = Course.objects.get(id=course_id)
        enrollment, created = CourseEnrollment.objects.get_or_create(
            course=course,
            student=self.user
        )
        return course.title, created

    async def enroll_course(self, data):
        course_id = data['course_id']
        course_title, created = await self.db_enroll_course(course_id)
        
        if created:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'course_enrolled',
                    'message': f'You are enrolled in {course_title}'
                }
            )

    @database_sync_to_async
    def db_complete_course(self, course_id):
        course = Course.objects.get(id=course_id)
        completion, created = CourseCompletion.objects.get_or_create(
            course=course,
            student=self.user,
            defaults={'certificate_url': course.certificate_url}  # Assuming there's a direct link to a general certificate
        )
        return course.title, created

    async def complete_course(self, data):
        course_id = data['course_id']
        course_title, created = await self.db_complete_course(course_id)
        
        if created:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'course_completed',
                    'message': f'You have completed {course_title}'
                }
            )

    async def course_enrolled(self, event):
        await self.send(text_data=json.dumps({
            'event': 'course_enrolled',
            'message': event['message']
        }))
    
    async def course_completed(self, event):
        await self.send(text_data=json.dumps({
            'event': 'course_completed',
            'message': event['message']
        }))
