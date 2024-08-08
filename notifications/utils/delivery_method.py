# notifications/utils/delivery_method.py

from enum import Enum
import logging

logger = logging.getLogger(__name__)

class DeliveryMethod(Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    IN_APP = "IN_APP"
    
    @staticmethod
    def notify(notification):
        from notifications.services.pubsub_service import PubSubService
        
        method = notification.delivery_method
        if method == DeliveryMethod.EMAIL.name:
            PubSubService.send_email_notification(notification)
        elif method == DeliveryMethod.SMS.name:
            PubSubService.send_sms_notification(notification)
        elif method == DeliveryMethod.PUSH.name:
            PubSubService.send_push_notification(notification.id)
        elif method == DeliveryMethod.IN_APP.name:
            PubSubService.send_in_app_notification(notification)
        
        # Publish to Redis and send WebSocket notification
        pubsub_service = PubSubService()
        pubsub_service.publish_notification('notifications', notification)
        PubSubService.send_websocket_notification(notification)