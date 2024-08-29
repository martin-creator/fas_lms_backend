from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from connections.models import ConnectionRequest, Connection
from connections.serializers import ConnectionRequestSerializer, ConnectionSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


# class ConnectionRequest(models.Model):
#     from_user = models.ForeignKey(UserProfile, related_name='connection_requests_sent', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(UserProfile, related_name='connection_requests_received', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.from_user} wants to connect with {self.to_user}"

#     def accept(self):
#         self.status = 'accepted'
#         Connection.objects.create(user=self.to_user, connection=self.from_user)
#         self.save()

#     def reject(self):
#         self.status = 'rejected'
#         self.save()

# class Connection(models.Model):
#     user = models.ForeignKey(UserProfile, related_name='connections', on_delete=models.CASCADE)
#     connection = models.ForeignKey(UserProfile, related_name='connected_users', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user} is connected with {self.connection}"


class ConnectionHelpers:
    
        @staticmethod
        def process_connection_request_data(data):
            """
            Process connection request data before saving it to the database.
            """
            from_user_id = data.get('from_user_id')
            to_user_id = data.get('to_user_id')
    
            if not from_user_id:
                raise ValidationError('From User ID is required.')
    
            if not to_user_id:
                raise ValidationError('To User ID is required.')
            
            from_user = User.objects.get(id=from_user_id)
            to_user = User.objects.get(id=to_user_id)
    
            connection_request = ConnectionRequest(
                from_user=from_user,
                to_user=to_user
            )
    
            return connection_request
        
    
        @staticmethod
        def process_connection_request_data_update(request_id, data):
            """
            Process connection request data before updating it in the database.
            """
            status = data.get('status')
    
            if not request_id:
                raise ValidationError('Request ID is required.')
            
            connection_request = ConnectionRequest.objects.get(id=request_id)
    
            if status is not None:
                connection_request.status = status
    
            return connection_request
        
        
    
    
        @staticmethod
        def process_connection_data(data):
            """
            Process connection data before saving it to the database.
            """
            user_id = data.get('user_id')
            connection_id = data.get('connection_id')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            if not connection_id:
                raise ValidationError('Connection ID is required.')
            
            user = User.objects.get(id=user_id)
            connection = User.objects.get(id=connection_id)
    
            connection = Connection(
                user=user,
                connection=connection
            )
    
            return connection
        
    
        @staticmethod
        def process_connection_data_update(connection_id, data):
            """
            Process connection data before updating it in the database.
            """
            user_id = data.get('user_id')
            connection_id = data.get('connection_id')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            if not connection_id:
                raise ValidationError('Connection ID is required.')
            
            connection = Connection.objects.get(id=connection_id)

            user = User.objects.get(id=user_id)
            connection = User.objects.get(id=connection_id)

            if user is not None:
                connection.user = user

            if connection is not None:
                connection.connection = connection

            return connection

