from profiles.models import User, UserProfile, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from allauth.account.views import ConfirmEmailView


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email_confirm.html'

class UserRegistrationView(APIView):
    """
    API endpoint to register a new user.

    Parameters:
    - username: string
    - email: string
    - password: string

    Returns:
    - username: string
    - email: string
    - token: string

    """

    pass



