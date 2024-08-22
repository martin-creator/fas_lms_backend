from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from followers.models import Follower, FollowRequest, FollowNotification
# from profiles.models import UserProfile
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()

# class Follower(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_followers', on_delete=models.CASCADE)
#     follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_following', on_delete=models.CASCADE)
#     followed_at = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.follower.user.username} follows {self.user.user.username}"
    
#     @staticmethod
#     def is_follower(user, follower):
#         return Follower.objects.filter(user=user, follower=follower).exists()

#     @staticmethod
#     def get_followers(user):
#         return Follower.objects.filter(user=user)

# class FollowRequest(models.Model):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_requests_sent', on_delete=models.CASCADE)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_requests_received', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     message = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.from_user.user.username} wants to follow {self.to_user.user.username}"

#     def accept(self):
#         self.status = 'accepted'
#         Follower.objects.create(user=self.to_user, follower=self.from_user)
#         self.save()

#     def reject(self):
#         self.status = 'rejected'
#         self.save()

# class FollowNotification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='follow_notifications', on_delete=models.CASCADE)
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.user.username}: {self.message}"



class FollowerHelpers:
    
        @staticmethod
        def process_follower_data(data):
            """
            Process follower data before saving it to the database.
            """
            user_id = data.get('user_id')
            follower_id = data.get('follower_id')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            if not follower_id:
                raise ValidationError('Follower ID is required.')
    
            user = User.objects.get(id=user_id)
            follower = User.objects.get(id=follower_id)
    
            follower = Follower(
                user=user,
                follower=follower
            )
    
            return follower
        
    
        @staticmethod
        def process_follower_data_update(follower_id, data):
            """
            Process follower data before updating it in the database.
            """
            user_id = data.get('user_id')
            follower_id = data.get('follower_id')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            if not follower_id:
                raise ValidationError('Follower ID is required.')
    
            user = User.objects.get(id=user_id)
            follower = User.objects.get(id=follower_id)
    
            follower = Follower.objects.get(id=follower_id)
            follower.user = user
            follower.follower = follower
    
            return follower
        
        
    
    
        @staticmethod
        def process_follow_request_data(data):
            """
            Process follow request data before saving it to the database.
            """
            from_user_id = data.get('from_user_id')
            to_user_id = data.get('to_user_id')
            message = data.get('message')
    
            if not from_user_id:
                raise ValidationError('From User ID is required.')
    
            if not to_user_id:
                raise ValidationError('To User ID is required.')
    
            from_user = User.objects.get(id=from_user_id)
            to_user = User.objects.get(id=to_user_id)
    
            follow_request = FollowRequest(
                from_user=from_user,
                to_user=to_user,
                message=message
            )
    
            return follow_request
        
    
        @staticmethod
        def process_follow_request_data_update(request_id, data):
            """
            Process follow request data before updating it in the database.
            """
            from_user_id = data.get('from_user_id')
            to_user_id = data.get('to_user_id')
            message = data.get('message')
    
            if not from_user_id:
                raise ValidationError('From User ID is required.')
    
            if not to_user_id:
                raise ValidationError('To User ID is required.')
            
            from_user = User.objects.get(id=from_user_id)

            to_user = User.objects.get(id=to_user_id)

            follow_request = FollowRequest.objects.get(id=request_id)
            follow_request.from_user = from_user
            follow_request.to_user = to_user
            follow_request.message = message

            return follow_request
        

        @staticmethod
        def process_follow_notification_data(data):
            """
            Process follow notification data before saving it to the database.
            """
            user_id = data.get('user_id')
            message = data.get('message')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            user = User.objects.get(id=user_id)
    
            follow_notification = FollowNotification(
                user=user,
                message=message
            )
    
            return follow_notification
        

        @staticmethod
        def process_follow_notification_data_update(notification_id, data):
            """
            Process follow notification data before updating it in the database.
            """
            user_id = data.get('user_id')
            message = data.get('message')
    
            if not user_id:
                raise ValidationError('User ID is required.')
    
            user = User.objects.get(id=user_id)
    
            follow_notification = FollowNotification.objects.get(id=notification_id)
            follow_notification.user = user
            follow_notification.message = message
    
            return follow_notification
        

    








