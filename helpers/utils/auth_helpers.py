# helpers/auth_helpers.py

import jwt
from datetime import datetime, timedelta
from django.conf import settings

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def check_user_permission(user, action):
    # Example: Check if user has permission for an action
    # Implement your permission logic here
    pass
