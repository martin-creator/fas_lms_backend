# utils/permissions.py
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .logging import log_data_access
from .models import Course, Assignment, Module
from querying.models import QueryExecutionPermission
from rest_framework import permissions

User = get_user_model()

class IsEnrolledInCourse(permissions.BasePermission):
    """
    Custom permission to check if the user is enrolled in the course.
    """

    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()

class IsInstructorOfCourse(permissions.BasePermission):
    """
    Custom permission to check if the user is the instructor of the course.
    """

    def has_object_permission(self, request, view, obj):
        return obj.instructor == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to edit objects.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsCourseInstructorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only course instructors to edit course details.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.instructor == request.user

class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only course owners to edit course details.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsStudentEnrolledInCourse(permissions.BasePermission):
    """
    Custom permission to check if the student is enrolled in the course.
    """

    def has_permission(self, request, view):
        course_id = view.kwargs.get('course_id')
        return request.user.enrolled_courses.filter(id=course_id).exists()

def check_user_is_admin(user):
    """
    Check if the user is an admin.

    Args:
    - user: User instance.

    Raises:
    - PermissionDenied: If the user is not an admin.
    """
    if not user.is_staff:
        log_data_access(user=user, query="Attempted admin action without admin rights.")
        raise PermissionDenied("Admin access required.")

def check_user_has_permission(user, required_permission):
    """
    Check if the user has a specific permission.

    Args:
    - user: User instance.
    - required_permission: Required permission string.

    Raises:
    - PermissionDenied: If the user does not have the required permission.
    """
    if not user.has_perm(required_permission):
        log_data_access(user=user, query=f"Attempted action without permission: {required_permission}")
        raise PermissionDenied(f"Required permission: {required_permission}.")

def check_user_can_access_course(user, course_id):
    """
    Check if the user can access a specific course.

    Args:
    - user: User instance.
    - course_id: ID of the course.

    Raises:
    - PermissionDenied: If the user cannot access the course.
    """
    course = get_object_or_404(Course, id=course_id)
    if not user.is_authenticated or not user.has_perm('view_course', course):
        log_data_access(user=user, query=f"Attempted to access course '{course.title}' without permission.")
        raise PermissionDenied("You do not have permission to access this course.")

    log_data_access(user=user, query=f"Accessed course '{course.title}'.")

def check_user_can_manage_module(user, module_id):
    """
    Check if the user can manage a specific module.

    Args:
    - user: User instance.
    - module_id: ID of the module.

    Raises:
    - PermissionDenied: If the user cannot manage the module.
    """
    module = get_object_or_404(Module, id=module_id)
    if not user.is_authenticated or not user.has_perm('manage_module', module):
        log_data_access(user=user, query=f"Attempted to manage module '{module.title}' without permission.")
        raise PermissionDenied("You do not have permission to manage this module.")

    log_data_access(user=user, query=f"Managed module '{module.title}'.")

def check_user_can_modify_assignment(user, assignment_id):
    """
    Check if the user can modify a specific assignment.

    Args:
    - user: User instance.
    - assignment_id: ID of the assignment.

    Raises:
    - PermissionDenied: If the user cannot modify the assignment.
    """
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if not user.is_authenticated or not user.has_perm('modify_assignment', assignment):
        log_data_access(user=user, query=f"Attempted to modify assignment '{assignment.title}' without permission.")
        raise PermissionDenied("You do not have permission to modify this assignment.")

    log_data_access(user=user, query=f"Modified assignment '{assignment.title}'.")

def check_query_execution_permission(query, user):
    """
    Check if the user has permission to execute the query.

    Args:
    - query: Query object from querying.models.QueryExecutionPermission.
    - user: User object from Django's custom user model.

    Returns:
    - Boolean indicating whether the user has permission to execute the query.
    """
    try:
        permission = QueryExecutionPermission.objects.get(query=query)
        has_permission = user.profile.followers.filter(id__in=permission.allowed_groups.all()).exists() or permission.allowed_users.filter(id=user.id).exists()
        if not has_permission:
            log_data_access(user=user, query=f"Attempted to execute query '{query}' without permission.")
        return has_permission
    except QueryExecutionPermission.DoesNotExist:
        log_data_access(user=user, query=f"Attempted to execute non-existent query '{query}'.")
        return False

# Additional Permission Functions can be added here for specific use cases