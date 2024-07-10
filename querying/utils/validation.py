# utils/validation.py
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from .logging import log_data_access, handle_query_execution_error
import re
import logging

logger = logging.getLogger(__name__)

User = get_user_model()


class QueryValidator:
    def __init__(self, user=None):
        self.user = user
    
    def validate_query_params(self, query_params):
        """
        Validate query parameters format and values.
        Example: Check required fields, data types, etc.
        """
        if not isinstance(query_params, dict):
            raise ValidationError("Query parameters must be a dictionary.")
        
        required_fields = ['param1', 'param2']
        for field in required_fields:
            if field not in query_params:
                raise ValidationError(f"Missing required field: {field}.")
            if not isinstance(query_params[field], str):
                raise ValidationError(f"Field '{field}' must be a string.")
    
    def check_query_execution_permission(self, query):
        """
        Check if the user has permission to execute the query.
        """
        User = get_user_model()
        if self.user.is_authenticated and self.user.has_perm('query_app.execute_query'):
            return True
        else:
            return False
    
    def validate_sql_syntax(self, sql_query):
        """
        Validate SQL syntax before executing the query.
        Example: Check for potential SQL injection risks.
        """
        if ";" in sql_query:
            raise ValidationError("Multiple SQL statements detected, potential SQL injection risk.")
        # Add more syntax validation as needed
    
    def sanitize_input(self, input_data):
        """
        Sanitize query inputs to prevent SQL injection attacks.
        Example: Remove potentially harmful characters.
        """
        sanitized_data = re.sub(r'[;\'\"]', '', input_data)  # Remove specific characters
        return sanitized_data
    
    def validate_data_integrity(self, data):
        """
        Check data integrity before executing operations.
        Example: Ensure required fields are populated correctly.
        """
        if not data.get('required_field'):
            raise ValidationError("Required field is missing.")
        # Add more integrity checks as needed
    
    def validate_configuration(self):
        """
        Validate application configuration settings.
        Example: Check database connection settings.
        """
        if not settings.DATABASES['default'].get('HOST'):
            raise ValidationError("Database configuration error: Host not specified.")
        # Add more configuration checks as needed
    
    def handle_validation_error(self, error_message):
        """
        Handle validation errors gracefully.
        """
        try:
            raise ValidationError(error_message)
        except ValidationError as e:
            # Example: Log the error
            handle_query_execution_error(e)

    # Additional Custom Validators
    def validate_unique_email(self, email):
        """
        Validate if the email is unique across the system.
        """
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists in the system.")

    def validate_unique_username(self, username):
        """
        Validate if the username is unique across the system.
        """
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists in the system.")

    def validate_user_exists(self, user_id):
        """
        Validate if the user with given user_id exists in the system.
        """
        User = get_user_model()
        if not User.objects.filter(id=user_id).exists():
            raise ValidationError("User does not exist.")

    def validate_user_active(self):
        """
        Validate if the user is active.
        """
        if not self.user.is_active:
            raise ValidationError("User is not active.")
    
    # Add more custom validators as per your application's requirements

class QueryParamsValidator:
    @staticmethod
    def validate(query_params):
        """
        Validate query parameters format and values.
        Example: Check required fields, data types, etc.
        """
        if not isinstance(query_params, dict):
            raise ValidationError("Query parameters must be a dictionary.")
        
        # Example: Validate specific fields and their types
        required_fields = ['param1', 'param2']
        for field in required_fields:
            if field not in query_params:
                raise ValidationError(f"Missing required field: {field}.")
            # Example: Ensure specific data types
            if not isinstance(query_params[field], str):
                raise ValidationError(f"Field '{field}' must be a string.")
        
        # Add more validation logic as needed

class QueryExecutionPermissionValidator:
    @staticmethod
    def check(query, user):
        """
        Check if the user has permission to execute the query.
        """
        User = get_user_model()
        # Example logic: Implement your permission checks based on user roles/groups
        if user.is_authenticated and user.has_perm('query_app.execute_query'):
            return True
        else:
            return False

class SQLSyntaxValidator:
    @staticmethod
    def validate(sql_query):
        """
        Validate SQL syntax before executing the query.
        Example: Check for potential SQL injection risks.
        """
        if ";" in sql_query:
            raise ValidationError("Multiple SQL statements detected, potential SQL injection risk.")
        # Add more syntax validation as needed

