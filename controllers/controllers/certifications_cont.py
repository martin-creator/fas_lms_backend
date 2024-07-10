from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from activity.models import Attachment
from certifications.models import Certification, CertificationEvent



class CertificationHandlingController:
    def __init__(self):
        pass

    def issue_certification(self, user, name, issuing_organization, issue_date, expiration_date=None, description="", certificate_image=None, related_jobs=None, related_courses=None, learning_paths=None):
        certification = Certification(
            user=user,
            name=name,
            issuing_organization=issuing_organization,
            issue_date=issue_date,
            expiration_date=expiration_date,
            description=description,
            certificate_image=certificate_image,
        )

        if related_jobs:
            certification.related_jobs.set(related_jobs)
        if related_courses:
            certification.related_courses.set(related_courses)
        if learning_paths:
            certification.learning_paths.set(learning_paths)

        certification.save()
        return certification

    def verify_certification(self, certification_id):
        certification = Certification.objects.get(id=certification_id)
        verified = (certification.credential_id)
        if verified:
            certification.verify()
        return verified

    def revoke_certification(self, certification_id, reason):
        certification = Certification.objects.get(id=certification_id)
        certification.revoke(reason)

    def add_attachment_to_certification(self, certification_id, attachment_file):
        certification = Certification.objects.get(id=certification_id)
        attachment = Attachment(file=attachment_file)
        attachment.save()
        certification.add_attachment(attachment)

    def list_certification_events(self, certification_id):
        certification = Certification.objects.get(id=certification_id)
        events = CertificationEvent.objects.filter(certification=certification).order_by('-timestamp')
        return events

    def get_user_certifications(self, user):
        return Certification.objects.filter(user=user)

    def is_certification_expired(self, certification_id):
        certification = Certification.objects.get(id=certification_id)
        return certification.is_expired()

    def generate_shareable_url(self, certification_id):
        certification = Certification.objects.get(id=certification_id)
        if not certification.shareable_url:
            unique_id = get_random_string(length=32)
            certification.shareable_url = f"{settings.SITE_URL}/certifications/share/{unique_id}/"
            certification.save()
        return certification.shareable_url

    def save_certification(self, certification):
        certification.save()

    def associate_certification_with_user_profile(self, certification):
        if not certification.user.profile.certifications.filter(id=certification.id).exists():
            certification.user.profile.certifications.add(certification)
