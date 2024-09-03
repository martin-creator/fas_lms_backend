from django.db.models import Count, Q
from connections.models import ConnectionRequest, Connection
from connections.serializers import ConnectionRequestSerializer, ConnectionSerializer
from django.utils import timezone


class ConnectionQuery:
    # connection queries
    @staticmethod
    def get_connection_requests():
        """
        Get all connection requests.
        """
        connection_requests = ConnectionRequest.objects.all()
        serializer = ConnectionRequestSerializer(connection_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_connection_request(request_id):
        """
        Get a specific connection request.
        """
        connection_request = ConnectionRequest.objects.get(id=request_id)
        serializer = ConnectionRequestSerializer(connection_request)
        return serializer.data
    

    @staticmethod
    def get_connection_requests_by_user(user_id):
        """
        Get all connection requests sent to a specific user.
        """
        connection_requests = ConnectionRequest.objects.filter(to_user=user_id)
        serializer = ConnectionRequestSerializer(connection_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_connection_requests_by_status(status):
        """
        Get all connection requests with a specific status.
        """
        connection_requests = ConnectionRequest.objects.filter(status=status)
        serializer = ConnectionRequestSerializer(connection_requests, many=True)
        return serializer.data
    

    @staticmethod
    def get_connections():
        """
        Get all connections.
        """
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        return serializer.data
    

    @staticmethod
    def get_connection(connection_id):
        """
        Get a specific connection.
        """
        connection = Connection.objects.get(id=connection_id)
        serializer = ConnectionSerializer(connection)
        return serializer.data
    

    @staticmethod
    def get_connections_by_user(user_id):
        """
        Get all connections for a specific user.
        """
        connections = Connection.objects.filter(Q(user=user_id) | Q(connection=user_id))
        serializer = ConnectionSerializer(connections, many=True)
        return serializer.data
    

    @staticmethod
    def get_connections_by_status(status):
        """
        Get all connections with a specific status.
        """
        connections = Connection.objects.filter(status=status)
        serializer = ConnectionSerializer(connections, many=True)
        return serializer.data
    

    @staticmethod
    def delete_connection_request(request_id):
        """
        Delete a connection request.
        """
        connection_request = ConnectionRequest.objects.get(id=request_id)
        connection_request.delete()

        return True
    

    @staticmethod
    def delete_connection(connection_id):
        """
        Delete a connection.
        """
        connection = Connection.objects.get(id=connection_id)
        connection.delete()

        return True
    

    @staticmethod
    def delete_all_connection_requests():
        """
        Delete all connection requests.
        """
        connection_requests = ConnectionRequest.objects.all()
        connection_requests.delete()

        return True
    

    @staticmethod
    def delete_all_connections():
        """
        Delete all connections.
        """
        connections = Connection.objects.all()
        connections.delete()

        return True

