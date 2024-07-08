import os
from django.core.files.storage import default_storage
from notifications.services import NotificationService
from certifications.models import Certificate
from notifications.models import Notification
from utils import file_handling, notifications
from courses.models import CourseCompletion, LearningPath
from utils.email_integration import EmailService

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
        EmailService.send_email(
            subject=f"Certificate Generated for {course.name}",
            message=f"Congratulations {user.first_name}, your certificate for {course.name} has been generated. You can download it from {certificate_url}.",
            recipient_list=[user.email],
        )
        return certificate_url

    @staticmethod
    def revoke_certificate(user, course):
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
            EmailService.send_email(
                subject=f"Certificate Revoked for {course.name}",
                message=f"Dear {user.first_name}, your certificate for {course.name} has been revoked.",
                recipient_list=[user.email],
            )

    @staticmethod
    def share_certificate(user, platform):
        notifications.NotificationHandler.send_notification(
            user,
            f"Certificate shared on {platform}.",
            "certificate_shared"
        )
        EmailService.send_email(
            subject="Certificate Shared",
            message=f"Your certificate has been shared on {platform}.",
            recipient_list=[user.email],
        )

    @staticmethod
    def get_certification_dashboard(user):
        certificates = Certificate.objects.filter(user=user)
        return {
            "certificates": [cert.to_dict() for cert in certificates]
        }

    @staticmethod
    def get_certification_analytics(user):
        completed_courses = CourseCompletion.objects.filter(user=user)
        analytics_data = {
            "total_certificates": completed_courses.count(),
            "courses_completed": [course.course.name for course in completed_courses]
        }
        notifications.NotificationHandler.send_notification(
            user,
            "New analytics report available for your certifications.",
            "certificate_analytics"
        )
        EmailService.send_email(
            subject="Certification Analytics Report",
            message="A new analytics report is available for your certifications.",
            recipient_list=[user.email],
        )
        return analytics_data

    @staticmethod
    def integrate_with_learning_path(user, course):
        learning_path = LearningPath.objects.filter(user=user, course=course).first()
        if learning_path:
            learning_path.is_completed = True
            learning_path.save()
            notifications.NotificationHandler.send_notification(
                user,
                f"Learning path for {course.name} has been updated with the certificate.",
                "learning_path_updated"
            )
            EmailService.send_email(
                subject="Learning Path Updated",
                message=f"Your learning path for {course.name} has been updated with the new certificate.",
                recipient_list=[user.email],
            )

    @staticmethod
    def send_certification_update_notifications(user):
        notifications = Notification.objects.filter(user=user, notification_type="certificate_update")
        for notification in notifications:
            NotificationService.create_notification(
                recipient=user,
                content=notification.message,
                notification_type_name=notification.notification_type.type_name,
                content_object=notification.content_object,
                priority=notification.priority
            )
        return [notification.to_dict() for notification in notifications]
