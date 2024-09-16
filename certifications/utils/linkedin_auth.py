import os
import requests
import json
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from rest_framework.response import Response
from rest_framework import status
from weasyprint import HTML  # Import WeasyPrint for generating certificates
from certifications.models import Certification, LinkedInBadge
from certifications.utils import UserUtils, DateTimeUtils


class LinkedInUtils:

    @staticmethod
    def get_access_token(auth_code):
        """
        Exchange the authorization code for an access token.
        """
        token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": settings.LINKEDIN_REDIRECT_URI,
            "client_id": settings.LINKEDIN_CLIENT_ID,
            "client_secret": settings.LINKEDIN_CLIENT_SECRET,
            "scope": settings.LINKEDIN_SCOPE,
        }

        try:
            response = requests.post(token_url, data=payload)
            print(response)
            response.raise_for_status()
            return response.json().get("access_token")
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
        headers = {"Authorization": f"Bearer {access_token}"}

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
    def update_linkedin_with_badge(access_token, certification, badge):
        """
        Update the user's LinkedIn profile with badge information.
        This function will create a post on the user's LinkedIn feed announcing the earned badge.
        """
        access_token = (
            certification.user.profile.linkedin_access_token
        )  # Adjust according to your user profile model

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
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
        }

        try:
            response = requests.post(
                post_url, headers=headers, data=json.dumps(post_data)
            )
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
    def add_badge_to_achievements(user, badge, access_token):
        """
        Add the badge to the user's achievements section on LinkedIn.
        """
        user = user  # Get the user profile
        access_token = access_token  # Get LinkedIn access token from user profile

        achievements_url = "https://api.linkedin.com/v2/endorsements"  # Adjust the endpoint as necessary
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Construct the achievement data
        achievement_data = {
            "entityUrn": f"urn:li:badge:{badge.id}",  # Unique identifier for the badge
            "issuer": {
                "name": "Future African Scientist",
                "url": "https://www.futureafricanscientist.org/",
            },
            "badges": [
                {
                    "name": badge.name,
                    "description": badge.description,
                    "imageUrl": badge.image_url,  # URL for the badge image
                    "date": badge.issued_date.isoformat(),  # Date badge was issued
                }
            ],
        }

        # Make the POST request to update achievements
        try:
            response = requests.post(
                achievements_url, headers=headers, data=json.dumps(achievement_data)
            )
            response.raise_for_status()  # Raise an error for bad responses
            print("Badge added to LinkedIn achievements successfully.")
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred while adding badge to achievements: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(
                f"Request error occurred while adding badge to achievements: {req_err}"
            )
