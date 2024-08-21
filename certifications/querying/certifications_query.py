from django.db.models import Count, Q
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from django.utils import timezone


class CertificationQuery:
    @staticmethod
    def get_certifications():
        """
        Get all certifications.
        """
        certifications = Certification.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certification(certification_id):
        """
        Get a specific certification.
        """
        certification = Certification.objects.get(id=certification_id)
        serializer = CertificationSerializer(certification)
        return serializer.data

    @staticmethod
    def get_certifications_by_user(user_id):
        """
        Get all certifications for a specific user.
        """
        certifications = Certification.objects.filter(user_id=user_id)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_category(category_id):
        """
        Get all certifications in a specific category.
        """
        certifications = Certification.objects.filter(categories=category_id)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_issuing_organization(issuing_organization):
        """
        Get all certifications from a specific issuing organization.
        """
        certifications = Certification.objects.filter(issuing_organization=issuing_organization)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_issue_date(issue_date):
        """
        Get all certifications issued on a specific date.
        """
        certifications = Certification.objects.filter(issue_date=issue_date)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_expiration_date(expiration_date):
        """
        Get all certifications expiring on a specific date.
        """
        certifications = Certification.objects.filter(expiration_date=expiration_date)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_verification_status(verification_status):
        """
        Get all certifications with a specific verification status.
        """
        certifications = Certification.objects.filter(verification_status=verification_status)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data

    @staticmethod
    def get_certifications_by_revoked(revoked):
        """
        Get all certifications with a specific revoked status.
        """
        certifications = Certification.objects.filter(revoked=revoked)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_certifications_by_name(name):
        """
        Get all certifications with a specific name.
        """
        certifications = Certification.objects.filter(name=name)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_certifications_by_credential_id(credential_id):
        """
        Get all certifications with a specific credential ID.
        """
        certifications = Certification.objects.filter(credential_id=credential_id)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_certifications_by_credential_url(credential_url):
        """
        Get all certifications with a specific credential URL.
        """
        certifications = Certification.objects.filter(credential_url=credential_url)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_linked_in_badges():
        """
        Get all LinkedIn badges.
        """
        linked_in_badges = LinkedInBadge.objects.all()
        serializer = LinkedInBadgeSerializer(linked_in_badges, many=True)
        return serializer.data
    

    @staticmethod
    def get_linked_in_badge(linked_in_badge_id):
        """
        Get a specific LinkedIn badge.
        """
        linked_in_badge = LinkedInBadge.objects.get(id=linked_in_badge_id)
        serializer = LinkedInBadgeSerializer(linked_in_badge)
        return serializer.data
    

    @staticmethod
    def get_linked_in_badges_by_certification(certification_id):
        """
        Get all LinkedIn badges for a specific certification.
        """
        linked_in_badges = LinkedInBadge.objects.filter(certification_id=certification_id)
        serializer = LinkedInBadgeSerializer(linked_in_badges, many=True)
        return serializer.data
    

    @staticmethod
    def get_linked_in_badges_by_user(user_id):
        """
        Get all LinkedIn badges for a specific user.
        """
        linked_in_badges = LinkedInBadge.objects.filter(user_id=user_id)
        serializer = LinkedInBadgeSerializer(linked_in_badges, many=True)
        return serializer.data



    @staticmethod
    def delete_certification(certification_id):
        """
        Delete a certification.
        """
        certification = Certification.objects.get(id=certification_id)
        certification.delete()

        return True
    

    @staticmethod
    def delete_linked_in_badge(linked_in_badge_id):
        """
        Delete a LinkedIn badge.
        """
        linked_in_badge = LinkedInBadge.objects.get(id=linked_in_badge_id)
        linked_in_badge.delete()

        return True
    

    @staticmethod
    def delete_all_certifications():
        """
        Delete all certifications.
        """
        certifications = Certification.objects.all()
        certifications.delete()

        return True
    

    @staticmethod
    def delete_all_linked_in_badges():
        """
        Delete all LinkedIn badges.
        """
        linked_in_badges = LinkedInBadge.objects.all()
        linked_in_badges.delete()

        return True
    

    @staticmethod
    def delete_all_certifications_and_linked_in_badges():
        """
        Delete all certifications and LinkedIn badges.
        """
        certifications = Certification.objects.all()
        certifications.delete()

        linked_in_badges = LinkedInBadge.objects.all()
        linked_in_badges.delete()

        return True