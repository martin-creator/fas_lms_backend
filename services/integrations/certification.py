import os
from django.core.files.storage import default_storage


from notifications.services import NotificationService

from certifications.models import Certificate
from notifications.models import Notification
from utils import file_handling , notifications
from courses.models import CourseCompletion


class CertificationService:
    @staticmethod
    def generate_certificate(user, course):
        certificate_url = file_handling.FileHandler.upload_file(course.generate_certificate_pdf(), 'certificates/')
        notifications.NotificationHandler.send_notification(
            user,
            f"Certificate for {course.name} generated successfully!",
            "certificate_generated",
            content_object=course
        )
        return certificate_url

    @staticmethod
    def revoke_certificate(user, course):
        # Assuming we have a Certificate model
        certificate = Certificate.objects.filter(user=user, course=course).first()
        if certificate:
            certificate.is_revoked = True
            certificate.save()
            notifications.NotificationHandler.send_notification(
                user,
                f"Certificate for {course.name} has been revoked.",
                "certificate_revoked",
                content_object=course
            )

    @staticmethod
    def share_certificate(user, platform):
        # Logic to share certificate on the specified platform
        notifications.NotificationHandler.send_notification(
            user,
            f"Certificate shared on {platform}.",
            "certificate_shared"
        )

    @staticmethod
    def get_certification_dashboard(user):
        # Logic to get certification dashboard data
        certificates = Certificate.objects.filter(user=user)
        return {
            "certificates": [cert.to_dict() for cert in certificates]
        }

    @staticmethod
    def get_certification_analytics(user):
        # Logic to get certification analytics
        completed_courses = CourseCompletion.objects.filter(user=user)
        analytics_data = {
            "total_certificates": completed_courses.count(),
            "courses_completed": [course.course.name for course in completed_courses]
        }
        return analytics_data

    @staticmethod
    def integrate_with_learning_path(user, course):
        # Logic to integrate certificate with learning path
        learning_path = LearningPath.objects.filter(user=user, course=course).first()
        if learning_path:
            learning_path.is_completed = True
            learning_path.save()
            notifications.NotificationHandler.send_notification(
                user,
                f"Learning path for {course.name} has been updated with the certificate.",
                "learning_path_updated"
            )

    @staticmethod
    def send_certification_update_notifications(user):
        # Logic to send certification update notifications
        notifications = Notification.objects.filter(user=user, notification_type="certificate_update")
        return [notification.to_dict() for notification in notifications]
