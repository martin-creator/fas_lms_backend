# utils/security.py

import re
import html
from typing import Any

def sanitize_input(data: Any) -> Any:
    """
    Sanitize input data to prevent SQL injection and XSS attacks.

    Args:
    - data: Input data which can be a string, list, or dict.

    Returns:
    - Sanitized data.
    """
    
    if isinstance(data, str):
        return sanitize_string(data)
    elif isinstance(data, list):
        return [sanitize_input(item) for item in data]
    elif isinstance(data, dict):
        return {key: sanitize_input(value) for key, value in data.items()}
    else:
        return data

def sanitize_string(value: str) -> str:
    """
    Sanitize a string input to prevent SQL injection and XSS attacks.

    Args:
    - value: The string to sanitize.

    Returns:
    - Sanitized string.
    """
    # Escape HTML characters
    sanitized_value = html.escape(value)
    
    # Remove potential SQL injection patterns (simple example)
    sanitized_value = re.sub(r'(union\s+select|select\s+from|drop\s+table|--|#|;)', '', sanitized_value, flags=re.IGNORECASE)

    # Remove potential XSS patterns
    sanitized_value = re.sub(r'(<script.*?>.*?</script>|<.*?javascript:.*?>)', '', sanitized_value, flags=re.IGNORECASE)

    return sanitized_value
