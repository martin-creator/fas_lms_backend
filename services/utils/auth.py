from django.contrib.auth import authenticate
import logging
from typing import Tuple, Union
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from services.exceptions import AuthException

logger = logging.getLogger(__name__)
User = get_user_model()

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        """
        Register a new user with the given credentials.
        """
        if User.objects.filter(username=username).exists():
            raise AuthException("Username is already taken.")
        
        if User.objects.filter(email=email).exists():
            raise AuthException("Email is already registered.")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        logger.info(f"User registered successfully: {username}")
        return user

    @staticmethod
    def authenticate_user(username: str, password: str) -> Union[User, None]:
        """
        Authenticate a user with the given username and password.
        """
        user = authenticate(username=username, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid credentials.")
        
        logger.info(f"User authenticated successfully: {username}")
        return user

    @staticmethod
    def generate_token(user: User) -> str:
        """
        Generate an authentication token for the user.
        """
        token, _ = Token.objects.get_or_create(user=user)
        logger.info(f"Token generated for user: {user.username}")
        return token.key

    @staticmethod
    def send_password_reset_email(email: str):
        """
        Send a password reset email to the user.
        """
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            send_mail(
                subject="Password Reset",
                message=f"Click the link to reset your password: {reset_link}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email]
            )
            logger.info(f"Password reset email sent to: {email}")
        except User.DoesNotExist:
            logger.error(f"Password reset requested for non-existent email: {email}")
            raise AuthException("No user found with this email address.")
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")
            raise AuthException("Failed to send password reset email.")

    @staticmethod
    def reset_password(uidb64: str, token: str, new_password: str):
        """
        Reset the user's password using the uid and token from the password reset link.
        """
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                logger.info(f"Password reset successfully for user: {user.username}")
            else:
                logger.error("Invalid password reset token.")
                raise ValidationError("Invalid token.")
        except User.DoesNotExist:
            logger.error("Password reset attempted for non-existent user.")
            raise AuthException("Invalid user.")
        except Exception as e:
            logger.error(f"Error resetting password: {e}")
            raise AuthException("Failed to reset password.")

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str):
        """
        Change the user's password.
        """
        if not user.check_password(old_password):
            logger.error(f"Password change failed for user: {user.username}. Incorrect old password.")
            raise AuthException("Old password is incorrect.")
        
        user.set_password(new_password)
        user.save()
        logger.info(f"Password changed successfully for user: {user.username}")

    @staticmethod
    def revoke_token(user: User):
        """
        Revoke the user's authentication token.
        """
        try:
            token = Token.objects.get(user=user)
            token.delete()
            logger.info(f"Token revoked for user: {user.username}")
        except Token.DoesNotExist:
            logger.error(f"Token revocation failed: no token found for user {user.username}")
            raise AuthException("No token found for this user.")
        except Exception as e:
            logger.error(f"Error revoking token for user {user.username}: {e}")
            raise AuthException("Failed to revoke token.")

    @staticmethod
    def get_user_by_token(token_key: str) -> Union[User, None]:
        """
        Get the user associated with the given token.
        """
        try:
            token = Token.objects.get(key=token_key)
            logger.info(f"User retrieved by token: {token.user.username}")
            return token.user
        except Token.DoesNotExist:
            logger.error(f"User retrieval failed: no token found with key {token_key}")
            raise AuthException("Invalid token.")
        except Exception as e:
            logger.error(f"Error retrieving user by token: {e}")
            raise AuthException("Failed to retrieve user by token."))

    @staticmethod
    def get_user_profile(user):
        return user.profile