class InputSanitizer:
    @staticmethod
    def sanitize(input_data):
        """
        Sanitize query inputs to prevent SQL injection attacks.
        Example: Remove potentially harmful characters.
        """
        sanitized_data = re.sub(r'[;\'\"]', '', input_data)  # Remove specific characters
        return sanitized_data

class DataIntegrityValidator:
    @staticmethod
    def check(data):
        """
        Check data integrity before executing operations.
        Example: Ensure required fields are populated correctly.
        """
        if not data.get('required_field'):
            raise ValidationError("Required field is missing.")
        # Add more integrity checks as needed

class ConfigurationValidator:
    @staticmethod
    def validate():
        """
        Validate application configuration settings.
        Example: Check database connection settings.
        """
        if not settings.DATABASES['default'].get('HOST'):
            raise ValidationError("Database configuration error: Host not specified.")
        # Add more configuration checks as needed

class UserValidator:
    @staticmethod
    def exists(user_id):
        """
        Validate if the user with given user_id exists in the system.
        """
        User = get_user_model()
        if not User.objects.filter(id=user_id).exists():
            raise ValidationError("User does not exist.")
    
    @staticmethod
    def active(user):
        """
        Validate if the user is active.
        """
        if not user.is_active:
            raise ValidationError("User is not active.")
    
    @staticmethod
    def has_permission(user, required_permission):
        """
        Validate if the user has the required permission.
        """
        if not user.has_perm(required_permission):
            raise ValidationError(f"User does not have permission: {required_permission}")
    
    @staticmethod
    def is_superuser(user):
        """
        Validate if the user is a superuser.
        """
        if not user.is_superuser:
            raise ValidationError("User is not a superuser.")
    
    @staticmethod
    def is_staff(user):
        """
        Validate if the user is staff.
        """
        if not user.is_staff:
            raise ValidationError("User is not staff.")
    
    @staticmethod
    def is_owner(user, instance):
        """
        Validate if the user is the owner of the instance.
        """
        if instance.user != user:
            raise ValidationError("User is not the owner of the instance.")
    
    @staticmethod
    def is_instructor(user):
        """
        Validate if the user is an instructor (custom logic example).
        """
        # Example custom logic for instructor validation
        if not user.profile.is_instructor:
            raise ValidationError("User is not an instructor.")

class CourseValidator:
    @staticmethod
    def enrollment(user, course):
        """
        Validate if the user is enrolled in the course.
        """
        if not user.profile.enrollments.filter(course=course).exists():
            raise ValidationError("User is not enrolled in the course.")
    
    @staticmethod
    def enrollment_capacity(course):
        """
        Validate if the course has reached its maximum enrollment capacity.
        """
        if course.enrollments.count() >= course.max_capacity:
            raise ValidationError("Course has reached its maximum enrollment capacity.")
    
    @staticmethod
    def enrollment_deadline(course):
        """
        Validate if the enrollment deadline for the course has passed.
        """
        if course.enrollment_deadline and course.enrollment_deadline < timezone.now():
            raise ValidationError("Enrollment deadline for the course has passed.")

class GradeValidator:
    @staticmethod
    def range(grade):
        """
        Validate if the grade falls within a specific range.
        """
        if not (0 <= grade <= 100):
            raise ValidationError("Grade must be between 0 and 100.")

class AssignmentValidator:
    @staticmethod
    def submission(user, assignment):
        """
        Validate if the user has submitted the assignment.
        """
        if not assignment.submissions.filter(submitted_by=user).exists():
            raise ValidationError("User has not submitted the assignment.")
    
    @staticmethod
    def deadline(assignment):
        """
        Validate if the assignment submission deadline has passed.
        """
        if assignment.deadline and assignment.deadline < timezone.now():
            raise ValidationError("Assignment submission deadline has passed.")

class QuizValidator:
    @staticmethod
    def submission(user, quiz):
        """
        Validate if the user has submitted the quiz.
        """
        if not quiz.submissions.filter(submitted_by=user).exists():
            raise ValidationError("User has not submitted the quiz.")
    
    @staticmethod
    def time_limit(quiz):
        """
        Validate if the time limit for the quiz has been exceeded.
        """
        if quiz.time_limit and quiz.time_limit < timezone.now() - quiz.start_time:
            raise ValidationError("Time limit for the quiz has been exceeded.")



#####################################################################################


