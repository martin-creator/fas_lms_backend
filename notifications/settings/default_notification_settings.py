

DEFAULT_NOTIFICATION_SETTINGS = {
    'NEW_MESSAGE': {
        'enabled': True,
        'channels': ['EMAIL', 'PUSH'],
    },
    'FRIEND_REQUEST': {
        'enabled': True,
        'channels': ['IN_APP'],
    },
    'EVENT_REMINDER': {
        'enabled': True,
        'channels': ['EMAIL', 'SMS', 'PUSH'],
    },
    # Add defaults for other notification types
}