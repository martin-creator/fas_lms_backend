from django.utils import timezone
from certifications.models import Certification
from utils.notifications import send_notification

def check_expiring_certifications():
    expiring_soon = Certification.objects.filter(expiration_date__lte=timezone.now().date() + timedelta(days=30))
    for cert in expiring_soon:
        send_notification(cert.user, "Your certification is expiring soon.", "Please renew your certification.")
