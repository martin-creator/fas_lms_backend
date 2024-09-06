from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Certification
from profiles.models import User, UserProfile
from jobs.models import JobListing
from courses.models import Course
from notifications.models import Notification
from courses.models import CourseCompletion
from services.utils.file_handling import generate_certificate_pdf
from services.utils.storage import save_certificate_file
from services.utils.notifications import send_notification
from django.utils import timezone

# Signal to send notification when a new certification is created
@receiver(post_save, sender=Certification)
def send_certification_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        notification_message = f"Congratulations! You have earned the {instance.name} certification."
        Notification.objects.create(user=user, message=notification_message)

# Signal to update related job listings when a user earns a new certification
@receiver(post_save, sender=Certification)
def update_related_jobs(sender, instance, created, **kwargs):
    if created:
        related_jobs = instance.related_jobs.all()
        for job in related_jobs:
            job.required_certifications.add(instance)

# Signal to update related courses when a user earns a new certification
@receiver(post_save, sender=Certification)
def update_related_courses(sender, instance, created, **kwargs):
    if created:
        related_courses = instance.related_courses.all()
        for course in related_courses:
            course.required_certifications.add(instance)
            
# signals to Update related jobs and courses when a new certification is earned
@receiver(post_save, sender=Certification)
def update_related_jobs_courses(sender, instance, created, **kwargs):
    if created:
        instance.related_jobs.add(*instance.user.profile.job_listings.all())
        instance.related_courses.add(*instance.user.profile.courses.all())

# Signal to update certification count when a certification is created or deleted
@receiver(post_save, sender=Certification)
@receiver(post_delete, sender=Certification)
def update_certification_count(sender, instance, **kwargs):
    user = instance.user
    user.certification_count = user.certifications.count()
    user.save()

# Signal to notify users when a certification is updated
@receiver(post_save, sender=Certification)
def notify_users_on_certification_update(sender, instance, **kwargs):
    if not instance.verification_status:
        user = instance.user
        notification_message = f"Your {instance.name} certification has been updated. Please verify your information."
        Notification.objects.create(user=user, message=notification_message)


@receiver(post_save, sender=CourseCompletion)
def handle_course_completion(sender, instance, created, **kwargs):
    if created:
        certification = Certification.objects.create(
            user=instance.user,
            name=f"Certificate for {instance.course.name}",
            issuing_organization=instance.course.organization,
            issue_date=instance.completion_date,
            related_courses=[instance.course],
            verification_status=False
        )
        pdf_path = generate_certificate_pdf(certification)
        save_certificate_file(pdf_path, f"certificates/{certification.id}.pdf")
        certification.certificate_file = f"certificates/{certification.id}.pdf"
        certification.save()

@receiver(post_save, sender=Certification)
def certification_update_handler(sender, instance, created, **kwargs):
    if created:
        send_notification(
            user=instance.user,
            message=f"Congratulations! You have been issued a new certification: '{instance.name}'.",
            notification_type='new_certification'
        )
    else:
        if instance.verification_status:
            send_notification(
                user=instance.user,
                message=f"Your certification '{instance.name}' has been verified.",
                notification_type='verification_status_change'
            )
        if instance.expiration_date and instance.expiration_date < timezone.now().date():
            send_notification(
                user=instance.user,
                message=f"Your certification '{instance.name}' has expired. Please renew.",
                notification_type='renewal_reminder'
            )