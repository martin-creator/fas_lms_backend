from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from connections.models import ConnectionRequest, Connection
from connections.serializers import ConnectionRequestSerializer, ConnectionSerializer
from connections.querying.connections_query import ConnectionQuery
from connections.services.connections_services import ConnectionService
from connections.helpers.connections_helpers import ConnectionHelpers
from connections.utils import UserUtils, DateTimeUtils
from connections.reports.connections_report import ConnectionReport
from connections.settings.connections_settings import ConnectionsSettings

class ConnectionController:

    def __init__(self):
        self.connection_query = ConnectionQuery()
        self.connection_report = ConnectionReport()
        self.connection_settings = ConnectionsSettings()
        self.user_utils = UserUtils()
        self.date_time_utils = DateTimeUtils()
        self.connection_service = ConnectionService()


    def get_all_connections(self):
        """
        Get all connections.
        """
        return self.connection_service.get_connections
    

    def get_connection(self, connection_id):
        """
        Get a specific connection.
        """
        return self.connection_service.get_connection(connection_id)
    

    def create_connection(self, connection_data):
        """
        Create a new connection.
        """
        return self.connection_service.create_connection(connection_data)
    

    def update_connection(self, connection_id, connection_data):
        """
        Update a connection.
        """
        return self.connection_service.update_connection(connection_id, connection_data)
    

    def delete_connection(self, connection_id):
        """
        Delete a connection.
        """
        return self.connection_service.delete_connection(connection_id)
    

    def delete_all_connections(self):
        """
        Delete all connections.
        """
        return self.connection_service.delete_all_connections()
    

    def get_all_connection_requests(self):
        """
        Get all connection requests.
        """
        return self.connection_service.get_connection_requests
    

    def get_connection_request(self, request_id):
        """
        Get a specific connection request.
        """
        return self.connection_service.get_connection_request(request_id)
    

    def create_connection_request(self, request_data):
        """
        Create a new connection request.
        """
        return self.connection_service.create_connection_request(request_data)
    

    def update_connection_request(self, request_id, request_data):
        """
        Update a connection request.
        """
        return self.connection_service.update_connection_request(request_id, request_data)
    

    def delete_connection_request(self, request_id):
        """
        Delete a connection request.
        """
        return self.connection_service.delete_connection_request(request_id)
    

    def delete_all_connection_requests(self):
        """
        Delete all connection requests.
        """
        return self.connection_service.delete_all_connection_requests()
    

    def get_user_connections(self, user_id):
        """
        Get all connections for a specific user.
        """
        return self.connection_service.get_user_connections(user_id)
    

    def get_user_connection_requests(self, user_id):
        """
        Get all connection requests for a specific user.
        """
        return self.connection_service.get_user_connection_requests(user_id)
    

    def get_user_connection_requests_by_status(self, user_id, status):
        """
        Get all connection requests for a specific user with a specific status.
        """
        return self.connection_service.get_user_connection_requests_by_status(user_id, status)
    

    def get_user_connection_requests_report(self, user_id):
        """
        Get a report for all connection requests sent to a specific user.
        """
        return self.connection_service.get_user_connection_requests_report(user_id)
    

    
