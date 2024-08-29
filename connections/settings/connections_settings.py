from django.conf import settings


class ConnectionsSettings:
    """
    ConnectionsSettings: Manages app-specific settings for connections.
    """

    @staticmethod
    def get_connections_settings():
        """
        Get all connections settings.
        """
        return settings.CONNECTIONS_SETTINGS

    @staticmethod
    def update_connections_settings(connections_settings):
        """
        Update connections settings.
        """
        settings.CONNECTIONS_SETTINGS = connections_settings
