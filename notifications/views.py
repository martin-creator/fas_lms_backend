from django.shortcuts import render
from django_ratelimit.decorators import ratelimit
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from notifications.models import Notification, NotificationSettings
from notifications.controllers.notification_controller import NotificationController



class NotificationViewSet(viewsets.ViewSet):
    """
    A viewset for viewing and editing notifications.
    """
    controller = NotificationController()

    def create(self, request):
        data = request.data
        notification = self.controller.create_notification(data)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        notification = self.controller.get_notification(pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def update(self, request, pk=None):
        data = request.data
        notification = self.controller.update_notification(pk, data)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        self.controller.delete_notification(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def user_notifications(self, request, user_id=None):
        notifications = self.controller.get_user_notifications(user_id)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def user_report(self, request, user_id=None):
        report = self.controller.generate_user_report(user_id)
        return Response(report)

    @action(detail=False, methods=['get'])
    def summary_report(self, request):
        report = self.controller.generate_summary_report()
        return Response(report)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        self.controller.mark_notification_as_read(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['put'])
    def update_settings(self, request, user_id=None):
        data = request.data
        settings = self.controller.update_notification_settings(user_id, data)
        serializer = NotificationSettingsSerializer(settings)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def settings(self, request, user_id=None):
        settings = self.controller.get_notification_settings(user_id)
        serializer = NotificationSettingsSerializer(settings)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_count(self, request, user_id=None):
        count = self.controller.get_unread_notifications_count(user_id)
        return Response({'unread_count': count})

    @action(detail=False, methods=['post'])
    def create_template(self, request):
        data = request.data
        template = self.controller.create_notification_template(data['notification_type'], data['template'])
        serializer = NotificationTemplateSerializer(template)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def template(self, request, notification_type=None):
        template = self.controller.get_notification_template(notification_type)
        return Response({'template': template})

    @action(detail=False, methods=['get'])
    def types(self, request):
        types = self.controller.get_notification_types()
        serializer = NotificationTypeSerializer(types, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_type(self, request):
        data = request.data
        notification_type = self.controller.create_notification_type(data)
        serializer = NotificationTypeSerializer(notification_type)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['put'])
    def update_type(self, request, notification_type_id=None):
        data = request.data
        notification_type = self.controller.update_notification_type(notification_type_id, data)
        serializer = NotificationTypeSerializer(notification_type)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def delete_type(self, request, notification_type_id=None):
        self.controller.delete_notification_type(notification_type_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        user = request.user
        notification_types = request.data.get('notification_types', [])
        self.controller.subscribe_to_notifications(user, notification_types)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        user = request.user
        notification_types = request.data.get('notification_types', [])
        self.controller.unsubscribe_from_notifications(user, notification_types)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def notify_followers(self, request):
        data = request.data
        self.controller.notify_followers(data['user_profile'], data['notification_type'], data.get('content_object'), data.get('content'), data.get('url'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def notify_all(self, request):
        data = request.data
        self.controller.notify_all_users(data['notification_type'], data.get('content_object'), data.get('content'), data.get('url'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def user_preferences(self, request, user_id=None):
        preferences = self.controller.get_user_preferences(user_id)
        serializer = UserNotificationPreferenceSerializer(preferences)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def update_preferences(self, request, user_id=None):
        data = request.data
        preferences = self.controller.update_user_preferences(user_id, data)
        serializer = UserNotificationPreferenceSerializer(preferences)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def snooze_notifications(self, request):
        data = request.data
        self.controller.snooze_notifications(request.user, data['start_time'], data['end_time'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def snooze_notification(self, request, notification_id=None):
        data = request.data
        self.controller.snooze_notification(notification_id, data['snooze_until'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def snoozed_notifications(self, request, user_id=None):
        snoozed_notifications = self.controller.get_snoozed_notifications(user_id)
        serializer = NotificationSerializer(snoozed_notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def log_engagement(self, request, notification_id=None):
        data = request.data
        self.controller.log_notification_engagement(notification_id, data['engagement_type'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def record_engagement(self, request, notification_id=None):
        data = request.data
        log_entry = self.controller.record_engagement(notification_id, data['engagement_type'])
        serializer = NotificationLogSerializer(log_entry)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def log_event(self, request, notification_id=None):
        data = request.data
        log_entry = self.controller.log_notification_event(notification_id, data['event_type'])
        serializer = NotificationLogSerializer(log_entry)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def assign_test(self, request):
        data = request.data
        test_group = self.controller.assign_user_to_test(data['user_id'], data['test_name'])
        return Response({'test_group': test_group})

    @action(detail=False, methods=['get'])
    def analyze_test(self, request, test_name=None):
        results = self.controller.analyze_ab_test_results(test_name)
        return Response(results)

    @action(detail=False, methods=['post'])
    def send_test_notification(self, request):
        data = request.data
        self.controller.send_test_notification(data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'])
    def send_test_multi_notification(self, request):
        data = request.data
        self.controller.send_test_multi_notification(data)
        return Response(status=status.HTTP_204_NO_CONTENT)
        

@ratelimit(key='user', rate='5/m', method='POST', block=True)
def send_notification_view(request):
    # Logic to send notification
    pass



def manage_notification_preferences(request):
    # Endpoint to manage user notification preferences
    pass

def set_do_not_disturb_mode(request):
    # Endpoint to set user's Do Not Disturb mode
    pass
