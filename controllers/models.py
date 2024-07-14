from django.db import models

class RegisteredController(models.Model):
    name = models.CharField(max_length=100)
    app_name = models.CharField(max_length=100)
    description = models.TextField()
    endpoint = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.app_name})"
