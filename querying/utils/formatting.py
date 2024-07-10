# utils/formatting.py
import re

def format_name(first_name, last_name):
    """
    Format the first name and last name into a single string.

    Args:
    - first_name: First name of the user.
    - last_name: Last name of the user.

    Returns:
    - Formatted full name string.
    """
    return f"{first_name} {last_name}"

def format_duration(minutes):
    """
    Format duration from minutes to hours and minutes.

    Args:
    - minutes: Duration in minutes.

    Returns:
    - Formatted duration string in hours and minutes (e.g., '2h 30m').
    """
    hours = minutes // 60
    minutes %= 60
    return f"{hours}h {minutes}m"

def format_phone_number(phone_number):
    """
    Format phone number into a standard format.

    Args:
    - phone_number: Phone number string.

    Returns:
    - Formatted phone number string (e.g., '+1234567890').
    """
    # Example format: Assume phone_number is already normalized or formatted
    return phone_number

def format_email(email):
    """
    Format email address into a standardized format.

    Args:
    - email: Email address string.

    Returns:
    - Formatted email address string.
    """
    # Example format: Validate and format email address
    return email.strip().lower()

def remove_special_characters(text):
    """
    Remove special characters from a given text.

    Args:
    - text: Input text containing special characters.

    Returns:
    - Text with special characters removed.
    """
    # Example: Remove non-alphanumeric characters
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length.

    Args:
    - text: Input text to truncate.
    - max_length: Maximum length of the truncated text (default is 100).

    Returns:
    - Truncated text.
    """
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def format_message(message):
    """
    Format a message for display or storage.

    Args:
    - message: Input message to format.

    Returns:
    - Formatted message string.
    """
    # Example: Apply specific formatting rules to the message
    return message.capitalize()

def format_url(url):
    """
    Format a URL string.

    Args:
    - url: URL string to format.

    Returns:
    - Formatted URL string.
    """
    # Example: Validate and format URL
    return url.strip()

def format_course_details(course):
    """
    Format course details for display.

    Args:
    - course: Dictionary containing course details.

    Returns:
    - Formatted course details string.
    """
    formatted_course = f"{course['title']}\n"
    formatted_course += f"Description: {truncate_text(course['description'])}\n"
    formatted_course += f"Prerequisites: {course.get('prerequisites', 'None')}\n"
    # Add more fields as needed
    return formatted_course

def format_user_profile(user_profile):
    """
    Format user profile details for display.

    Args:
    - user_profile: Dictionary containing user profile details.

    Returns:
    - Formatted user profile string.
    """
    formatted_profile = f"User Profile\n"
    formatted_profile += f"Name: {format_name(user_profile['first_name'], user_profile['last_name'])}\n"
    formatted_profile += f"Email: {format_email(user_profile['email'])}\n"
    formatted_profile += f"Bio: {truncate_text(user_profile['bio'])}\n"
    # Add more fields as needed
    return formatted_profile

def format_notification(notification):
    """
    Format notification details for display.

    Args:
    - notification: Dictionary containing notification details.

    Returns:
    - Formatted notification string.
    """
    formatted_notification = f"Notification\n"
    formatted_notification += f"Subject: {truncate_text(notification['subject'])}\n"
    formatted_notification += f"Message: {truncate_text(notification['message'])}\n"
    # Add more fields as needed
    return formatted_notification

# Additional Formatting Functions can be added as needed for specific LMS functionalities