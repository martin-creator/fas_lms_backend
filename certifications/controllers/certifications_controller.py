from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer   
from certifications.settings.certifications_settings import CertificationsSettings
from certifications.querying.certifications_query import CertificationQuery
from certifications.helpers.certifications_helpers import CertificationHelpers
from certifications.utils import UserUtils, DateTimeUtils
from certifications.reports.certifications_report import CertificationsReport
from certifications.services.certifications_services import CertificationService


# @staticmethod
#     def linkedin_login(request):
#         """
#         Redirect users to LinkedIn for authentication.
#         """
#         linkedin_auth_url = (
#             "https://www.linkedin.com/oauth/v2/authorization"
#             f"?response_type=code"
#             f"&client_id={settings.LINKEDIN_CLIENT_ID}"
#             f"&redirect_uri={settings.LINKEDIN_REDIRECT_URI}"
#             "&scope=r_liteprofile%20r_emailaddress"  # Adjust the scope as needed
#         )
#         return redirect(linkedin_auth_url)
    

#     @staticmethod
#     def linkedin_callback(request):
#         """
#         Receive the authorization code from LinkedIn and exchange it for an access token.
#         """
#         auth_code = request.GET.get('code')
#         if not auth_code:
#             return Response({"error": "Authorization code not provided."}, status=status.HTTP_400_BAD_REQUEST)

#         access_token = LinkedInUtils.get_access_token(auth_code)
#         if access_token:
#             user_data = LinkedInUtils.fetch_user_profile(access_token)
#             # Here you can create or update the user profile in your database
#             return Response({"user_data": user_data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Failed to retrieve access token."}, status=status.HTTP_400_BAD_REQUEST)
        

#     @staticmethod
#     def create_certification(data):
#         """
#         Create a new certification.
#         """
#         certification = CertificationHelpers.process_certification_data(data)
#         certification.save()

#         serializer = CertificationSerializer(certification)

#         return serializer.data
    

#     @staticmethod
#     def update_certification(certification_id, data):
#         """
#         Update a certification.
#         """
#         certification = CertificationQuery.get_certification(certification_id)
#         certification = CertificationHelpers.process_certification_data_update(certification, data)
#         certification.save()

#         serializer = CertificationSerializer(certification)

#         return serializer.data
    

#     @staticmethod
#     def delete_certification(certification_id):
#         """
#         Delete a certification.
#         """
#         certification = CertificationQuery.get_certification(certification_id)
#         certification.delete()

#         return True
    

#     @staticmethod
#     def generate_pdf_certificate(certification_id):
#         """
#         Generate a PDF certificate for a specific certification.
#         """
#         certification = CertificationQuery.get_certification(certification_id)
#         html_content = CertificationHelpers.generate_certificate_html(certification)
#         certificate_file_path, certificate_url, certificate_id = CertificationHelpers.generate_certificate_pdf_and_path(html_content, certification)

#         #save the pdf_path and pdf_url to the certification
#         certification.credential_url = certificate_url
#         certification.credential_id = certificate_id
#         certification.certification_image = certificate_file_path

#         certification.save()


#         return certificate_url
    

#     @staticmethod
#     def verify_certificate(credential_id):
#         """
#         Verify a certificate using the credential ID.
#         """
#         certification = CertificationQuery.get_certification(credential_id)
#         if certification:
#             return True
#         else:
#             return False
        

#     @staticmethod
#     def revoke_certificate(certification_id):
#         """
#         Revoke a certification.
#         """
#         certification = CertificationQuery.get_certification(certification_id)
#         certification.revoked = True
#         certification.save()

#         return True
        

#     @staticmethod
#     def create_linkedin_badge(data):
#         """
#         Create a new LinkedIn badge.
#         """
#         linkedin_badge = CertificationHelpers.process_linkedin_badge_data(data)
#         linkedin_badge.save()

#         serializer = LinkedInBadgeSerializer(linkedin_badge)

#         return serializer.data
    

#     @staticmethod
#     def update_linkedin_badge(badge_id, data):
#         """
#         Update a LinkedIn badge.
#         """
#         linkedin_badge = CertificationQuery.get_linked_in_badge(badge_id)
#         linkedin_badge = CertificationHelpers.process_linkedin_badge_data_update(linkedin_badge, data)
#         linkedin_badge.save()

#         serializer = LinkedInBadgeSerializer(linkedin_badge)

#         return serializer.data
    