# class ActivityValidator:
#     @staticmethod
#     def validate_activity_log(activity_log):
#         """
#         Validate user activity log before saving.
#         Example: Ensure required fields are present and formatted correctly.
#         """
#         required_fields = ['user', 'action', 'timestamp']
#         for field in required_fields:
#             if field not in activity_log:
#                 raise ValidationError(f"Missing required field '{field}' in activity log.")
        
#         if not isinstance(activity_log['user'], int):
#             raise ValidationError("User ID must be an integer in activity log.")
        
#         # Additional validations as per activity log structure
    
#     @staticmethod
#     def validate_notification(notification):
#         """
#         Validate notification details before sending.
#         Example: Check fields like recipient_id, message, notification_type, etc.
#         """
#         required_fields = ['recipient_id', 'message', 'notification_type']
#         for field in required_fields:
#             if field not in notification:
#                 raise ValidationError(f"Missing required field '{field}' in notification.")
        
#         # Additional validations for notification services

# class CertificationValidator:
#     @staticmethod
#     def validate_certification(certification):
#         """
#         Validate certification details before issuance.
#         Example: Check fields like title, issuing authority, expiration date, etc.
#         """
#         required_fields = ['title', 'issuer', 'expiration_date']
#         for field in required_fields:
#             if field not in certification:
#                 raise ValidationError(f"Missing required field '{field}' in certification details.")
        
#         if not isinstance(certification['expiration_date'], timezone.datetime):
#             raise ValidationError("Certification expiration date must be a valid datetime object.")
        
#         # Additional validations for certification lifecycle management
    
#     @staticmethod
#     def validate_certification_expiration(certification):
#         """
#         Validate certification expiration date.
#         """
#         if 'expiration_date' in certification:
#             if certification['expiration_date'] < timezone.now():
#                 raise ValidationError("Certification has expired.")
#         else:
#             raise ValidationError("Certification expiration date is required.")

# class CompanyProfileValidator:
#     @staticmethod
#     def validate_company_profile(company_profile):
#         """
#         Validate company profile details before update.
#         Example: Check fields like name, address, industry, contact information, etc.
#         """
#         required_fields = ['name', 'address', 'industry']
#         for field in required_fields:
#             if field not in company_profile:
#                 raise ValidationError(f"Missing required field '{field}' in company profile.")
        
#         # Additional validations for company profile management

# class ConnectionValidator:
#     @staticmethod
#     def validate_connection(connection):
#         """
#         Validate user connection details.
#         Example: Check fields like user_id, connection_id, connection_status, etc.
#         """
#         required_fields = ['user_id', 'connection_id', 'connection_status']
#         for field in required_fields:
#             if field not in connection:
#                 raise ValidationError(f"Missing required field '{field}' in connection details.")
        
#         # Additional validations for user connection management

# class CourseValidator:
#     @staticmethod
#     def validate_course(course):
#         """
#         Validate course details before creation or update.
#         Example: Check fields like title, description, prerequisites, etc.
#         """
#         required_fields = ['title', 'description']
#         for field in required_fields:
#             if field not in course:
#                 raise ValidationError(f"Missing required field '{field}' in course details.")
        
#         # Additional validations for course operations
    
#     @staticmethod
#     def validate_module(module):
#         """
#         Validate module details.
#         Example: Check fields like title, content, duration, etc.
#         """
#         required_fields = ['title', 'content', 'duration']
#         for field in required_fields:
#             if field not in module:
#                 raise ValidationError(f"Missing required field '{field}' in module details.")
        
#         # Additional validations for module management
    
#     @staticmethod
#     def validate_quiz(quiz):
#         """
#         Validate quiz details.
#         Example: Check fields like title, questions, duration, etc.
#         """
#         required_fields = ['title', 'questions', 'duration']
#         for field in required_fields:
#             if field not in quiz:
#                 raise ValidationError(f"Missing required field '{field}' in quiz details.")
        
#         # Additional validations for quiz management
    
#     @staticmethod
#     def validate_assignment(assignment):
#         """
#         Validate assignment details.
#         Example: Check fields like title, description, deadline, etc.
#         """
#         required_fields = ['title', 'description', 'deadline']
#         for field in required_fields:
#             if field not in assignment:
#                 raise ValidationError(f"Missing required field '{field}' in assignment details.")
        
#         # Additional validations for assignment management

# class EventValidator:
#     @staticmethod
#     def validate_event(event):
#         """
#         Validate event details before creation or update.
#         Example: Check fields like title, description, start_date, end_date, etc.
#         """
#         required_fields = ['title', 'description', 'start_date', 'end_date']
#         for field in required_fields:
#             if field not in event:
#                 raise ValidationError(f"Missing required field '{field}' in event details.")
        
