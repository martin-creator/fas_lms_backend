# helpers/data_helpers.py

import re

def validate_email(email):
    # Basic email validation
    if re.match(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$', email):
        return True
    return False

def sanitize_text(text):
    # Example: Strip HTML tags
    return re.sub(r'<[^>]*?>', '', text)

def format_date(date):
    # Example: Format date as YYYY-MM-DD
    return date.strftime('%Y-%m-%d')
