import os
import requests
import json
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from weasyprint import HTML  # Import WeasyPrint for generating certificates
from .models import Certification, Badge  # Import your Certification and Badge models

# class LinkedInLoginView(View):
#     def get(self, request):
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

# class LinkedInCallbackView(View):
#     def get(self, request):
#         """
#         Receive the authorization code from LinkedIn and exchange it for an access token.
#         """
#         auth_code = request.GET.get('code')
#         if not auth_code:
#             return Response({"error": "Authorization code not provided."}, status=status.HTTP_400_BAD_REQUEST)

#         access_token = get_access_token(auth_code)
#         if access_token:
#             user_data = fetch_user_profile(access_token)
#             # Here you can create or update the user profile in your database
#             return Response({"user_data": user_data}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Failed to retrieve access token."}, status=status.HTTP_400_BAD_REQUEST)


class LinkedInUtils:
    
    @staticmethod
    def get_access_token(auth_code):
        """
        Exchange the authorization code for an access token.
        """
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': settings.LINKEDIN_REDIRECT_URI,
            'client_id': settings.LINKEDIN_CLIENT_ID,
            'client_secret': settings.LINKEDIN_CLIENT_SECRET
        }

        try:
            response = requests.post(token_url, data=payload)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        
        return None
    

    @staticmethod
    def fetch_user_profile(access_token):
        """
        Fetch the user's profile data from LinkedIn using the access token.
        """
        user_profile_url = "https://api.linkedin.com/v2/me"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            response = requests.get(user_profile_url, headers=headers)
            response.raise_for_status()
            return response.json()  # Return the user profile data
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while fetching user profile: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred while fetching user profile: {req_err}")
        
        return None
    

    @staticmethod
    def update_linkedin_with_badge(certification, badge):
        """
        Update the user's LinkedIn profile with badge information.
        This function will create a post on the user's LinkedIn feed announcing the earned badge.
        """
        access_token = certification.user.profile.linkedin_access_token  # Adjust according to your user profile model

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
    def add_badge_to_achievements(user_id, badge_id):
        """
        Add the badge to the user's achievements section on LinkedIn.
        """
        user = Use
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
                "url": "https://www.yourorganization.com"
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

# class GenerateCertificateView(View):
#     def post(self, request):
#         """
#         Generate a certificate and return the certificate ID and URL.
#         """
#         user = request.user  # Assuming user is authenticated
#         data = request.data
#         certificate_id = f"cert-{user.id}-{data.get('course_name')}"  # Example credential ID

#         # Generate certificate content
#         certificate_html = f"""
#         <h1>Certificate of Completion</h1>
#         <p>This certifies that <strong>{user.username}</strong> has completed the course: <strong>{data.get('course_name')}</strong></p>
#         """

#         # Generate the PDF using WeasyPrint
#         certificate_file_path = os.path.join(settings.CERTIFICATE_IMAGE_PATH, f"{certificate_id}.pdf")
#         HTML(string=certificate_html).write_pdf(certificate_file_path)

#         # Save certificate details to the database
#         Certification.objects.create(
#             user=user,
#             name=data.get('course_name'),
#             credential_id=certificate_id,
#             credential_url=certificate_file_path,
#             issue_date=data.get('issue_date'),
#             expiration_date=data.get('expiration_date')
#         )

#         return Response({"credential_id": certificate_id, "credential_url": certificate_file_path}, status=status.HTTP_201_CREATED)

# class VerifyCertificateView(View):
#     def get(self, request, credential_id):
#         """
#         Verify a certificate by its credential ID.
#         """
#         try:
#             certification = Certification.objects.get(credential_id=credential_id)
#             return Response({"status": "valid", "certification": certification}, status=status.HTTP_200_OK)
#         except Certification.DoesNotExist:
#             return Response({"status": "invalid"}, status=status.HTTP_404_NOT_FOUND)

# class AssignBadgeView(View):
#     def post(self, request, credential_id):
#         """
#         Assign a badge to a certification based on its credential ID.
#         """
#         try:
#             certification = Certification.objects.get(credential_id=credential_id)
#             badge_id = request.data.get('badge_id')
#             badge = Badge.objects.get(id=badge_id)

#             # Assign the badge to the certification
#             certification.badge = badge
#             certification.save()

#             # Update LinkedIn profile with the badge information
#             if update_linkedin_with_badge(certification, badge):
#                 return Response({"message": "Badge assigned and LinkedIn updated successfully."}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message": "Badge assigned, but failed to update LinkedIn."}, status=status.HTTP_200_OK)
#         except Certification.DoesNotExist:
#             return Response({"error": "Certification not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Badge.DoesNotExist:
#             return Response({"error": "Badge not found."}, status=status.HTTP_404_NOT_FOUND)


