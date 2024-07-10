from connections.models import ConnectionRequest, Connection, Recommendation
from profiles.models import UserProfile


class ConnectionsController:
    def __init__(self):
        pass

    def send_connection_request(self, from_user, to_user):
        connection_request = ConnectionRequest(
            from_user=from_user,
            to_user=to_user,
        )
        connection_request.save()
        return connection_request

    def accept_connection_request(self, request_id):
        connection_request = ConnectionRequest.objects.get(id=request_id)
        connection_request.accept()
        return connection_request

    def reject_connection_request(self, request_id):
        connection_request = ConnectionRequest.objects.get(id=request_id)
        connection_request.reject()
        return connection_request

    def get_user_connections(self, user_id):
        user = UserProfile.objects.get(id=user_id)
        return user.connections.all()

    def recommend_user(self, recommended_by, recommended_user, content):
        recommendation = Recommendation(
            recommended_by=recommended_by,
            recommended_user=recommended_user,
            content=content,
        )
        recommendation.save()
        return recommendation
