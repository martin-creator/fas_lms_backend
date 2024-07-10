from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import Group
from django.conf import settings

class QueryCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Query(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(QueryCategory, on_delete=models.CASCADE, related_name='queries')
    query_params = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class QueryParameter(models.Model):
    DATA_TYPE_CHOICES = [
        ('integer', 'Integer'),
        ('string', 'String'),
        ('boolean', 'Boolean'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)  # Choices for data type
    default_value = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        # Example validation logic (customize as per project requirements)
        if self.data_type == 'integer':
            try:
                int(self.default_value)
            except ValueError:
                raise ValidationError("Default value must be an integer.")

class QueryExecutionPermission(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='execution_permissions')
    allowed_groups = models.ManyToManyField(Group, blank=True)
    allowed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return f"Execution Permissions for {self.query.name}"

    def has_permission(self, user):
        return user.groups.filter(id__in=self.allowed_groups.all()).exists() or self.allowed_users.filter(id=user.id).exists()

class QueryLog(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='logs')
    executed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    execution_duration = models.FloatField()  # Execution time in seconds
    executed_query = models.TextField()
    client_ip = models.CharField(max_length=50, blank=True, null=True)  # Store client IP address

    def __str__(self):
        return f"Query Execution Log for {self.query.name} by {self.executed_by} at {self.executed_at}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.executed_query = self.query.query_params.get('query', '')
        super().save(*args, **kwargs)

class QueryResult(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='results')
    result_data = JSONField()
    executed_at = models.DateTimeField(auto_now_add=True)
    num_rows_returned = models.IntegerField()  # Example metadata field

    def __str__(self):
        return f"Result of {self.query.name} at {self.executed_at}"