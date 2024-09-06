# helpers/email_helpers.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_email(recipient, subject, template, context):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient], html_message=html_message)

def attach_file_to_email(email, attachment):
    # Example: Attach a file to an email
    # Implement according to your email backend or library used
    pass
