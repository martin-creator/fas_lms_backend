from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings
from django.core.files.storage import default_storage

class FileHandler:
    @staticmethod
    def upload_file(file, path):
        file_path = os.path.join(path, file.name)
        if not default_storage.exists(file_path):
            default_storage.save(file_path, file)
        return file_path

    @staticmethod
    def delete_file(path):
        if default_storage.exists(path):
            default_storage.delete(path)

def generate_certificate_pdf(certification):
    file_path = f"/tmp/{certification.id}.pdf"
    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, f"Certificate of Completion")
    c.drawString(100, 725, f"Name: {certification.user.username}")
    c.drawString(100, 700, f"Course: {certification.related_courses.first().name}")
    c.drawString(100, 675, f"Date: {certification.issue_date.strftime('%Y-%m-%d')}")
    c.save()
    return file_path
