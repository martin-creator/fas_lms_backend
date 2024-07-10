from django.db import models

# Create your models here.
# reports/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ReportTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    query = models.ForeignKey('querying.Query', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_templates')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Report(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    template = models.ForeignKey(ReportTemplate, on_delete=models.CASCADE, related_name='reports')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def execute(self, parameters=None):
        # Execute the report using the template query and parameters
        report_execution = ReportExecution(report=self)
        report_execution.save()
        # Add logic to execute report based on the template query
        return report_execution

class ReportExecution(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='executions')
    executed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Execution of {self.report.name} by {self.executed_by.username}'

class Visualization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    report_execution = models.OneToOneField(ReportExecution, on_delete=models.CASCADE, related_name='visualization')
    visualization_data = models.JSONField()

    def __str__(self):
        return self.name

class ScheduledReport(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='schedules')
    scheduled_time = models.DateTimeField()
    repeat_interval = models.DurationField(blank=True, null=True)
    last_executed_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Scheduled {self.report.name} at {self.scheduled_time}'

    def execute(self):
        # Logic to execute the scheduled report
        if self.is_active:
            report_execution = self.report.execute()
            self.last_executed_at = timezone.now()
            self.save()
            return report_execution
        return None

class ExportFormat(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
