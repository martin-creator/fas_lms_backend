# utils/formatting.py
import re
from datetime import datetime
from django.utils.dateformat import format as django_format
from django.utils.translation import gettext as _
import locale

locale.setlocale(locale.LC_ALL, '')  # Set to the user's default locale (may vary)

def format_name(first_name, last_name):
    """
    Format the first name and last name into a single string.
    """
    return f"{first_name.strip().title()} {last_name.strip().title()}"

def format_duration(minutes):
    """
    Format duration from minutes to hours and minutes.
    """
    hours = minutes // 60
    minutes %= 60
    return f"{hours}h {minutes}m"

def format_phone_number(phone_number):
    """
    Format phone number into a standard format.
    """
    # Example format: Normalize phone number to E.164 format
    phone_number = re.sub(r'\D', '', phone_number)
    if phone_number.startswith('0'):
        phone_number = phone_number[1:]
    return f"+{phone_number}"

def format_email(email):
    """
    Format email address into a standardized format.
    """
    return email.strip().lower()

def remove_special_characters(text):
    """
    Remove special characters from a given text.
    """
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length.
    """
    if len(text) > max_length:
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    return text

def format_message(message):
    """
    Format a message for display or storage.
    """
    return message.strip().capitalize()

def format_url(url):
    """
    Format a URL string.
    """
    return url.strip()

def format_course_details(course):
    """
    Format course details for display.
    """
    formatted_course = f"{course['title'].strip().title()}\n"
    formatted_course += f"Description: {truncate_text(course['description'].strip())}\n"
    formatted_course += f"Prerequisites: {course.get('prerequisites', 'None').strip()}\n"
    # Add more fields as needed
    return formatted_course

def format_user_profile(user_profile):
    """
    Format user profile details for display.
    """
    formatted_profile = "User Profile\n"
    formatted_profile += f"Name: {format_name(user_profile['first_name'], user_profile['last_name'])}\n"
    formatted_profile += f"Email: {format_email(user_profile['email'])}\n"
    formatted_profile += f"Bio: {truncate_text(user_profile.get('bio', '').strip())}\n"
    # Add more fields as needed
    return formatted_profile

def format_notification(notification):
    """
    Format notification details for display.
    """
    formatted_notification = "Notification\n"
    formatted_notification += f"Subject: {truncate_text(notification['subject'].strip())}\n"
    formatted_notification += f"Message: {truncate_text(notification['message'].strip())}\n"
    # Add more fields as needed
    return formatted_notification

def format_date(date, date_format='%Y-%m-%d'):
    """
    Format a date string into the specified format.

    Args:
    - date: Date object or string.
    - date_format: Format string (default is '%Y-%m-%d').

    Returns:
    - Formatted date string.
    """
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(date_format)

def format_datetime(datetime_obj, datetime_format='%Y-%m-%d %H:%M:%S'):
    """
    Format a datetime object into the specified format.

    Args:
    - datetime_obj: Datetime object.
    - datetime_format: Format string (default is '%Y-%m-%d %H:%M:%S').

    Returns:
    - Formatted datetime string.
    """
    return django_format(datetime_obj, datetime_format)

def format_number(number, decimal_places=2):
    """
    Format a number with commas and specified decimal places.

    Args:
    - number: Number to format.
    - decimal_places: Number of decimal places (default is 2).

    Returns:
    - Formatted number string.
    """
    return f"{number:,.{decimal_places}f}"

def format_currency(amount, currency_symbol='$'):
    """
    Format a number as currency.

    Args:
    - amount: Amount to format.
    - currency_symbol: Currency symbol (default is '$').

    Returns:
    - Formatted currency string.
    """
    return f"{currency_symbol}{amount:,.2f}"

def format_percentage(value, decimal_places=2):
    """
    Format a number as a percentage.

    Args:
    - value: Value to format as a percentage.
    - decimal_places: Number of decimal places (default is 2).

    Returns:
    - Formatted percentage string.
    """
    return f"{value:.{decimal_places}%}"

def format_address(address):
    """
    Format an address dictionary into a single string.

    Args:
    - address: Dictionary containing address components.

    Returns:
    - Formatted address string.
    """
    return f"{address.get('street', '').strip()}, {address.get('city', '').strip()}, {address.get('state', '').strip()} {address.get('zip_code', '').strip()}"

def format_json(data):
    """
    Pretty format JSON data.

    Args:
    - data: Data to format as JSON.

    Returns:
    - Formatted JSON string.
    """
    return json.dumps(data, indent=4, sort_keys=True)

def format_full_name(user):
    """
    Format a user's full name including title and suffix if available.

    Args:
    - user: User object or dictionary containing name details.

    Returns:
    - Formatted full name string.
    """
    name_parts = [user.get('title', '').strip(), user['first_name'].strip(), user['last_name'].strip(), user.get('suffix', '').strip()]
    return ' '.join(part for part in name_parts if part)

# Additional formatting functions for different use cases
def format_multiline_text(text):
    """
    Format multiline text to remove extra whitespace and clean up each line.

    Args:
    - text: Multiline text string.

    Returns:
    - Cleaned multiline text.
    """
    lines = text.strip().split('\n')
    return '\n'.join(line.strip() for line in lines)

def format_csv_row(data, delimiter=','):
    """
    Format a list or tuple into a CSV row string.

    Args:
    - data: List or tuple containing row data.
    - delimiter: Delimiter for CSV (default is ',').

    Returns:
    - Formatted CSV row string.
    """
    return delimiter.join(f'"{str(item).replace(\'"\', \'""\')}"' for item in data)

# Internationalization support functions
def format_localized_date(date, locale_code='en_US'):
    """
    Format date according to the specified locale.

    Args:
    - date: Date object or string.
    - locale_code: Locale code (default is 'en_US').

    Returns:
    - Localized formatted date string.
    """
    locale.setlocale(locale.LC_TIME, locale_code)
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%x')

def format_localized_currency(amount, locale_code='en_US'):
    """
    Format currency according to the specified locale.

    Args:
    - amount: Amount to format.
    - locale_code: Locale code (default is 'en_US').

    Returns:
    - Localized formatted currency string.
    """
    locale.setlocale(locale.LC_ALL, locale_code)
    return locale.currency(amount, grouping=True)

def format_localized_number(number, locale_code='en_US'):
    """
    Format number according to the specified locale.

    Args:
    - number: Number to format.
    - locale_code: Locale code (default is 'en_US').

    Returns:
    - Localized formatted number string.
    """
    locale.setlocale(locale.LC_ALL, locale_code)
    return locale.format_string("%d", number, grouping=True)

# Enhance docstrings for better understanding and usage
def format_product_details(product):
    """
    Format product details for display.

    Args:
    - product: Dictionary containing product details.

    Returns:
    - Formatted product details string.
    """
    formatted_product = f"Product: {product['name'].strip()}\n"
    formatted_product += f"Price: {format_currency(product['price'])}\n"
    formatted_product += f"Description: {truncate_text(product['description'].strip())}\n"
    # Add more fields as needed
    return formatted_product