import redis

class PubSubService:
    @staticmethod
    def publish_notification(channel, message):
        r = redis.Redis()
        r.publish(channel, message)