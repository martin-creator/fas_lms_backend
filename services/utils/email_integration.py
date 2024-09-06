from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from typing import List, Dict, Union
from services.exceptions import EmailIntegrationException

logger = logging.getLogger(__name__)

class EmailIntegration:
    @staticmethod
    def send_plain_email(subject: str, message: str, recipient_list: List[str], from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send a plain text email.
        """
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Plain email sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending plain email to {recipient_list}: {e}")
            raise EmailIntegrationException("Failed to send plain email.")
    
    @staticmethod
    def send_html_email(subject: str, html_content: str, recipient_list: List[str], from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send an HTML email.
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            logger.info(f"HTML email sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending HTML email to {recipient_list}: {e}")
            raise EmailIntegrationException("Failed to send HTML email.")
    
    @staticmethod
    def send_email_with_attachment(subject: str, message: str, recipient_list: List[str], attachment_path: str, from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send an email with an attachment.
        """
        try:
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email=from_email,
                to=recipient_list,
            )
            email.attach_file(attachment_path)
            email.send(fail_silently=False)
            logger.info(f"Email with attachment sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending email with attachment to {recipient_list}: {e}")
            raise EmailIntegrationException("Failed to send email with attachment.")
    
    @staticmethod
    def send_templated_email(subject: str, template_name: str, context: Dict[str, Union[str, int]], recipient_list: List[str], from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send an email using an HTML template.
        """
        try:
            html_content = render_to_string(template_name, context)
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=recipient_list,
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            logger.info(f"Templated email sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending templated email to {recipient_list}: {e}")
            raise EmailIntegrationException("Failed to send templated email.")
    
    @staticmethod
    def validate_email_address(email: str) -> bool:
        """
        Validate an email address.
        """
        import re
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        is_valid = re.match(email_regex, email) is not None
        if is_valid:
            logger.info(f"Valid email address: {email}")
        else:
            logger.error(f"Invalid email address: {email}")
        return is_valid
    
    @staticmethod
    def send_bulk_email(subject: str, message: str, recipient_list: List[str], from_email: str = settings.DEFAULT_FROM_EMAIL):
        """
        Send bulk plain text emails.
        """
        try:
            for recipient in recipient_list:
                EmailIntegration.send_plain_email(subject, message, [recipient], from_email)
            logger.info(f"Bulk emails sent successfully to: {recipient_list}")
        except Exception as e:
            logger.error(f"Error sending bulk emails to {recipient_list}: {e}")
            raise EmailIntegrationException("Failed to send bulk emails.")

# Example usage:
# EmailIntegration.send_plain_email("Subject", "Message", ["recipient@example.com"])
class EmailService:
    @staticmethod
    def send_email(subject, message, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=fail_silently,
        )

    @staticmethod
    def send_email_with_attachment(subject, message, recipient_list, attachment_path, from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
        email = EmailMessage(
            subject,
            message,
            from_email,
            recipient_list
        )
        email.attach_file(attachment_path)
        email.send(fail_silently=fail_silently)

    @staticmethod
    def send_templated_email(subject, template_name, context, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
        html_message = render_to_string(template_name, context)
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            html_message=html_message,
            fail_silently=fail_silently,
        )