#     @staticmethod
#     def delete_linkedin_badge(badge_id):
#         """
#         Delete a LinkedIn badge.
#         """
#         linkedin_badge = CertificationQuery.get_linked_in_badge(badge_id)
#         linkedin_badge.delete()

#         return True
    

#     @staticmethod
#     def post_badge_to_linkedin(certification_id, badge_id):
#         """
#         Post a badge to LinkedIn.
#         """

#         certification = CertificationQuery.get_certification(certification_id)
#         access_token = certification.user.profile.linkedin_access_token
#         badge = CertificationQuery.get_linked_in_badge(badge_id)


#          # Update LinkedIn feed post
#         post_url = "https://api.linkedin.com/v2/ugcPosts"
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json",
#         }

#         # Construct the post data for LinkedIn feed
#         post_data = {
#             "author": f"urn:li:person:{certification.user.profile.linkedin_id}",  # Use LinkedIn user ID
#             "lifecycleState": "PUBLISHED",
#             "specificContent": {
#                 "com.linkedin.ugc.ShareContent": {
#                     "shareCommentary": {
#                         "text": f"I just earned the '{badge.name}' badge for completing the course: '{certification.name}'! 🎉"
#                     },
#                     "shareMediaCategory": "NONE",
#                 }
#             },
#             "visibility": {
#                 "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
#             }
#         }

#         try:
#             response = requests.post(post_url, headers=headers, data=json.dumps(post_data))
#             response.raise_for_status()  # Raise an error for bad responses
#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred while updating LinkedIn profile: {http_err}")
#             return False
#         except requests.exceptions.RequestException as req_err:
#             print(f"Request error occurred while updating LinkedIn profile: {req_err}")
#             return False

#         # # Update achievements section
#         # add_badge_to_achievements(certification.user, badge)

#         return True  # Successfully updated LinkedIn profile
    

#     @staticmethod
#     def add_badge_to_user_linkedin_achievements(user_id, badge_id):
    
#         """
#         Add the badge to the user's achievements section on LinkedIn.
#         """
#         user = UserUtils.get_user(user_id)
#         badge = CertificationQuery.get_linked_in_badge(badge_id)
#         access_token = user.profile.linkedin_access_token  # Get LinkedIn access token from user profile

#         achievements_url = "https://api.linkedin.com/v2/endorsements"  # Adjust the endpoint as necessary
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#             "Content-Type": "application/json",
#         }

#         # Construct the achievement data
#         achievement_data = {
#             "entityUrn": f"urn:li:badge:{badge.id}",  # Unique identifier for the badge
#             "issuer": {
#                 "name": "Your Organization Name",
#                 "url": "https://www.futureafricanscientist.org/"
#             },
#             "badges": [{
#                 "name": badge.name,
#                 "description": badge.description,
#                 "imageUrl": badge.image_url,  # URL for the badge image
#                 "date": badge.issued_date.isoformat()  # Date badge was issued
#             }]
#         }

#         # Make the POST request to update achievements
#         try:
#             response = requests.post(achievements_url, headers=headers, data=json.dumps(achievement_data))
#             response.raise_for_status()  # Raise an error for bad responses
#             print("Badge added to LinkedIn achievements successfully.")
#         except requests.exceptions.HTTPError as http_err:
#             print(f"HTTP error occurred while adding badge to achievements: {http_err}")
#         except requests.exceptions.RequestException as req_err:
#             print(f"Request error occurred while adding badge to achievements: {req_err}")

