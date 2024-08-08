# notifications/utils/notification_utils.py

import logging
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from notifications.querying.notification_query import NotificationQueryService
from notifications.reports.notification_report import generate_user_notification_report, generate_notification_summary
from notifications.utils.permissions import PermissionChecker
from notifications.utils.notification_validation import NotificationsValidator
from notifications.services.pubsub_service import PubSubService
from notifications.services.crm_integration import send_crm_alert
from notifications.services.alert_system_integration import send_external_alert
from notifications.settings.config.constances import NOTIFICATION_CHANNELS
from notifications.metrics import increment_notifications_sent, increment_notifications_failed
from django.utils.translation import gettext_lazy as _
import random
from django.apps import apps


logger = logging.getLogger(__name__)

class NotificationUtils:

    @staticmethod
    def get_model(model_name):
        return apps.get_model('notifications', model_name)

    @staticmethod
    def send_notification(data):
        from profiles.models import UserProfile
        from notifications.serializers import NotificationSerializer
        from notifications.utils.delivery_method import DeliveryMethod

        user = UserProfile.objects.get(id=data['recipient'])
        
        if not PermissionChecker.user_can_manage_notifications(user):
            raise PermissionDenied(_("You do not have permission to send notifications."))
        
        if not NotificationsValidator.validate_notification_permissions(user, data['notification_type']):
            raise PermissionDenied(_("User does not have permission to receive this notification."))

        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            delivery_method = data.get('delivery_method', DeliveryMethod.PUSH.value)
            NotificationUtils._dispatch_notification(notification, delivery_method)

            if data.get('notify_crm'):
                send_crm_alert(user.id, data['event_type'], data['event_data'])
            if data.get('notify_alert_system'):
                send_external_alert(user.id, data['alert_type'], data['message'])

            PubSubService.publish_notification(notification)
            increment_notifications_sent()
            return notification
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def _dispatch_notification(notification, delivery_method):
        from notifications.utils.delivery_method import DeliveryMethod

        try:
            delivery_function = getattr(DeliveryMethod, f'send_{delivery_method.lower()}_notification')
            delivery_function(notification)
        except AttributeError:
            raise ValueError(_("Invalid delivery method."))

    @staticmethod
    def _handle_error(e, data):
        increment_notifications_failed()
        NotificationsValidator.handle_notification_failure(data, str(e))
        raise

    @staticmethod
    def mark_notification_as_read(notification_id):
        Notification = NotificationUtils.get_model('Notification')
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

    @staticmethod
    def delete_notification(notification_id):
        Notification = NotificationUtils.get_model('Notification')
        Notification.objects.filter(id=notification_id).delete()

    @staticmethod
    def get_notification(notification_id):
        from notifications.serializers import NotificationSerializer
        
        Notification = NotificationUtils.get_model('Notification')
        notification = Notification.objects.get(id=notification_id)
        serializer = NotificationSerializer(notification)
        return serializer.data

    @staticmethod
    def update_notification(notification_id, data):
        from notifications.serializers import NotificationSerializer

        Notification = NotificationUtils.get_model('Notification')
        notification = Notification.objects.get(id=notification_id)
        serializer = NotificationSerializer(notification, data=data)
        if serializer.is_valid():
            updated_notification = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def get_user_notifications(user_id):
        from notifications.serializers import NotificationSerializer
        
        notifications = NotificationQueryService.get_notifications_by_user(user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return serializer.data

    @staticmethod
    def generate_user_report(user_id):
        return generate_user_notification_report(user_id)

    @staticmethod
    def generate_summary_report():
        return generate_notification_summary()

    @staticmethod
    def update_notification_settings(user_id, settings_data):
        from notifications.serializers import NotificationSettingsSerializer

        NotificationSettings = NotificationUtils.get_model('NotificationSettings')
        settings, created = NotificationSettings.objects.get_or_create(user_id=user_id)
        serializer = NotificationSettingsSerializer(settings, data=settings_data)
        if serializer.is_valid():
            updated_settings = serializer.save()
            cache_key = f"notification_settings_{user_id}"
            cache.set(cache_key, updated_settings, timeout=3600)
            return updated_settings
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def get_notification_settings(user_id):
        from notifications.serializers import NotificationSettingsSerializer
        
        NotificationSettings = NotificationUtils.get_model('NotificationSettings')
        cache_key = f"notification_settings_{user_id}"
        settings = cache.get(cache_key)
        if not settings:
            settings = NotificationSettings.objects.get(user_id=user_id)
            cache.set(cache_key, settings, timeout=3600)
        serializer = NotificationSettingsSerializer(settings)
        return serializer.data

    @staticmethod
    def get_unread_notifications_count(user):
        count = NotificationQueryService.get_unread_notifications_count(user.id)
        return {'unread_count': count}

    @staticmethod
    def create_notification_template(notification_type, template):
        from notifications.serializers import NotificationTemplateSerializer
        
        NotificationTemplate = NotificationUtils.get_model('NotificationTemplate')
        template_obj, created = NotificationTemplate.objects.get_or_create(notification_type=notification_type)
        template_obj.template = template
        template_obj.save()
        serializer = NotificationTemplateSerializer(template_obj)
        return serializer.data

    @staticmethod
    def update_notification_template(template_id, data):
        from notifications.serializers import NotificationTemplateSerializer
        
        NotificationTemplate = NotificationUtils.get_model('NotificationTemplate')
        template = NotificationTemplate.objects.get(id=template_id)
        serializer = NotificationTemplateSerializer(template, data=data)
        if serializer.is_valid():
            updated_template = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def get_notification_template(notification_type):
        from notifications.serializers import NotificationTemplateSerializer
        
        NotificationTemplate = NotificationUtils.get_model('NotificationTemplate')
        try:
            template = NotificationTemplate.objects.get(notification_type=notification_type)
            serializer = NotificationTemplateSerializer(template)
            return serializer.data
        except NotificationTemplate.DoesNotExist:
            return None

    @staticmethod
    def get_notification_types():
        from notifications.serializers import NotificationTypeSerializer
        
        NotificationType = NotificationUtils.get_model('NotificationType')
        notification_types = NotificationType.objects.all()
        serializer = NotificationTypeSerializer(notification_types, many=True)
        return serializer.data

    @staticmethod
    def create_notification_type(data):
        from notifications.serializers import NotificationTypeSerializer
        
        NotificationType = NotificationUtils.get_model('NotificationType')
        serializer = NotificationTypeSerializer(data=data)
        if serializer.is_valid():
            notification_type = serializer.save()
            return notification_type
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def update_notification_type(notification_type_id, data):
        from notifications.serializers import NotificationTypeSerializer
        
        NotificationType = NotificationUtils.get_model('NotificationType')
        notification_type = NotificationType.objects.get(id=notification_type_id)
        serializer = NotificationTypeSerializer(notification_type, data=data)
        if serializer.is_valid():
            updated_notification_type = serializer.save()
            return serializer.data
        else:
            raise ValueError(serializer.errors)

    @staticmethod
    def delete_notification_type(notification_type_id):
        NotificationType = NotificationUtils.get_model('NotificationType')
        NotificationType.objects.filter(id=notification_type_id).delete()

    @staticmethod
    def subscribe_to_notifications(user, notification_types):
        from notifications.serializers import NotificationSettingsSerializer
        
        NotificationSettings = NotificationUtils.get_model('NotificationSettings')
        subscribed_settings = []
        for notification_type in notification_types:
            setting, created = NotificationSettings.objects.get_or_create(user=user, notification_type=notification_type, defaults={'is_enabled': True})
            serializer = NotificationSettingsSerializer(setting)
            subscribed_settings.append(serializer.data)
        return subscribed_settings

    @staticmethod
    def unsubscribe_from_notifications(user, notification_types):
        from notifications.serializers import NotificationSettingsSerializer
        
        NotificationSettings = NotificationUtils.get_model('NotificationSettings')
        settings_to_delete = NotificationSettings.objects.filter(user=user, notification_type__in=notification_types)
        serialized_settings = NotificationSettingsSerializer(settings_to_delete, many=True).data
        settings_to_delete.delete()
        return serialized_settings

    @staticmethod
    def notify_followers(user_profile, notification_type, content_object=None, content='', url=''):
        from notifications.serializers import NotificationSerializer
        
        followers = user_profile.followers.all()
        notifications = []
        for follower in followers:
            notification_data = {
                'recipient': follower.id,
                'notification_type': notification_type.id,
                'content_object': content_object.id if content_object else None,
                'content': content,
                'url': url,
                'is_read': False
            }
            serializer = NotificationSerializer(data=notification_data)
            if serializer.is_valid():
                notification = serializer.save()
                notifications.append(serializer.data)
            else:
                raise ValueError(serializer.errors)
        return notifications

    @staticmethod
    def notify_all_users(notification_type, content_object=None, content='', url=''):
        from profiles.models import UserProfile
        from notifications.serializers import NotificationSerializer
        
        all_users = UserProfile.objects.all()
        notifications = []
        for user in all_users:
            notification_data = {
                'recipient': user.id,
                'notification_type': notification_type.id,
                'content_object': content_object.id if content_object else None,
                'content': content,
                'url': url,
                'is_read': False
            }
            serializer = NotificationSerializer(data=notification_data)
            if serializer.is_valid():
                notification = serializer.save()
                notifications.append(serializer.data)
            else:
                raise ValueError(serializer.errors)
        return notifications

    @staticmethod
    def get_user_preferences(user):
        from notifications.serializers import UserNotificationPreferenceSerializer
        
        UserNotificationPreference = NotificationUtils.get_model('UserNotificationPreference')
        preferences = UserNotificationPreference.objects.filter(user=user)
        serializer = UserNotificationPreferenceSerializer(preferences, many=True)
        return serializer.data

    @staticmethod
    def update_user_preferences(user, preferences_data):
        from notifications.serializers import UserNotificationPreferenceSerializer
        
        UserNotificationPreference = NotificationUtils.get_model('UserNotificationPreference')
        for preference in preferences_data:
            pref_obj, created = UserNotificationPreference.objects.update_or_create(
                user=user,
                notification_type=preference['notification_type'],
                defaults={'is_enabled': preference['is_enabled'], 'frequency': preference['frequency']}
            )
        return NotificationUtils.get_user_preferences(user)

    @staticmethod
    def snooze_notifications(user, start_time, end_time):
        NotificationSnooze = NotificationUtils.get_model('NotificationSnooze')
        NotificationSnooze.objects.create(user=user, start_time=start_time, end_time=end_time)

    @staticmethod
    def snooze_notification(notification_id, snooze_until):
        Notification = NotificationUtils.get_model('Notification')
        NotificationSnooze = NotificationUtils.get_model('NotificationSnooze')
        notification = Notification.objects.get(id=notification_id)
        NotificationSnooze.objects.update_or_create(
            notification=notification,
            defaults={'snooze_until': snooze_until}
        )

    @staticmethod
    def is_user_snoozed(user):
        NotificationSnooze = NotificationUtils.get_model('NotificationSnooze')
        snooze = NotificationSnooze.objects.filter(user=user, end_time__gte=timezone.now()).exists()
        return snooze

    @staticmethod
    def get_snoozed_notifications(user):
        from notifications.serializers import NotificationSerializer
        
        NotificationSnooze = NotificationUtils.get_model('NotificationSnooze')
        Notification = NotificationUtils.get_model('Notification')
        snoozed_notifications = NotificationSnooze.objects.filter(user=user, end_time__gte=timezone.now())
        notifications = [snooze.notification for snooze in snoozed_notifications]
        return NotificationSerializer(notifications, many=True).data

    @staticmethod
    def log_notification_engagement(notification_id, engagement_type):
        Notification = NotificationUtils.get_model('Notification')
        NotificationEngagement = NotificationUtils.get_model('NotificationEngagement')
        notification = Notification.objects.get(id=notification_id)
        NotificationEngagement.objects.create(notification=notification, engagement_type=engagement_type)

    @staticmethod
    def record_engagement(notification_id, engagement_type):
        Notification = NotificationUtils.get_model('Notification')
        NotificationLog = NotificationUtils.get_model('NotificationLog')
        notification = Notification.objects.get(id=notification_id)
        log_entry = NotificationLog(notification=notification, engagement_type=engagement_type, timestamp=timezone.now())
        log_entry.save()
        return log_entry

    @staticmethod
    def log_notification_event(notification_id, event_type):
        Notification = NotificationUtils.get_model('Notification')
        NotificationLog = NotificationUtils.get_model('NotificationLog')
        notification = Notification.objects.get(id=notification_id)
        log_entry = NotificationLog(notification=notification, event_type=event_type, timestamp=timezone.now())
        log_entry.save()
        return log_entry

    @staticmethod
    def assign_user_to_test(user_id, test_name):
        test_group = random.choice(['A', 'B'])
        # Record user's test group assignment in database or cache
        return test_group

    @staticmethod
    def analyze_ab_test_results(test_name):
        # Perform analysis of A/B test results and return the findings
        pass

    @staticmethod
    def send_test_notification(data):
        data['content'] = _('This is a test notification.')
        data['html_content'] = '<p>This is a <strong>test</strong> notification.</p>'
        NotificationUtils.send_notification(data)

    @staticmethod
    def send_test_multi_notification(data):
        data['content'] = _('This is a test notification.')
        data['html_content'] = '<p>This is a <strong>test</strong> notification.</p>'
        NotificationUtils.send_notification(data)