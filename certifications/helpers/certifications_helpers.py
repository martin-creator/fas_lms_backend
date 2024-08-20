from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from certifications.models import Certification, LinkedInBadge
# from profiles.models import UserProfile
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


# class Certification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_certifications', on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     attachments = GenericRelation(Attachment)
#     issuing_organization = models.CharField(max_length=255)
#     issue_date = models.DateField()
#     expiration_date = models.DateField(null=True, blank=True)
#     credential_id = models.CharField(max_length=255, blank=True)
#     credential_url = models.URLField(blank=True)
#     description = models.TextField(blank=True)
#     categories = models.ManyToManyField('activity.Category', related_name='certifications_categories')
#     certificate_image = models.ImageField(upload_to='certificates/', blank=True)
#     verification_status = models.BooleanField(default=False)
#     related_jobs = models.ManyToManyField('jobs.JobListing', related_name='job_certifications', blank=True)
#     related_courses = models.ManyToManyField('courses.Course', related_name='courses_certifications', blank=True)
#     related_events = models.ManyToManyField('events.Event', related_name='event_certifications', blank=True)
#     revoked = models.BooleanField(default=False, blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - {self.user.user.username}"
    
# class LinkedInBadge(models.Model):
#     certification = models.OneToOneField(Certification, related_name='linkedin_badge', on_delete=models.CASCADE)
#     badge_image = models.ImageField(upload_to='linkedin_badges/', blank=True)
#     badge_url = models.URLField(blank=True)
#     share_on_linkedin = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"LinkedIn Badge for {self.certification.name}"


class CertificationHelpers:
    
        @staticmethod
        def process_certification_data(data):
            """
            Process certification data before saving it to the database.
            """
            user_id = data.get('user_id')
            name = data.get('name')
            issuing_organization = data.get('issuing_organization')
            issue_date = data.get('issue_date')
            expiration_date = data.get('expiration_date')
            credential_id = data.get('credential_id')
            credential_url = data.get('credential_url')
            description = data.get('description')
            categories = data.get('categories')
            certificate_image = data.get('certificate_image')
            related_jobs = data.get('related_jobs')
            related_courses = data.get('related_courses')
            related_events = data.get('related_events')
            revoked = data.get('revoked')
    
            user = User.objects.get(id=user_id)
    
            certification = Certification(
                user=user,
                name=name,
                issuing_organization=issuing_organization,
                issue_date=issue_date,
                expiration_date=expiration_date,
                credential_id=credential_id,
                credential_url=credential_url,
                description=description,
                certificate_image=certificate_image,
                revoked=revoked
            )
    
            return certification, categories, related_jobs, related_courses, related_events
        
    
        @staticmethod
        def process_certification_data_update(certification_id, data):
            """
            Process certification data before updating it in the database.
            """
            certification = Certification.objects.get(id=certification_id)
            
            name = data.get('name')
            issuing_organization = data.get('issuing_organization')
            issue_date = data.get('issue_date')
            expiration_date = data.get('expiration_date')
            credential_id = data.get('credential_id')
            credential_url = data.get('credential_url')
            description = data.get('description')
            categories = data.get('categories')
            certificate_image = data.get('certificate_image')
            related_jobs = data.get('related_jobs')
            related_courses = data.get('related_courses')
            related_events = data.get('related_events')
            revoked = data.get('revoked')
    
            if name is not None:
                certification.name = name
    
            if issuing_organization is not None:
                certification.issuing_organization = issuing_organization
    
            if issue_date is not None:
                certification.issue_date = issue_date
    
            if expiration_date is not None:
                certification.expiration_date = expiration_date
    
            if credential_id is not None:
                certification.credential_id = credential_id

            if credential_url is not None:
                certification.credential_url = credential_url
            
            if description is not None:
                certification.description = description

            if certificate_image is not None:
                certification.certificate_image = certificate_image

            if revoked is not None:
                certification.revoked = revoked

            

            return certification, categories, related_jobs, related_courses, related_events
        

        @staticmethod
        def process_linkedin_badge_data(data):
            """
            Process LinkedIn badge data before saving it to the database.
            """
            certification_id = data.get('certification_id')
            badge_image = data.get('badge_image')
            badge_url = data.get('badge_url')
            share_on_linkedin = data.get('share_on_linkedin')
    
            certification = Certification.objects.get(id=certification_id)
    
            linkedin_badge = LinkedInBadge(
                certification=certification,
                badge_image=badge_image,
                badge_url=badge_url,
                share_on_linkedin=share_on_linkedin
            )
    
            return linkedin_badge
        

        @staticmethod
        def process_linkedin_badge_data_update(badge_id, data):
            """
            Process LinkedIn badge data before updating it in the database.
            """
            linkedin_badge = LinkedInBadge.objects.get(id=badge_id)
            
            badge_image = data.get('badge_image')
            badge_url = data.get('badge_url')
            share_on_linkedin = data.get('share_on_linkedin')
    
            if badge_image is not None:
                linkedin_badge.badge_image = badge_image
    
            if badge_url is not None:
                linkedin_badge.badge_url = badge_url
    
            if share_on_linkedin is not None:
                linkedin_badge.share_on_linkedin = share_on_linkedin
    
            return linkedin_badge