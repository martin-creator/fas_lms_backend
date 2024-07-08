from django.db import models
from django.conf import settings
from activity.models import Attachment
from django.contrib.contenttypes.fields import GenericRelation

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
        self.verification_status = True  # Set verification status based on check
        self.save()
            
        
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.user.profile.certifications.filter(id=self.id).exists():
            self.user.profile.certifications.add(self)
    
    def is_expired(self):
            return self.expiration_date and self.expiration_date < timezone.now().date()
    
    def add_attachment(self, attachment):
            Attachment.objects.create(content_object=self, attachment=attachment)
    