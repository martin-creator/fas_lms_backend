

# settings/logging_settings.py

from config.constances import LOGGING_SETTINGS, ERROR_HANDLING

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': LOGGING_SETTINGS['LOG_LEVEL'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGGING_SETTINGS['LOG_FILE'],
            'maxBytes': LOGGING_SETTINGS['MAX_BYTES'],
            'backupCount': LOGGING_SETTINGS['BACKUP_COUNT'],
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'notifications': {
            'handlers': ['file'],
            'level': LOGGING_SETTINGS['LOG_LEVEL'],
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
}

ERROR_HANDLING_CONFIG = {
    'RETRY_COUNT': ERROR_HANDLING['RETRY_COUNT'],
    'RETRY_DELAY_SECONDS': ERROR_HANDLING['RETRY_DELAY_SECONDS'],
}
