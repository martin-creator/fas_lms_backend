from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from certifications.settings.certifications_settings import CertificationsSettings
from certifications.querying.certifications_query import CertificationQuery
from certifications.helpers.certifications_helpers import CertificationHelpers
from certifications.utils import UserUtils, DateTimeUtils, LinkedInUtils
from certifications.reports.certifications_report import CertificationsReport
from django.conf import settings
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
import requests, json



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



class CertificationService:

    @staticmethod
    def linkedin_login(request):
        """
        Redirect users to LinkedIn for authentication.
        """
        linkedin_auth_url = (
            "https://www.linkedin.com/oauth/v2/authorization"
            f"?response_type=code"
            f"&client_id={settings.LINKEDIN_CLIENT_ID}"
            f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
            "&scope=openid%20profile%20email"  # Adjust the scope as needed
        )
        
        return redirect(linkedin_auth_url)
    

    @staticmethod
    def linkedin_callback(request):
        """
        Receive the authorization code from LinkedIn and exchange it for an access token.
        """
        auth_code = request.GET.get('code')
        if not auth_code:
            return Response({"error": "Authorization code not provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = LinkedInUtils.get_access_token(auth_code)
        if access_token:
            print("auth_code", auth_code, "\n")
            print("access_token", access_token ,"\n")
            
            user_data = LinkedInUtils.fetch_user_profile(access_token)
            # Here you can create or update the user profile in your database
            return Response({"user_data": user_data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to retrieve access token."}, status=status.HTTP_400_BAD_REQUEST)
        

    @staticmethod
    def get_certifications():
        """
        Get all certifications.
        """
        certifications = CertificationQuery.get_certifications()
        return certifications
    


    @staticmethod
    def create_certification(data):
        """
        Create a new certification.
        """
        certification = CertificationHelpers.process_certification_data(data)
        certification.save()

        serializer = CertificationSerializer(certification)

        return serializer.data
    

    @staticmethod
    def get_certification_by_id(certification_id):
        """
        Get a specific certification.
        """
        certification = CertificationQuery.get_certification(certification_id)
        serializer = CertificationSerializer(certification)

        return serializer.data
    

    @staticmethod
    def update_certification(certification_id, data):
        """
        Update a certification.
        """
        certification = CertificationQuery.get_certification(certification_id)
        certification = CertificationHelpers.process_certification_data_update(certification, data)
        certification.save()

        serializer = CertificationSerializer(certification)

        return serializer.data
    

    @staticmethod
    def delete_certification(certification_id):
        """
        Delete a certification.
        """
        certification = CertificationQuery.get_certification(certification_id)
        certification.delete()

        return True
    

    @staticmethod
    def generate_pdf_certificate(certification_id):
        """
        Generate a PDF certificate for a specific certification.
        """
        certification = CertificationQuery.get_certification(certification_id)
        html_content = CertificationHelpers.generate_certificate_html(certification)
        certificate_file_path, certificate_url, certificate_id = CertificationHelpers.generate_certificate_pdf_and_path(html_content, certification)

        #save the pdf_path and pdf_url to the certification
        certification.credential_url = certificate_url
        certification.credential_id = certificate_id
        certification.certification_image = certificate_file_path

        certification.save()


        return certificate_url
    

    @staticmethod
    def verify_certificate(credential_id):
        """
        Verify a certificate using the credential ID.
        """
        certification = CertificationQuery.get_certification(credential_id)
        if certification:
            return True
        else:
            return False
        

    @staticmethod
    def revoke_certificate(certification_id):
        """
        Revoke a certification.
        """
        certification = CertificationQuery.get_certification(certification_id)
        certification.revoked = True
        certification.save()

        return True
        

    @staticmethod
    def create_linkedin_badge(data):
        """
        Create a new LinkedIn badge.
        """
        linkedin_badge = CertificationHelpers.process_linkedin_badge_data(data)
        linkedin_badge.save()

        serializer = LinkedInBadgeSerializer(linkedin_badge)

        return serializer.data
    

    @staticmethod
    def get_all_linkedin_badges():
        """
        Get all LinkedIn badges.
        """
        linkedin_badges = CertificationQuery.get_linked_in_badges()
        return linkedin_badges
    

    
    @staticmethod
    def get_linkedin_badge_by_id(badge_id):
        """
        Get a specific LinkedIn badge.
        """
        linkedin_badge = CertificationQuery.get_linked_in_badge(badge_id)
        serializer = LinkedInBadgeSerializer(linkedin_badge)

        return serializer.data
    

    
    @staticmethod
    def get_linkedin_badges_by_certification(certification_id):
        """
        Get all LinkedIn badges for a specific certification.
        """
        linkedin_badges = CertificationQuery.get_linked_in_badges_by_certification(certification_id)
        return linkedin_badges
    

    @staticmethod
    def get_linkedin_badges_by_user(user_id):
        """
        Get all LinkedIn badges for a specific user.
        """
        linkedin_badges = CertificationQuery.get_linked_in_badges_by_user(user_id)
        return linkedin_badges

    @staticmethod
    def update_linkedin_badge(badge_id, data):
        """
        Update a LinkedIn badge.
        """
        linkedin_badge = CertificationQuery.get_linked_in_badge(badge_id)
        linkedin_badge = CertificationHelpers.process_linkedin_badge_data_update(linkedin_badge, data)
        linkedin_badge.save()

        serializer = LinkedInBadgeSerializer(linkedin_badge)

        return serializer.data
    
    

    @staticmethod
    def delete_linkedin_badge(badge_id):
        """
        Delete a LinkedIn badge.
        """
        linkedin_badge = CertificationQuery.get_linked_in_badge(badge_id)
        linkedin_badge.delete()

        return True
    

    @staticmethod
    def post_badge_to_linkedin(certification_id, badge_id):
        """
        Post a badge to LinkedIn.
        """

        certification = CertificationQuery.get_certification(certification_id)
        access_token = certification.user.profile.linkedin_access_token
        badge = CertificationQuery.get_linked_in_badge(badge_id)

        # use linkedin Utils
        linkedin_post_response = LinkedInUtils.update_linkedin_with_badge( access_token, certification, badge)

        return linkedin_post_response

    

    @staticmethod
    def add_badge_to_user_linkedin_achievements(user_id, badge_id):
    
        """
        Add the badge to the user's achievements section on LinkedIn.
        """
        user = UserUtils.get_user(user_id)
        badge = CertificationQuery.get_linked_in_badge(badge_id)
        access_token = user.profile.linkedin_access_token  # Get LinkedIn access token from user profile

        linkedin_achievements_response = LinkedInUtils.add_badge_to_achievements(user, badge, access_token)

        return linkedin_achievements_response