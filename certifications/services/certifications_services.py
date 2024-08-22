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
            "&scope=r_liteprofile%20r_emailaddress"  # Adjust the scope as needed
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
            user_data = LinkedInUtils.fetch_user_profile(access_token)
            # Here you can create or update the user profile in your database
            return Response({"user_data": user_data}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to retrieve access token."}, status=status.HTTP_400_BAD_REQUEST)
        

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


         # Update LinkedIn feed post
        post_url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Construct the post data for LinkedIn feed
        post_data = {
            "author": f"urn:li:person:{certification.user.profile.linkedin_id}",  # Use LinkedIn user ID
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f"I just earned the '{badge.name}' badge for completing the course: '{certification.name}'! 🎉"
                    },
                    "shareMediaCategory": "NONE",
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }

        try:
            response = requests.post(post_url, headers=headers, data=json.dumps(post_data))
            response.raise_for_status()  # Raise an error for bad responses
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while updating LinkedIn profile: {http_err}")
            return False
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred while updating LinkedIn profile: {req_err}")
            return False

        # # Update achievements section
        # add_badge_to_achievements(certification.user, badge)

        return True  # Successfully updated LinkedIn profile
    

    @staticmethod
    def add_badge_to_user_linkedin_achievements(user_id, badge_id):
    
        """
        Add the badge to the user's achievements section on LinkedIn.
        """
        user = UserUtils.get_user(user_id)
        badge = CertificationQuery.get_linked_in_badge(badge_id)
        access_token = user.profile.linkedin_access_token  # Get LinkedIn access token from user profile

        achievements_url = "https://api.linkedin.com/v2/endorsements"  # Adjust the endpoint as necessary
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Construct the achievement data
        achievement_data = {
            "entityUrn": f"urn:li:badge:{badge.id}",  # Unique identifier for the badge
            "issuer": {
                "name": "Your Organization Name",
                "url": "https://www.futureafricanscientist.org/"
            },
            "badges": [{
                "name": badge.name,
                "description": badge.description,
                "imageUrl": badge.image_url,  # URL for the badge image
                "date": badge.issued_date.isoformat()  # Date badge was issued
            }]
        }

        # Make the POST request to update achievements
        try:
            response = requests.post(achievements_url, headers=headers, data=json.dumps(achievement_data))
            response.raise_for_status()  # Raise an error for bad responses
            print("Badge added to LinkedIn achievements successfully.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while adding badge to achievements: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred while adding badge to achievements: {req_err}")
        

        







        

    



# class CompanyService:

#     @staticmethod
#     def get_companies():
#         """
#         Get all companies.
#         """
#         companies = CompanyQuery.get_companies()
#         return companies
    

#     @staticmethod
#     def get_company(company_id):
#         """
#         Get a specific company.
#         """
#         company = CompanyQuery.get_company(company_id)
#         return company
    
#     @staticmethod
#     def create_company(company_data):
#         """
#         Create a new company.
#         """
#         company, categories, members, followers = CompanyHelpers.process_company_data(company_data)
#         company.save()

#         if categories:
#             company.categories.set(categories)
        
#         if members:
#             company.members.set(members)

#         if followers:
#             company.followers.set(followers)

#         serializer = CompanySerializer(company)

#         return serializer.data
    

#     @staticmethod
#     def update_company(company_id, company_data):
#         """
#         Update a company.
#         """
#         company, categories, members, followers =  CompanyHelpers.process_company_data_update(company_id, company_data)
#         company.save()

#         if categories:
#             company.categories.set(categories)
        
#         if members:
#             company.members.set(members)

#         if followers:
#             company.followers.set(followers)

#         serializer = CompanySerializer(company)

#         return serializer.data
    

#     @staticmethod
#     def delete_company(company_id):
#         """
#         Delete a company.
#         """
#         company = CompanyQuery.get_company(company_id)
#         company.delete()

#         return True
    

#     @staticmethod
#     def delete_all_companies():
#         """
#         Delete all companies.
#         """
#         companies = CompanyQuery.get_companies()
#         companies.delete()

#         return True
    

#     @staticmethod
#     def get_company_updates(company_id):
#         """
#         Get all updates for a specific company.
#         """
#         updates = CompanyQuery.get_company_updates(company_id)
        
#         return updates
    

#     @staticmethod
#     def get_company_update_by_id(update_id):
#         """
#         Get a specific update for a company.
#         """
#         update = CompanyQuery.get_company_update(update_id)
#         return update
    


#     @staticmethod
#     def create_company_update(company_id, update_data):
#         """
#         Create a new update for a company.
#         """
#         company_update = CompanyHelpers.process_company_update_data(company_id, update_data)
#         company_update.save()

#         serializer = CompanyUpdateSerializer(company_update)

#         return serializer.data
    

#     @staticmethod
#     def update_company_update(company_id, update_id, update_data):
#         """
#         Update an update for a company.
#         """
#         company_update = CompanyHelpers.process_company_update_data_update(update_id, update_data)
#         company_update.save()

#         serializer = CompanyUpdateSerializer(company_update)

#         return serializer.data
    

#     @staticmethod
#     def delete_company_update(update_id):
#         """
#         Delete an update for a company.
#         """
#         company_update = CompanyQuery.get_company_update(update_id)
#         company_update.delete()

#         return True
    