#         # Additional validations for event management

# class FollowerValidator:
#     @staticmethod
#     def validate_follower(follower):
#         """
#         Validate follower details before subscription.
#         Example: Check fields like follower_id, followee_id, subscription_status, etc.
#         """
#         required_fields = ['follower_id', 'followee_id']
#         for field in required_fields:
#             if field not in follower:
#                 raise ValidationError(f"Missing required field '{field}' in follower details.")
        
#         # Additional validations for follower system

# class GroupValidator:
#     @staticmethod
#     def validate_group(group):
#         """
#         Validate group details before creation or update.
#         Example: Check fields like title, description, members, group_type, etc.
#         """
#         required_fields = ['title', 'description', 'members']
#         for field in required_fields:
#             if field not in group:
#                 raise ValidationError(f"Missing required field '{field}' in group details.")
        
#         # Additional validations for group management

# class JobListingValidator:
#     @staticmethod
#     def validate_job_listing(job_listing):
#         """
#         Validate job listing details before posting.
#         Example: Check fields like title, description, requirements, etc.
#         """
#         required_fields = ['title', 'description', 'requirements']
#         for field in required_fields:
#             if field not in job_listing:
#                 raise ValidationError(f"Missing required field '{field}' in job listing details.")
        
#         # Additional validations for job listings

# class MessageValidator:
#     @staticmethod
#     def validate_message(message):
#         """
#         Validate message details before sending.
#         Example: Check fields like sender_id, recipient_id, message_content, etc.
#         """
#         required_fields = ['sender_id', 'recipient_id', 'message_content']
#         for field in required_fields:
#             if field not in message:
#                 raise ValidationError(f"Missing required field '{field}' in message details.")
        
#         # Additional validations for messaging services

# class PostValidator:
#     @staticmethod
#     def validate_post(post):
#         """
#         Validate post details before publishing.
#         Example: Check fields like author_id, content, publish_date, etc.
#         """
#         required_fields = ['author_id', 'content', 'publish_date']
#         for field in required_fields:
#             if field not in post:
#                 raise ValidationError(f"Missing required field '{field}' in post details.")
        
#         # Additional validations for post management

# class ProfileValidator:
#     @staticmethod
#     def validate_profile(profile):
#         """
#         Validate user profile details before update.
#         Example: Check fields like user_id, bio, interests, etc.
#         """
#         required_fields = ['user_id', 'bio', 'interests']
#         for field in required_fields:
#             if field not in profile:
#                 raise ValidationError(f"Missing required field '{field}' in user profile.")
        
#         # Additional validations for profile management

# class SettingsValidator:
#     @staticmethod
#     def validate_settings(settings_data):
#         """
#         Validate system-wide or module-specific settings.
#         Example: Check fields like setting_name, setting_value, etc.
#         """
#         required_fields = ['setting_name', 'setting_value']
#         for field in required_fields:
#             if field not in settings_data:
#                 raise ValidationError(f"Missing required field '{field}' in settings.")
        
#         # Additional validations for settings configuration

# class ReportValidator:
#     @staticmethod
#     def validate_report_generation(report_params):
#         """
#         Validate parameters for report generation.
#         Example: Check fields like report_type, start_date, end_date, etc.
#         """
#         required_fields = ['report_type', 'start_date', 'end_date']
#         for field in required_fields:
#             if field not in report_params:
#                 raise ValidationError(f"Missing required field '{field}' for report generation.")
        
#         # Additional validations for report generation

# class PaymentValidator:
#     @staticmethod
#     def validate_payment_transaction(transaction):
#         """
#         Validate payment transaction details.
#         Example: Check fields like amount, currency, transaction_id, etc.
#         """
#         required_fields = ['amount', 'currency', 'transaction_id']
#         for field in required_fields:
#             if field not in transaction:
#                 raise ValidationError(f"Missing required field '{field}' in payment transaction.")
        
#         # Additional validations for payment processing

# class NotificationValidator:
#     @staticmethod
#     def validate_notification(notification):
#         """
#         Validate notification details before sending.
#         Example: Check fields like recipient_id, message, notification_type, etc.
#         """
#         required_fields = ['recipient_id', 'message', 'notification_type']
#         for field in required_fields:
#             if field not in notification:
#                 raise ValidationError(f"Missing required field '{field}' in notification.")
        
#         # Additional validations for notification services
