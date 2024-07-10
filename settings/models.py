from django.db import models
from profiles.models import UserProfile

# Define Setting Types for categorizing settings
class SettingType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Global settings applicable across the entire LMS
class GlobalSetting(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    value_type = models.CharField(max_length=50)
    default_value = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Module-specific settings linked to specific modules (e.g., Courses, Events)
class ModuleSetting(models.Model):
    module = models.ForeignKey('modules.Module', on_delete=models.CASCADE)  # Adjust 'modules.Module' to your actual module model
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    value_type = models.CharField(max_length=50)
    default_value = models.CharField(max_length=255)
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.module.name} - {self.name}"

# Options for settings that have predefined choices (e.g., dropdown selections)
class SettingOption(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    default_value = models.JSONField()

    def __str__(self):
        return self.name

# Actual values for module settings
class SettingValue(models.Model):
    setting = models.ForeignKey(ModuleSetting, on_delete=models.CASCADE, related_name='values')
    value = models.JSONField()

    def __str__(self):
        return str(self.value)

# Validation rules for module settings
class SettingValidation(models.Model):
    setting = models.ForeignKey(ModuleSetting, on_delete=models.CASCADE, related_name='validations')
    validation_type = models.CharField(max_length=50)
    validation_rule = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.setting} - {self.validation_type}'

# Integration services configuration for external services
class IntegrationService(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    endpoint_url = models.URLField()
    api_key = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

# Reports and analytics on settings usage and configurations
class SettingsReport(models.Model):
    date_generated = models.DateTimeField(auto_now_add=True)
    report_content = models.TextField()
    generated_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Settings Report - {self.date_generated}"
