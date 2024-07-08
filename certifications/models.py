from django.db import models
from django.conf import settings
from django.utils import timezone
from activity.models import Attachment
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.crypto import get_random_string


class Certification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_certifications', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    attachments = GenericRelation(Attachment)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiration_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=255, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField('activity.Category', related_name='certifications_categories')
    certificate_image = models.ImageField(upload_to='certificates/', blank=True)
    verification_status = models.BooleanField(default=False)
    related_jobs = models.ManyToManyField('jobs.JobListing', related_name='job_certifications', blank=True)
    related_courses = models.ManyToManyField('courses.Course', related_name='courses_certifications', blank=True)
    revoked = models.BooleanField(default=False)
    revocation_reason = models.TextField(blank=True, null=True)
    shareable_url = models.URLField(blank=True, null=True)
    learning_paths = models.ManyToManyField('courses.LearningPath', related_name='learning_path_certifications', blank=True)

    def __str__(self):
        return f"{self.name} - {self.user.user.username}"
        
        
    def verify(self):
        """
        Method to verify certification authenticity using external service.
        Example: Check credential_id against an external API for verification.
        # Replace with actual verification logic
        verified = external_verification_service.verify_certification(self.credential_id)
        if verified:
            self.verification_status = True
            self.save()
        return verified
        """
        # Logic to verify certification authenticity
        # Example: Check credential_id against an external service
        self.verification_status = True
        self.save()
        CertificationEvent.objects.create(certification=self, user=self.user, event_type='VERIFIED')

            
    def revoke(self, reason):
        self.revoked = True
        self.revocation_reason = reason
        self.save()
        CertificationEvent.objects.create(certification=self, user=self.user, event_type='REVOKED')
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.shareable_url:
            unique_id = get_random_string(length=32)
            self.shareable_url = f"{settings.SITE_URL}/certifications/share/{unique_id}/"
        super().save(*args, **kwargs)
        if is_new:
            CertificationEvent.objects.create(certification=self, user=self.user, event_type='ISSUED')
        
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user.profile.certifications.filter(id=self.id).exists():
            self.user.profile.certifications.add(self)
    
    def is_expired(self):
            return self.expiration_date and self.expiration_date < timezone.now().date()
    
    def add_attachment(self, attachment):
            Attachment.objects.create(content_object=self, attachment=attachment)
    
    
class CertificationEvent(models.Model):
    EVENT_CHOICES = [
        ('ISSUED', 'Issued'),
        ('REVOKED', 'Revoked'),
        ('VERIFIED', 'Verified'),
    ]
    certification = models.ForeignKey('Certification', related_name='events', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=10, choices=EVENT_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.certification.name} - {self.event_type} - {self.timestamp}"