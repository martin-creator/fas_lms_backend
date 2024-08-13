# notifications/metrics.py
from prometheus_client import Counter

notifications_sent = Counter('notifications_sent', 'Total number of notifications sent')
notifications_failed = Counter('notifications_failed', 'Total number of notifications failed')

def increment_notifications_sent():
    notifications_sent.inc()

def increment_notifications_failed():
    notifications_failed.inc()
