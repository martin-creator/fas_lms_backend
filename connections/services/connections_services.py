from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from connections.models import ConnectionRequest, Connection
from connections.serializers import ConnectionRequestSerializer, ConnectionSerializer
from connections.querying.connections_query import ConnectionQuery
from connections.helpers.connections_helpers import ConnectionHelpers
from connections.utils import UserUtils
from connections.reports.connections_report import ConnectionReport
from connections.settings.connections_settings import ConnectionsSettings


# generate CRUD services for both Connection and ConnectionRequest models
# also add user services for user connections and connection requests

class ConnectionService:
    # connection services
    @staticmethod
    def get_connections():
        """
        Get all connections.
        """
        connections = ConnectionQuery.get_connections()
        return connections
    
    @staticmethod
    def get_connection(connection_id):
        """
        Get a specific connection.
        """
        connection = ConnectionQuery.get_connection(connection_id)
        return connection
    
    @staticmethod
    def create_connection(connection_data):
        """
        Create a new connection.
        """
        connection = ConnectionHelpers.process_connection_data(connection_data)
        connection.save()
        
        serializer = ConnectionSerializer(connection)
        
        return serializer.data
    
    @staticmethod
    def update_connection(connection_id, connection_data):
        """
        Update a connection.
        """
        connection = ConnectionQuery.get_connection(connection_id)
        connection = ConnectionHelpers.process_connection_data(connection, connection_data)
        connection.save()
        
        serializer = ConnectionSerializer(connection)
        
        return serializer.data
    
    @staticmethod
    def delete_connection(connection_id):
        """
        Delete a connection.
        """
        connection = ConnectionQuery.get_connection(connection_id)
        connection.delete()
        
        return True
    
    @staticmethod
    def delete_all_connections():
        """
        Delete all connections.
        """
        connections = ConnectionQuery.get_connections()
        connections.delete()
        
        return True
    

    # connection request services
    @staticmethod
    def get_connection_requests():
        """
        Get all connection requests.
        """
        connection_requests = ConnectionQuery.get_connection_requests()
        return connection_requests
    
    @staticmethod
    def get_connection_request(request_id):
        """
        Get a specific connection request.
        """
        connection_request = ConnectionQuery.get_connection_request(request_id)
        return connection_request
    
    @staticmethod
    def create_connection_request(request_data):
        """
        Create a new connection request.
        """
        connection_request = ConnectionHelpers.process_connection_request_data(request_data)
        connection_request.save()
        
        serializer = ConnectionRequestSerializer(connection_request)
        
        return serializer.data
    
    @staticmethod
    def update_connection_request(request_id, request_data):
        """
        Update a connection request.
        """
        connection_request = ConnectionQuery.get_connection_request(request_id)
        connection_request = ConnectionHelpers.process_connection_request_data_update(connection_request, request_data)
        connection_request.save()
        
        serializer = ConnectionRequestSerializer(connection_request)
        
        return serializer.data
    
    @staticmethod
    def delete_connection_request(request_id):
        """
        Delete a connection request.
        """
        connection_request = ConnectionQuery.get_connection_request(request_id)
        connection_request.delete()
        
        return True
    
    @staticmethod
    def delete_all_connection_requests():
        """
        Delete all connection requests.
        """
        connection_requests = ConnectionQuery.get_connection_requests()
        connection_requests.delete()
        
        return True
    

    # user services
    @staticmethod
    def get_user_connections(user_id):
        """
        Get all connections for a specific user.
        """
        connections = ConnectionQuery.get_connections_by_user(user_id)
        return connections
    
    @staticmethod
    def get_user_connection_requests(user_id):
        """
        Get all connection requests for a specific user.
        """
        connection_requests = ConnectionQuery.get_connection_requests_by_user(user_id)
        return connection_requests
    

    @staticmethod
    def get_user_connection_requests_by_status(user_id, status):
        """
        Get all connection requests for a specific user with a specific status.
        """
        connection_requests = ConnectionQuery.get_connection_requests_by_status(user_id, status)
        return connection_requests
    

    @staticmethod
    def get_user_connection_requests_report(user_id):
        """
        Get a report for all connection requests sent to a specific user.
        """
        report = ConnectionReport.get_connection_requests_by_user_report(user_id)
        return report
    

