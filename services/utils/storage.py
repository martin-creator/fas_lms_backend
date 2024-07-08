import shutil
import json
from django.core.cache import cache

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
