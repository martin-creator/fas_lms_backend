from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

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
