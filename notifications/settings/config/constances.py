# notifications/settings/config/constances.py

from django.utils.translation import gettext_lazy as _


NOTIFICATION_PRIORITY = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
    (4, 'Critical'),
]

DEFAULT_NOTIFICATION_TYPE = [
    ('job_application', 'Job Application'),
    ('job_listing', 'Job Listing'),
    ('message', 'Message'),
    ('follow', 'Follow'),
    ('connection', 'Connection'),
    ('reaction', 'Reaction'),
    ('post', 'Posts'),
    ('share', 'Share'),
    ('tag', 'Tag'),
    ('comment', 'Comment'),
    ('endorsement', 'Endorsement'),
    ('skill', 'Skill'),
    ('experience', 'Experience'),
    ('education', 'Education'),
    ('group', 'Group'),
]

DEFAULT_LANGUAGE_TYPES = [
    ('en', _('English')), 
    ('es', _('Spanish')), 
    ('fr', _('French')),
]

SEVERITY_CHOICES = [
    ('info', _('Info')),
    ('warning', _('Warning')),
    ('alert', _('Alert')),
]

INTERACTION_TYPE = [
    ('view', 'View'),
    ('click', 'Click'),
    ('dismiss', 'Dismiss')
]

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
    'WEEKLY_DIGEST': 'Weekly Digest',
    # Add more frequency options as needed
}

# Example for Do Not Disturb settings
DO_NOT_DISTURB = {
    'START_TIME': '22:00',
    'END_TIME': '08:00',
}