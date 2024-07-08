from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class NotificationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        Notification.objects.create(user=self.user, message="Test notification")

    def test_notification_creation(self):
        notification = Notification.objects.get(user=self.user)
        self.assertEqual(notification.message, "Test notification")

    def test_notification_list_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get('/notifications/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test notification")
