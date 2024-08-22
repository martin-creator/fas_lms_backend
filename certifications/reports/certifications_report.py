from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from certifications.querying.certifications_query import CertificationQuery


class CertificationsReport:

    @staticmethod
    def get_certifications_report(user):
        """
        Get a report for a specific user.
        """
        certifications = CertificationQuery.get_certifications_by_user(user)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod  
    def get_generated_certifications_report():
        """
        Get a report for all generated certifications.
        """
        certifications = Certification.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    
    @staticmethod
    def get_certifications_by_category_report(category):
        """
        Get a report for certifications by category.
        """
        certifications = CertificationQuery.get_certifications_by_category(category)
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    

    @staticmethod
    def get_certifications_by_date_report():
        """
        Get a report for certifications by date.
        """
        certifications = Certification.objects.all()
        serializer = CertificationSerializer(certifications, many=True)
        return serializer.data
    