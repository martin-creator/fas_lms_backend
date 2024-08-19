# notifications/utils/delivery_method.py

from enum import Enum
from django.utils.translation import gettext as _
import logging

logger = logging.getLogger(__name__)

class DeliveryMethod(Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"

class DeliveryMethodHandler:
    def __init__(self):
        from notifications.services.pubsub_service import PubSubService
        self._pubsub_service = PubSubService()
        self._method_function_map = {
            DeliveryMethod.EMAIL.name: self._pubsub_service.send_email_notification,
            DeliveryMethod.SMS.name: self._pubsub_service.send_sms_notification,
            DeliveryMethod.PUSH.name: self._pubsub_service.send_push_notification,
            DeliveryMethod.IN_APP.name: self._pubsub_service.send_in_app_notification,
        }

    def dispatch(self, notification, method):
        """
        Dispatch the notification based on the specified delivery method.

        Args:
            notification (Notification): The notification object.
            method (str): The delivery method as a string.
        """
        func = self._method_function_map.get(method)
        if func:
            func(notification)


    def notify(self, notification):
        """
        Handle notification dispatch and real-time notifications.

        Args:
            notification (Notification): The notification object.
        """
        delivery_method = notification.delivery_method
        self.dispatch(notification, delivery_method)