
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

