# helpers/file_helpers.py

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import requests

def upload_file(file, destination):
    # Example: Upload file to default storage
    path = default_storage.save(destination, ContentFile(file.read()))
    return path

def download_file(url, destination):
    # Example: Download file from URL
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as f:
            f.write(response.content)
        return True
    return False

def extract_text_from_pdf(pdf_file):
    # Example: Extract text from PDF file
    # You may use libraries like PyMuPDF or pdfminer for this task
    pass
