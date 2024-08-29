import logging
from django.core.exceptions import PermissionDenied
from profiles.models import UserProfile
from chat.models import ChatRoom

logger = logging.getLogger(__name__)

class PermissionChecker:

    @staticmethod
    def user_can_manage_notifications(user):
        return user.is_staff

    @staticmethod
    def user_can_send_message(user, chat):
        if chat.is_private and user not in chat.members.all():
            raise PermissionDenied("You do not have permission to send messages to this chat.")
        return True

    @staticmethod
    def user_can_view_chat(user, chat):
        if chat.is_private and user not in chat.members.all():
            raise PermissionDenied("You do not have permission to view this chat.")
        return True