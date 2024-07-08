from django.contrib.auth import authenticate

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        return authenticate(username=username, password=password)

    @staticmethod
    def get_user_profile(user):
        return user.profile
