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

