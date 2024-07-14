# activity/utils/validators.py

import re

class ActivityValidators:
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format.
        """
        email_regex = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        else:
            return False

    @staticmethod
    def validate_username(username):
        """
        Validate username format.
        """
        username_regex = r'^[a-zA-Z0-9_]+$'
        if re.match(username_regex, username):
            return True
        else:
            return False