class CertificationController:
        
        def __init__(self):
            self.certification_query = CertificationQuery()
            self.certification_report = CertificationsReport()
            self.certification_settings = CertificationsSettings()
            self.user_utils = UserUtils()
            self.date_time_utils = DateTimeUtils()
            self.certification_service = CertificationService()

        
        def linkedin_login(self, request):
            """
            Redirect users to LinkedIn for authentication.
            """
            return self.certification_service.linkedin_login(request)   
        

        def linkedin_callback(self, request):
            """
            Receive the authorization code from LinkedIn and exchange it for an access token.
            """
            return self.certification_service.linkedin_callback(request)
        

        def get_all_certifications(self):
            """
            Get all certifications.
            """
            return self.certification_service.get_certifications()
        

        def get_certification_by_id(self, certification_id):
            """
            Get a specific certification.
            """
            return self.certification_service.get_certification_by_id(certification_id)
        

        def create_certification(self, data):
            """
            Create a new certification.
            """
            return self.certification_service.create_certification(data)
        

        def update_certification(self, certification_id, data):
            """
            Update a certification.
            """
            return self.certification_service.update_certification(certification_id, data)
        

        def delete_certification(self, certification_id):
            """
            Delete a certification.
            """
            return self.certification_service.delete_certification(certification_id)
        

        def generate_pdf_certificate(self, certification_id):
            """
            Generate a PDF certificate for a specific certification.
            """
            return self.certification_service.generate_pdf_certificate(certification_id)
        

        def verify_certificate(self, credential_id):
            """
            Verify a certificate using the credential ID.
            """
            return self.certification_service.verify_certificate(credential_id)
        

        def revoke_certificate(self, certification_id):
            """
            Revoke a certification.
            """
            return self.certification_service.revoke_certificate(certification_id)
        

        def get_all_linkedin_badges(self):
            """
            Get all LinkedIn badges.
            """
            return self.certification_service.get_all_linkedin_badges()
        

        def get_linkedin_badge_by_id(self, badge_id):
            """
            Get a specific LinkedIn badge.
            """
            return self.certification_service.get_linkedin_badge_by_id(badge_id)
        

        def get_linkedin_badges_by_certification(self, certification_id):
            """
            Get all LinkedIn badges for a specific certification.
            """
            return self.certification_service.get_linkedin_badges_by_certification(certification_id)
        

        def get_linkedin_badges_by_user(self, user_id):
            """
            Get all LinkedIn badges for a specific user.
            """
            return self.certification_service.get_linkedin_badges_by_user(user_id)
        

        def create_linkedin_badge(self, data):
            """
            Create a new LinkedIn badge.
            """
            return self.certification_service.create_linkedin_badge(data)
        

        def update_linkedin_badge(self, badge_id, data):
            """
            Update a LinkedIn badge.
            """
            return self.certification_service.update_linkedin_badge(badge_id, data)
        

        def delete_linkedin_badge(self, badge_id):
            """
            Delete a LinkedIn badge.
            """
            return self.certification_service.delete_linkedin_badge(badge_id)
        

        def post_badge_to_linkedin(self, certification_id, badge_id):
            """
            Post a badge to LinkedIn.
            """
            return self.certification_service.post_badge_to_linkedin(certification_id, badge_id)
        

        def add_badge_to_user_linkedin_achievements(self, user_id, badge_id):
            """
            Add the badge to the user's achievements section on LinkedIn.
            """
            return self.certification_service.add_badge_to_user_linkedin_achievements(user_id, badge_id)

    
    
       


# class CompanyController:
    
#     def __init__(self):
#         self.company_query = CompanyQuery()
#         self.company_report = CompanyReport()
#         self.company_settings = CompanySettings()
#         self.user_utils = UserUtils()
#         self.date_time_utils = DateTimeUtils()
#         self.company_service = CompanyService()


#     def get_all_companies(self):
#         """
#         Get all companies.
#         """
#         return self.company_service.get_companies()


#     def get_company_by_id(self, company_id):
#         """
#         Get a specific company.
#         """
#         return self.company_service.get_company(company_id)


#     def create_company(self, company_data):
#         """
#         Create a new company.
#         """
#         return self.company_service.create_company(company_data)
    

#     def update_company(self, company_id, company_data):
#         """
#         Update a company.
#         """
#         return self.company_service.update_company(company_id, company_data)
    

#     def delete_company(self, company_id):
#         """
#         Delete a company.
#         """
#         return self.company_service.delete_company(company_id)
    

#     def delete_all_companies(self):
#         """
#         Delete all companies.
#         """
#         return self.company_service.delete_all_companies()
    

#     def get_company_updates(self, company_id):
#         """
#         Get all updates for a company.
#         """
#         return self.company_service.get_company_updates(company_id)
    

#     def get_company_update_by_id(self, update_id):
#         """
#         Get a specific company update.
#         """
#         return self.company_service.get_company_update_by_id(update_id)
    

#     def create_company_update(self, company_id, update_data):
#         """
#         Create an update for a company.
#         """
#         return self.company_service.create_company_update(company_id, update_data)
    

#     def update_company_update(self, company_id, update_id, update_data):
#         """
#         Update an update for a company.
#         """
#         return self.company_service.update_company_update(company_id, update_id, update_data)
    

#     def delete_company_update(self, update_id):
#         """
#         Delete a company update.
#         """
#         return self.company_service.delete_company_update(update_id)



