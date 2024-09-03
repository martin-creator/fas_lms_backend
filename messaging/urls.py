from django.urls import path
from . import views



urlpatterns = [
    path('messages/', views.get_messages, name='get_messages'),
    path('messages/<int:message_id>/', views.get_specific_message, name='get_specific_message'),
    path('messages/create/', views.create_message, name='create_message'),
    path('messages/update/<int:message_id>/', views.update_message, name='update_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/chat/<int:chat_id>/', views.get_messages_by_chat, name='get_messages_by_chat'),
    path('messages/sender/<int:sender_id>/', views.get_messages_by_sender, name='get_messages_by_sender'),
    path('messages/mark-read/<int:message_id>/', views.mark_message_as_read, name='mark_message_as_read'),
    path('messages/edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path('messages/delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('messages/replies/<int:message_id>/', views.get_reply_chain, name='get_reply_chain'),
    path('messages/preview/<int:message_id>/', views.get_preview, name='get_preview'),
    path('messages/reactions/<int:message_id>/', views.get_reactions_summary, name='get_reactions_summary'),
    path('messages/content/<int:message_id>/', views.get_content, name='get_content'),
    path('chat-rooms/', views.get_chat_rooms, name='get_chat_rooms'),
    path('chat-rooms/<int:chat_id>/', views.get_specific_chat_room, name='get_specific_chat_room'),
    path('chat-rooms/create/', views.create_chat_room, name='create_chat_room'),
    path('chat-rooms/update/<int:chat_id>/', views.update_chat_room, name='update_chat_room'),
    path('chat-rooms/delete/<int:chat_id>/', views.delete_chat_room, name='delete_chat_room'),
    path('chat-rooms/add-member/<int:chat_id>/<int:user_id>/', views.add_member_to_chat_room, name='add_member_to_chat_room'),
    path('chat-rooms/remove-member/<int:chat_id>/<int:user_id>/', views.remove_member_from_chat_room, name='remove_member_from_chat_room'),
    path('chat-rooms/members/<int:chat_id>/', views.get_chat_room_members, name='get_chat_room_members'),
    path('chat-rooms/messages-count/<int:chat_id>/', views.get_chat_room_messages_count, name='get_chat_room_messages_count'),
    path('chat-rooms/member-count/<int:chat_id>/', views.get_chat_room_members_count, name='get_chat_room_members_count'),
    path('chat-rooms/unread-messages-count/<int:chat_id>/', views.get_chat_room_unread_messages_count, name='get_chat_room_unread_messages_count'),
    path('chat-rooms/read-messages-count/<int:chat_id>/', views.get_chat_room_read_messages_count, name='get_chat_room_read_messages_count'),
    path('chat-rooms/notifications/<int:chat_id>/<int:user_id>/', views.get_chat_room_notifications, name='get_chat_room_notifications'),
    path('chat-rooms/mark-notification-read/<int:notification_id>/', views.mark_chat_room_notification_as_read, name='mark_chat_room_notification_as_read'),
    path('chat-rooms/create-notification/', views.create_chat_room_notification, name='create_chat_room_notification'),
    path('chat-rooms/unread-notifications/<int:chat_id>/<int:user_id>/', views.get_unread_notifications, name='get_unread_notifications'),
]