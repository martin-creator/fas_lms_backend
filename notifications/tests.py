# notifications/tests.py

import pytest
from django.contrib.auth import get_user_model
from notifications.models import Notification

User = get_user_model()

@pytest.mark.django_db
def test_create_notification():
    user = User.objects.create_user(username='testuser', password='password')
    notification = Notification.objects.create(
        recipient=user,
        content='Test notification content',
        notification_type='info'
        # Add other required fields here
    )
    assert notification.id is not None

@pytest.mark.django_db
def test_notification_mark_as_read():
    user = User.objects.create_user(username='testuser', password='password')
    notification = Notification.objects.create(
        recipient=user,
        content='Test notification content',
        notification_type='info'
        # Add other required fields here
    )
    
    notification.mark_as_read()
    assert notification.is_read is True
    assert notification.read_at is not None

# Add more tests as per your model's functionality





# import pytest
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# from notifications.models import (
#     Notification,
#     NotificationType,
#     NotificationTemplate,
#     NotificationSettings,
#     NotificationReadStatus,
#     NotificationSnooze,
#     NotificationEngagement,
#     NotificationABTest,
#     NotificationLog
# )
# from profiles.models import UserProfile
# from notifications.tasks import (
#     send_notification_task,
#     log_notification_action_task,
#     archive_old_notifications_task,
#     send_bulk_notifications,
#     mark_notifications_as_read_task
# )

# User = get_user_model()


# @pytest.fixture
# def user():
#     user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
#     return user


# @pytest.fixture
# def notification_type():
#     type_name = 'Test Notification Type'
#     notification_type = NotificationType.objects.create(type_name=type_name)
#     return notification_type


# @pytest.fixture
# def notification_template(notification_type):
#     template = '<html><body>{{ content }}</body></html>'
#     notification_template = NotificationTemplate.objects.create(notification_type=notification_type, template=template)
#     return notification_template


# @pytest.fixture
# def notification_settings(user, notification_type):
#     notification_settings = NotificationSettings.objects.create(user=user, notification_type=notification_type, is_enabled=True)
#     return notification_settings


# @pytest.fixture
# def notification(user, notification_type):
#     notification = Notification.objects.create(
#         recipient=user,
#         notification_type=notification_type,
#         content='Test notification content',
#         timestamp=timezone.now(),
#         is_read=False
#     )
#     return notification


# @pytest.fixture
# def notification_read_status(user, notification):
#     notification_read_status = NotificationReadStatus.objects.create(user=user, notification=notification, is_read=False)
#     return notification_read_status


# @pytest.fixture
# def notification_snooze(user):
#     start_time = timezone.now()
#     end_time = start_time + timezone.timedelta(days=1)
#     notification_snooze = NotificationSnooze.objects.create(user=user, start_time=start_time, end_time=end_time)
#     return notification_snooze


# @pytest.fixture
# def notification_engagement(user, notification):
#     notification_engagement = NotificationEngagement.objects.create(
#         user=user,
#         notification=notification,
#         viewed_at=timezone.now(),
#         clicked_at=None,
#         interaction_type='view'
#     )
#     return notification_engagement


# @pytest.fixture
# def notification_ab_test(notification_template):
#     start_date = timezone.now()
#     end_date = start_date + timezone.timedelta(days=7)
#     notification_ab_test = NotificationABTest.objects.create(
#         test_name='Test A/B Test',
#         variant='A',
#         notification_template=notification_template,
#         start_date=start_date,
#         end_date=end_date
#     )
#     return notification_ab_test


# @pytest.fixture
# def notification_log(user, notification):
#     notification_log = NotificationLog.objects.create(
#         notification=notification,
#         action='created',
#         performed_by=user
#     )
#     return notification_log


# @pytest.mark.django_db
# def test_notification_creation(notification):
#     assert Notification.objects.count() == 1
#     assert notification.recipient.username == 'testuser'
#     assert notification.notification_type.type_name == 'Test Notification Type'


# @pytest.mark.django_db
# def test_notification_settings(notification_settings):
#     assert NotificationSettings.objects.count() == 1
#     assert notification_settings.user.username == 'testuser'
#     assert notification_settings.notification_type.type_name == 'Test Notification Type'
#     assert notification_settings.is_enabled is True


# @pytest.mark.django_db
# def test_notification_read_status(notification_read_status):
#     assert NotificationReadStatus.objects.count() == 1
#     assert notification_read_status.user.username == 'testuser'
#     assert notification_read_status.notification.content == 'Test notification content'
#     assert notification_read_status.is_read is False


# @pytest.mark.django_db
# def test_notification_snooze(notification_snooze):
#     assert NotificationSnooze.objects.count() == 1
#     assert notification_snooze.user.username == 'testuser'
#     assert notification_snooze.start_time.date() == timezone.now().date()


# @pytest.mark.django_db
# def test_notification_engagement(notification_engagement):
#     assert NotificationEngagement.objects.count() == 1
#     assert notification_engagement.user.username == 'testuser'
#     assert notification_engagement.notification.content == 'Test notification content'
#     assert notification_engagement.interaction_type == 'view'


# @pytest.mark.django_db
# def test_notification_ab_test(notification_ab_test):
#     assert NotificationABTest.objects.count() == 1
#     assert notification_ab_test.test_name == 'Test A/B Test'
#     assert notification_ab_test.notification_template.notification_type.type_name == 'Test Notification Type'


# @pytest.mark.django_db
# def test_notification_log(notification_log):
#     assert NotificationLog.objects.count() == 1
#     assert notification_log.notification.content == 'Test notification content'
#     assert notification_log.action == 'created'
#     assert notification_log.performed_by.username == 'testuser'


# @pytest.mark.django_db
# def test_send_notification_task(notification):
#     send_notification_task(notification.id)
#     # Verify notification sending logic here (e.g., check logs, external service mocks, etc.)
#     # Add assertions based on actual implementation or mock responses


# @pytest.mark.django_db
# def test_log_notification_action_task(notification):
#     log_notification_action_task(notification.id, action='updated')
#     # Verify notification action logging logic here (e.g., check NotificationLog entries, etc.)
#     # Add assertions based on actual implementation or mock responses


# @pytest.mark.django_db
# def test_archive_old_notifications_task(notification):
#     notification.timestamp = timezone.now() - timezone.timedelta(days=366)  # Set notification older than 1 year
#     notification.save()
#     archive_old_notifications_task()
#     assert Notification.objects.filter(id=notification.id, is_archived=True).exists()


# @pytest.mark.django_db
# def test_send_bulk_notifications(user):
#     user_ids = [user.id]
#     notification_data = {
#         'content': 'Bulk notification content',
#         'notification_type': 'Test Notification Type',
#         'timestamp': timezone.now(),
#         'is_read': False
#     }
#     send_bulk_notifications(user_ids, notification_data)
#     assert Notification.objects.filter(recipient_id=user.id, content='Bulk notification content').exists()


# @pytest.mark.django_db
# def test_mark_notifications_as_read_task(notification):
#     notification_ids = [notification.id]
#     mark_notifications_as_read_task(notification.recipient_id, notification_ids)
#     updated_notification = Notification.objects.get(id=notification.id)
#     assert updated_notification.is_read is True
#     assert updated_notification.read_at is not None
#     assert NotificationReadStatus.objects.filter(user_id=notification.recipient_id, notification_id=notification.id, is_read=True).exists()

# # Add more tests as needed to cover additional functionality and edge cases.

