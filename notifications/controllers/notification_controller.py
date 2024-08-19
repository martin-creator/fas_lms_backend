from notifications.services.notification_service import NotificationService

class NotificationController:
    
    def __init__(self):
        self.notification_service = NotificationService()

    def create_notification(self, data):
        return self.notification_service.send_notification(data)

    def get_notification(self, notification_id):
        return self.notification_service.get(notification_id)

    def update_notification(self, notification_id, data):
        return self.notification_service.update(notification_id, data)

    def delete_notification(self, notification_id):
        self.notification_service.delete(notification_id)

    def mark_notification_as_read(self, notification_id):
        self.notification_service.mark_as_read(notification_id)

    def get_user_notifications(self, user_id):
        return self.notification_service.get_user_notifications(user_id)

    def generate_user_report(self, user_id):
        return self.notification_service.generate_user_report(user_id)

    def generate_summary_report(self):
        return self.notification_service.generate_summary_report()

    def update_notification_settings(self, user_id, settings_data):
        return self.notification_service.update_settings(user_id, settings_data)

    def get_notification_settings(self, user_id):
        return self.notification_service.get_settings(user_id)
        
    def get_unread_notifications_count(self, user):
        return self.notification_service.get_unread_count(user)

    def create_notification_template(self, notification_type, template):
        return self.notification_service.create_template(notification_type, template)

    def update_notification_template(self, template_id, data):
        return self.notification_service.update_template(template_id, data)

    def get_notification_template(self, notification_type):
        return self.notification_service.get_template(notification_type)

    def get_notification_types(self):
        return self.notification_service.get_types()

    def create_notification_type(self, data):
        return self.notification_service.create_type(data)

    def update_notification_type(self, notification_type_id, data):
        return self.notification_service.update_type(notification_type_id, data)

    def delete_notification_type(self, notification_type_id):
        self.notification_service.delete_type(notification_type_id)

    def subscribe_to_notifications(self, user, notification_types):
        return self.notification_service.subscribe(user, notification_types)

    def unsubscribe_from_notifications(self, user, notification_types):
        return self.notification_service.unsubscribe(user, notification_types)

    def notify_followers(self, user_profile, notification_type, content_object=None, content='', url=''):
        return self.notification_service.notify_followers(user_profile, notification_type, content_object, content, url)

    def notify_all_users(self, notification_type, content_object=None, content='', url=''):
        return self.notification_service.notify_all_users(notification_type, content_object, content, url)

    def get_user_preferences(self, user):
        return self.notification_service.get_user_preferences(user)

    def update_user_preferences(self, user, preferences_data):
        return self.notification_service.update_preferences(user, preferences_data)

    def snooze_notifications(self, user, start_time, end_time):
        return self.notification_service.snooze_notifications(user, start_time, end_time)

    def snooze_notification(self, notification_id, snooze_until):
        return self.notification_service.snooze_notification(notification_id, snooze_until)

    def is_user_snoozed(self, user):
        return self.notification_service.is_user_snoozed(user)

    def get_snoozed_notifications(self, user):
        return self.notification_service.get_snoozed_notifications(user)

    def log_notification_engagement(self, notification_id, engagement_type):
        return self.notification_service.log_notification_engagement(notification_id, engagement_type)

    def record_engagement(self, notification_id, engagement_type):
        return self.notification_service.record_engagement(notification_id, engagement_type)

    def log_notification_event(self, notification_id, event_type):
        return self.notification_service.log_notification_event(notification_id, event_type)

    def assign_user_to_test(self, user_id, test_name):
        return self.notification_service.assign_user_to_test(user_id, test_name)

    def analyze_ab_test_results(self, test_name):
        return self.notification_service.analyze_ab_test_results(test_name)

    def send_test_notification(self, data):
        return self.notification_service.send_test_notification(data)

    def send_test_multi_notification(self, data):
        return self.notification_service.send_test_multi_notification(data)
