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

class ValidationErrorDetail(ValidationError):
    """
    Custom validation error with detailed messages.
    """
    pass

class QueryValidator:
    def __init__(self, user=None):
        self.user = user
    
    def validate_query_params(self, query_params):
        """
        Validate query parameters format and values.
        """
        if not isinstance(query_params, dict):
            raise ValidationErrorDetail("Query parameters must be a dictionary.")
        
        required_fields = ['param1', 'param2']
        for field in required_fields:
            if field not in query_params:
                raise ValidationErrorDetail(f"Missing required field: {field}.")
            if not isinstance(query_params[field], str):
                raise ValidationErrorDetail(f"Field '{field}' must be a string.")
    
    def validate_sql_syntax(self, sql_query):
        """
        Validate SQL syntax to prevent SQL injection risks.
        """
        if ";" in sql_query:
            raise ValidationErrorDetail("Potential SQL injection risk detected.")
        # Add additional SQL syntax validation if needed
    
    def sanitize_input(self, input_data):
        """
        Sanitize query inputs to prevent SQL injection.
        """
        return re.sub(r'[;\'\"]', '', input_data)
    
    def validate_data_integrity(self, data):
        """
        Check data integrity before executing operations.
        """
        if not data.get('required_field'):
            raise ValidationErrorDetail("Required field is missing.")
        # Add additional data integrity checks if needed
    
    def validate_configuration(self):
        """
        Validate application configuration settings.
        """
        if not settings.DATABASES['default'].get('HOST'):
            raise ValidationErrorDetail("Database configuration error: Host not specified.")
        # Add additional configuration checks if needed
    
    def handle_validation_error(self, error_message):
        """
        Handle validation errors and log them.
        """
        logger.error(f"Validation error: {error_message}")
        handle_query_execution_error(ValidationErrorDetail(error_message))

class UserValidator:
    @staticmethod
    def exists(user_id):
        """
        Validate if the user with the given user_id exists.
        """
        if not User.objects.filter(id=user_id).exists():
            raise ValidationErrorDetail("User does not exist.")
    
    @staticmethod
    def active(user):
        """
        Validate if the user is active.
        """
        if not user.is_active:
            raise ValidationErrorDetail("User is not active.")
    
    @staticmethod
    def has_permission(user, required_permission):
        """
        Validate if the user has the required permission.
        """
        if not user.has_perm(required_permission):
            raise ValidationErrorDetail(f"User lacks required permission: {required_permission}.")
    
    @staticmethod
    def is_superuser(user):
        """
        Validate if the user is a superuser.
        """
        if not user.is_superuser:
            raise ValidationErrorDetail("User is not a superuser.")
    
    @staticmethod
    def is_staff(user):
        """
        Validate if the user is staff.
        """
        if not user.is_staff:
            raise ValidationErrorDetail("User is not staff.")
    
    @staticmethod
    def is_owner(user, instance):
        """
        Validate if the user is the owner of the instance.
        """
        if instance.user != user:
            raise ValidationErrorDetail("User is not the owner of the instance.")
    
    @staticmethod
    def is_instructor(user):
        """
        Validate if the user is an instructor.
        """
        if not user.profile.is_instructor:
            raise ValidationErrorDetail("User is not an instructor.")

class CourseValidator:
    @staticmethod
    def enrollment(user, course):
        """
        Validate if the user is enrolled in the course.
        """
        if not user.profile.enrollments.filter(course=course).exists():
            raise ValidationErrorDetail("User is not enrolled in the course.")
    
    @staticmethod
    def enrollment_capacity(course):
        """
        Validate if the course has reached its maximum enrollment capacity.
        """
        if course.enrollments.count() >= course.max_capacity:
            raise ValidationErrorDetail("Course has reached its maximum enrollment capacity.")
    
    @staticmethod
    def enrollment_deadline(course):
        """
        Validate if the enrollment deadline for the course has passed.
        """
        if course.enrollment_deadline and course.enrollment_deadline < timezone.now():
            raise ValidationErrorDetail("Enrollment deadline for the course has passed.")

class GradeValidator:
    @staticmethod
    def range(grade):
        """
        Validate if the grade falls within a specific range.
        """
        if not (0 <= grade <= 100):
            raise ValidationErrorDetail("Grade must be between 0 and 100.")

class AssignmentValidator:
    @staticmethod
    def submission(user, assignment):
        """
        Validate if the user has submitted the assignment.
        """
        if not assignment.submissions.filter(submitted_by=user).exists():
            raise ValidationErrorDetail("User has not submitted the assignment.")
    
    @staticmethod
    def deadline(assignment):
        """
        Validate if the assignment submission deadline has passed.
        """
        if assignment.deadline and assignment.deadline < timezone.now():
            raise ValidationErrorDetail("Assignment submission deadline has passed.")

class QuizValidator:
    @staticmethod
    def submission(user, quiz):
        """
        Validate if the user has submitted the quiz.
        """
        if not quiz.submissions.filter(submitted_by=user).exists():
            raise ValidationErrorDetail("User has not submitted the quiz.")
    
    @staticmethod
    def time_limit(quiz):
        """
        Validate if the time limit for the quiz has been exceeded.
        """
        if quiz.time_limit and quiz.time_limit < timezone.now() - quiz.start_time:
            raise ValidationErrorDetail("Time limit for the quiz has been exceeded.")



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
