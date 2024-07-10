import shutil
import json
from django.core.cache import cache
import logging
import os
from pathlib import Path
from typing import List, Union
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage, FileSystemStorage
from django.core.exceptions import SuspiciousFileOperation
from django.utils.crypto import get_random_string
from services.exceptions import StorageException
from celery import shared_task
from boto3.session import Session
from google.cloud import storage as gcs

logger = logging.getLogger(__name__)

class StorageHandler:
    @staticmethod
    def generate_unique_filepath(orig_file_name: str, directory: str = '') -> str:
        """
        Generate a unique file path to prevent file name collisions.
        """
        file_extension = Path(orig_file_name).suffix
        unique_id = get_random_string(8)
        file_id = f"{unique_id}{file_extension}"
        file_path = os.path.join(directory, file_id) if directory else file_id
        return file_path
    
    @staticmethod
    def validate_file(file: UploadedFile) -> bool:
        """
        Validate file based on predefined criteria.
        """
        allowed_mimetypes = ['application/pdf', 'image/jpeg', 'image/png', 'text/plain']
        max_file_size = 10 * 1024 * 1024  # 10MB
        
        if file.size > max_file_size:
            raise StorageException("File size exceeds the allowed limit.")
        
        if file.content_type not in allowed_mimetypes:
            raise StorageException("File type is not allowed.")
        
        return True

    @staticmethod
    def save_file(file: UploadedFile, file_path: str) -> str:
        """
        Save uploaded file to the specified path.
        """
        try:
            with default_storage.open(file_path, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return file_path
        except Exception as e:
            logger.error(f"Failed to save file: {e}")
            raise StorageException("Failed to save the uploaded file.")

    @staticmethod
    def delete_file(file_path: str):
        """
        Delete a file from the storage system.
        """
        try:
            default_storage.delete(file_path)
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")
            raise StorageException("Failed to delete file.")

    @staticmethod
    def list_files(directory: str = '') -> List[str]:
        """
        List all files in the given directory.
        """
        try:
            return default_storage.listdir(directory)[1]
        except Exception as e:
            logger.error(f"Error listing files in directory {directory}: {e}")
            raise StorageException("Failed to list files in directory.")

    @staticmethod
    def download_file(file_path: str) -> bytes:
        """
        Download a file from the storage system.
        """
        try:
            with default_storage.open(file_path, 'rb') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error downloading file {file_path}: {e}")
            raise StorageException("Failed to download file.")
    
    @staticmethod
    @shared_task
    def async_delete_file(file_path: str):
        """
        Celery task to delete a file asynchronously.
        """
        try:
            StorageHandler.delete_file(file_path)
            logger.info(f"File {file_path} deleted asynchronously.")
        except StorageException as e:
            logger.error(f"File deletion failed: {e}")
            raise
    
    @staticmethod
    def upload_to_s3(file: UploadedFile, bucket_name: str, file_path: str) -> str:
        """
        Upload a file to AWS S3.
        """
        session = Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        s3 = session.resource('s3')
        try:
            s3.Bucket(bucket_name).put_object(Key=file_path, Body=file)
                        return f"s3://{bucket_name}/{file_path}"
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise StorageException("Failed to upload file to S3.")
    
    @staticmethod
    def download_from_s3(bucket_name: str, file_path: str) -> bytes:
        """
        Download a file from AWS S3.
        """
        session = Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        s3 = session.resource('s3')
        try:
            obj = s3.Object(bucket_name, file_path)
            return obj.get()['Body'].read()
        except Exception as e:
            logger.error(f"Error downloading file from S3: {e}")
            raise StorageException("Failed to download file from S3.")
    
    @staticmethod
    def upload_to_gcs(file: UploadedFile, bucket_name: str, file_path: str) -> str:
        """
        Upload a file to Google Cloud Storage.
        """
        client = gcs.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        try:
            blob.upload_from_file(file)
            return f"gs://{bucket_name}/{file_path}"
        except Exception as e:
            logger.error(f"Error uploading file to GCS: {e}")
            raise StorageException("Failed to upload file to GCS.")
    
    @staticmethod
    def download_from_gcs(bucket_name: str, file_path: str) -> bytes:
        """
        Download a file from Google Cloud Storage.
        """
        client = gcs.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        try:
            return blob.download_as_bytes()
        except Exception as e:
            logger.error(f"Error downloading file from GCS: {e}")
            raise StorageException("Failed to download file from GCS.")
    
    @staticmethod
    def async_process_file(file_path: str):
        """
        Celery task to process a file asynchronously.
        Placeholder for actual processing logic.
        """
        try:
            # Example processing: simply read the file content
            file_content = StorageHandler.download_file(file_path)
            # Perform actual processing here (e.g., parsing, conversion)
            logger.info(f"Processed file: {file_path}")
        except StorageException as e:
            logger.error(f"File processing failed: {e}")
            raise
    
    @staticmethod
    def upload_file(file: UploadedFile, directory: str = '') -> str:
        """
        Handle file upload: validate and save.
        """
        StorageHandler.validate_file(file)
        file_path = StorageHandler.generate_unique_filepath(file.name, directory)
        StorageHandler.save_file(file, file_path)
        return file_path
    
    @staticmethod
    def delete_directory(directory: str):
        """
        Delete all files in the given directory.
        """
        try:
            file_list = StorageHandler.list_files(directory)
            for file_name in file_list:
                StorageHandler.delete_file(os.path.join(directory, file_name))
        except StorageException as e:
            logger.error(f"Failed to delete directory {directory}: {e}")
            raise


class StorageService:
    @staticmethod
    def save_to_cache(key, value, timeout=300):
        cache.set(key, value, timeout)

    @staticmethod
    def get_from_cache(key):
        return cache.get(key)

    @staticmethod
    def save_to_db(model_instance):
        model_instance.save()

    @staticmethod
    def retrieve_from_db(model_class, **filters):
        return model_class.objects.filter(**filters)

def save_certificate_file(file_path, destination_path):
    shutil.move(file_path, destination_path)

def retrieve_certificate_file(path):
    with open(path, 'rb') as file:
        return file.read()
