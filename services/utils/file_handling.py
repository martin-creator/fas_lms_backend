from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.files.storage import default_storage
import os
import shutil
import logging
import mimetypes
from pathlib import Path
from typing import Tuple, Union, List
from django.core.files.uploadedfile import UploadedFile
from django.core.files import File
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.utils.crypto import get_random_string
from celery import shared_task
from services.models import FileRecord, Project
from services.exceptions import FileHandlingException

logger = logging.getLogger(__name__)

# Base directory for file storage
BASE_DIR = settings.MEDIA_ROOT

class FileHandler:
    
    @staticmethod
    def generate_unique_filepath(orig_file_name: str, project_id: int) -> Tuple[str, str]:
        """
        Generate a unique file path to prevent file name collisions.
        """
        file_extension = Path(orig_file_name).suffix
        unique_id = get_random_string(8)
        file_id = f"{unique_id}{file_extension}"
        project_dir = os.path.join(BASE_DIR, 'projects', str(project_id))
        
        # Ensure the directory exists
        os.makedirs(project_dir, exist_ok=True)
        
        file_path = os.path.join(project_dir, file_id)
        
        return file_path, file_id
    
    @staticmethod
    def validate_uploaded_file(file: UploadedFile) -> Tuple[bool, str]:
        """
        Validate uploaded file based on predefined criteria.
        """
        allowed_mimetypes = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
        max_file_size = 10 * 1024 * 1024  # 10MB
        
        if file.size > max_file_size:
            return False, "File size exceeds the allowed limit."
        
        if file.content_type not in allowed_mimetypes:
            return False, "File type is not allowed."
        
        return True, "File is valid."
    
    @staticmethod
    def save_uploaded_file(file: UploadedFile, file_path: str):
        """
        Save uploaded file to the specified path.
        """
        try:
            with open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise FileHandlingException("Failed to save the uploaded file.")
    
    @staticmethod
    def delete_file(file_path: str):
        """
        Delete a file from the filesystem.
        """
        try:
            os.remove(file_path)
        except OSError as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise FileHandlingException(f"Failed to delete file: {file_path}")
    
    @staticmethod
    def get_file_content(file_path: str) -> bytes:
        """
        Read and return the content of the file.
        """
        try:
            with open(file_path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            raise FileHandlingException("File not found.")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise FileHandlingException("Failed to read file content.")
    
    @staticmethod
    def list_files_in_directory(directory: str) -> List[str]:
        """
        List all files in the given directory.
        """
        try:
            return os.listdir(directory)
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"Error listing files in directory {directory}: {e}")
            raise FileHandlingException("Failed to list files in directory.")
    
    @staticmethod
    @shared_task
    def process_uploaded_file(file_path: str):
        """
        Celery task to process the uploaded file asynchronously.
        """
        # Placeholder for actual file processing logic
        try:
            file_content = FileHandler.get_file_content(file_path)
            # Perform processing (e.g., text extraction, format conversion)
            logger.info(f"Processed file: {file_path}")
        except FileHandlingException as e:
            logger.error(f"File processing failed: {e}")
            raise
    
    @staticmethod
    def upload_file(file: UploadedFile, project_id: int) -> str:
        """
        Handle file upload: validate, save, and process.
        """
        is_valid, validation_message = FileHandler.validate_uploaded_file(file)
        if not is_valid:
            raise FileHandlingException(validation_message)
        
        file_path, file_id = FileHandler.generate_unique_filepath(file.name, project_id)
        FileHandler.save_uploaded_file(file, file_path)
        
        # Save file record in the database
        FileRecord.objects.create(
            project_id=project_id,
            file_id=file_id,
            file_path=file_path,
            file_name=file.name,
            file_size=file.size,
            file_type=file.content_type
        )
        
        # Offload processing to Celery
        FileHandler.process_uploaded_file.delay(file_path)
        
        return file_id
    
    @staticmethod
    def download_file(file_id: str, project_id: int) -> Union[File, None]:
        """
        Retrieve a file for download.
        """
        try:
            file_record = FileRecord.objects.get(project_id=project_id, file_id=file_id)
            file_path = file_record.file_path
            return open(file_path, 'rb')
        except FileRecord.DoesNotExist:
            raise FileHandlingException("File record not found.")
        except Exception as e:
            logger.error(f"Error downloading file {file_id}: {e}")
            raise FileHandlingException("Failed to download file.")
    
    @staticmethod
    def delete_project_files(project_id: int):
        """
        Delete all files associated with a project.
        """
        try:
            project_dir = os.path.join(BASE_DIR, 'projects', str(project_id))
            shutil.rmtree(project_dir, ignore_errors=True)
            
            # Delete file records from the database
            FileRecord.objects.filter(project_id=project_id).delete()
        except Exception as e:
            logger.error(f"Error deleting project files for project {project_id}: {e}")
            raise FileHandlingException("Failed to delete project files.")
    
    @staticmethod
    def generate_certificate_pdf(certification):
        """
        Generate a PDF certificate for a user.
        """
        file_path = f"/tmp/{certification.id}.pdf"
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, f"Certificate of Completion")
        c.drawString(100, 725, f"Name: {certification.user.username}")
        c.drawString(100, 700, f"Course: {certification.related_courses.first().name}")
        c.drawString(100, 675, f"Date: {certification.issue_date.strftime('%Y-%m-%d')}")
        c.save()
        return file_path
    
    @staticmethod
    def move_file(src_path: str, dest_path: str):
        """
        Move a file from one location to another.
        """
        try:
            shutil.move(src_path, dest_path)
        except Exception as e:
            logger.error(f"Error moving file from {src_path} to {dest_path}: {e}")
            raise FileHandlingException("Failed to move file.")
    
    @staticmethod
    def copy_file(src_path: str, dest_path: str):
        """
        Copy a file from one location to another.
        """
        try:
            shutil.copy2(src_path, dest_path)
        except Exception as e:
            logger.error(f"Error copying file from {src_path} to {dest_path}: {e}")
            raise FileHandlingException("Failed to copy file.")
    
    @staticmethod
    def archive_project_files(project_id: int) -> str:
        """
        Archive all files associated with a project into a zip file.
        """
        try:
            project_dir = os.path.join(BASE_DIR, 'projects', str(project_id))
            archive_path = f"/tmp/project_{project_id}_archive.zip"
            shutil.make_archive(archive_path.replace('.zip', ''), 'zip', project_dir)
            return archive_path
        except Exception as e:
            logger.error(f"Error archiving project files for project {project_id}: {e}")
            raise FileHandlingException("Failed to archive project files.")
    
    @staticmethod
    def unarchive_project_files(archive_path: str, project_id: int):
        """
        Unarchive files from a zip archive into the project directory.
        """
        try:
            project_dir = os.path.join(BASE_DIR, 'projects', str(project_id))
            shutil.unpack_archive(archive_path, project_dir)
        except Exception as e:
            logger.error(f"Error unarchiving files from {archive_path} to project {project_id}: {e}")
            raise FileHandlingException("Failed to unarchive project files.")