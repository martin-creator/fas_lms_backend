
NOTIFICATION_TYPES = {
    'NEW_MESSAGE': 'New Message',
    'FRIEND_REQUEST': 'Friend Request',
    'EVENT_REMINDER': 'Event Reminder',
    # Add more notification types as needed
}

NOTIFICATION_CHANNELS = {
    'EMAIL': 'Email',
    'SMS': 'SMS',
    'PUSH': 'Push Notification',
    'IN_APP': 'In-App Notification',
    # Add more channels as needed
}

LOGGING_SETTINGS = {
    'LOG_LEVEL': 'DEBUG',
    'LOG_FILE': '/path/to/notifications_app/logs/notifications.log',
    'MAX_BYTES': 1024 * 1024,  # 1 MB
    'BACKUP_COUNT': 5,
}

# Example for error handling and retries
ERROR_HANDLING = {
    'RETRY_COUNT': 3,
    'RETRY_DELAY_SECONDS': 5,
}


NOTIFICATION_FREQUENCY = {
    'IMMEDIATE': 'Immediate',
    'HOURLY_DIGEST': 'Hourly Digest',
    'DAILY_DIGEST': 'Daily Digest',
    # Add more frequency options as needed
}

# Example for Do Not Disturb settings
DO_NOT_DISTURB = {
    'START_TIME': '22:00',
    'END_TIME': '08:00',
}