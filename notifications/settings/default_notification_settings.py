


from config.constances import NOTIFICATION_TYPES, NOTIFICATION_CHANNELS

DEFAULT_NOTIFICATION_SETTINGS = {
    'NEW_MESSAGE': {
        'enabled': True,
        'channels': [NOTIFICATION_CHANNELS['EMAIL'], NOTIFICATION_CHANNELS['PUSH']],
    },
    'FRIEND_REQUEST': {
        'enabled': True,
        'channels': [NOTIFICATION_CHANNELS['IN_APP']],
    },
    'EVENT_REMINDER': {
        'enabled': True,
        'channels': [NOTIFICATION_CHANNELS['EMAIL'], NOTIFICATION_CHANNELS['SMS'], NOTIFICATION_CHANNELS['PUSH']],
    },
    # Add defaults for other notification types
}