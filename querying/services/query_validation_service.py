# services/query_validation_service.py
from utils.validation import QueryValidator
from querying.models import QueryExecutionPermission
from django.core.exceptions import ValidationError

class QueryValidationService:
    def __init__(self, user=None):
        self.validator = QueryValidator(user=user)
    
    def validate_query_params(self, query_params):
        """
        Validate query parameters.
        """
        self.validator.validate_query_params(query_params)
    
    def has_permission(self, query):
        """
        Check if the user has permission to execute the query.
        """
        try:
            permission = QueryExecutionPermission.objects.get(query=query)
            return self.user.groups.filter(id__in=permission.allowed_groups.all()).exists() or permission.allowed_users.filter(id=self.user.id).exists()
        except QueryExecutionPermission.DoesNotExist:
            raise ValidationError("Permission denied.")