# notifications/services/role_service.py
from django.contrib.auth.models import Group, Permission

def create_roles_and_permissions():
    manager_group, created = Group.objects.get_or_create(name='Notification Manager')
    view_permission = Permission.objects.get(codename='can_view_notifications')
    manage_permission = Permission.objects.get(codename='can_manage_notifications')
    manager_group.permissions.add(view_permission, manage_permission)