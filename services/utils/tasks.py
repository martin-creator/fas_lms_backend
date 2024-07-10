from django.utils import timezone
from certifications.models import Certification
from utils.notifications import send_notification
import os
import logging
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .file_handling import FileHandler
from .data_processing import DataProcessor
from .storage import StorageHandler
from services.models import FileRecord, Notification
from services.exceptions import TaskException

logger = logging.getLogger(__name__)

@shared_task
def process_uploaded_file(file_id: int):
    """
    Celery task to process an uploaded file.
    """
    try:
        file_record = FileRecord.objects.get(id=file_id)
        file_path = file_record.file_path
        
        # Example processing: parse the file (e.g., extract text, convert format)
        DataProcessor.process_file(file_path)
        
        # Update file record status
        file_record.status = 'processed'
        file_record.save()
        
        logger.info(f"Processed file: {file_path}")
    except FileRecord.DoesNotExist:
        logger.error(f"FileRecord with id {file_id} does not exist.")
        raise TaskException("FileRecord not found.")
    except Exception as e:
        logger.error(f"Error processing file {file_id}: {e}")
        raise TaskException(f"Failed to process file: {e}")

@shared_task
def send_notification_email(notification_id: int):
    """
    Celery task to send notification emails.
    """
    try:
        notification = Notification.objects.get(id=notification_id)
        send_mail(
            subject=notification.subject,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[notification.recipient_email],
        )
        notification.status = 'sent'
        notification.save()
        logger.info(f"Sent notification email to {notification.recipient_email}")
    except Notification.DoesNotExist:
        logger.error(f"Notification with id {notification_id} does not exist.")
        raise TaskException("Notification not found.")
    except Exception as e:
        logger.error(f"Error sending notification email {notification_id}: {e}")
        raise TaskException(f"Failed to send notification email: {e}")

@shared_task
def backup_database():
    """
    Celery task to backup the database.
    """
    try:
        db_name = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_file = os.path.join(backup_dir, f"{db_name}_backup.sql")
        
        os.system(f"pg_dump {db_name} > {backup_file}")
        logger.info(f"Database backup completed: {backup_file}")
    except Exception as e:
        logger.error(f"Error during database backup: {e}")
        raise TaskException(f"Failed to backup database: {e}")

@shared_task
def cleanup_old_files(days: int = 30):
    """
    Celery task to clean up old files that are older than a specified number of days.
    """
    try:
        old_files = FileRecord.objects.filter(created_at__lt=timezone.now() - timezone.timedelta(days=days))
        for file_record in old_files:
            FileHandler.delete_file(file_record.file_path)
            file_record.delete()
        logger.info(f"Cleaned up {old_files.count()} old files.")
    except Exception as e:
        logger.error(f"Error cleaning up old files: {e}")
        raise TaskException(f"Failed to clean up old files: {e}")

@shared_task
def sync_files_to_s3():
    """
    Celery task to synchronize files to S3.
    """
    try:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        files_to_sync = FileRecord.objects.filter(synced_to_s3=False)
        
        for file_record in files_to_sync:
            StorageHandler.upload_to_s3(file_record.file_path, bucket_name, file_record.file_path)
            file_record.synced_to_s3 = True
            file_record.save()
        
        logger.info(f"Synchronized {files_to_sync.count()} files to S3.")
    except Exception as e:
        logger.error(f"Error synchronizing files to S3: {e}")
        raise TaskException(f"Failed to synchronize files to S3: {e}")

@shared_task
def generate_certificate(certification_id: int):
    """
    Celery task to generate a certificate PDF.
    """
    try:
        certification = Certification.objects.get(id=certification_id)
        pdf_path = FileHandler.generate_certificate_pdf(certification)
        certification.pdf_path = pdf_path
        certification.save()
        
        logger.info(f"Generated certificate PDF for certification id {certification_id}")
    except Certification.DoesNotExist:
        logger.error(f"Certification with id {certification_id} does not exist.")
        raise TaskException("Certification not found.")
    except Exception as e:
        logger.error(f"Error generating certificate PDF {certification_id}: {e}")
        raise TaskException(f"Failed to generate certificate PDF: {e}")

@shared_task
def compress_and_archive_files(project_id: int):
    """
    Celery task to compress and archive all files of a project.
    """
    try:
        project_files = FileRecord.objects.filter(project_id=project_id)
        archive_path = f"/tmp/project_{project_id}_archive.zip"
        
        with ZipFile(archive_path, 'w') as archive:
            for file_record in project_files:
                archive.write(file_record.file_path, os.path.basename(file_record.file_path))
        
        StorageHandler.upload_file(open(archive_path, 'rb'), directory='archives')
        
        logger.info(f"Compressed and archived files for project id {project_id}")
    except Exception as e:
        logger.error(f"Error compressing and archiving files for project id {project_id}: {e}")
        raise TaskException(f"Failed to compress and archive files: {e}")
        
def check_expiring_certifications():
    expiring_soon = Certification.objects.filter(expiration_date__lte=timezone.now().date() + timedelta(days=30))
    for cert in expiring_soon:
        send_notification(cert.user, "Your certification is expiring soon.", "Please renew your certification.")
