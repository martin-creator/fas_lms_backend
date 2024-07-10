from groups.models import Group, GroupMembership
from django.conf import settings


class GroupManagementController:
    def __init__(self):
        pass

    def create_group(self, name, description, creator, group_type='public', privacy_level='medium', categories=None, tags=None):
        group = Group(
            name=name,
            description=description,
            creator=creator,
            group_type=group_type,
            privacy_level=privacy_level,
        )
        group.save()
        if categories:
            group.categories.set(categories)
        if tags:
            group.tags.set(*tags)
        return group

    def update_group(self, group_id, **kwargs):
        group = Group.objects.get(id=group_id)
        for key, value in kwargs.items():
            setattr(group, key, value)
        group.save()
        return group

    def add_member_to_group(self, user, group, role='member'):
        membership, created = GroupMembership.objects.get_or_create(user=user, group=group, defaults={'role': role})
        return membership

    def remove_member_from_group(self, user, group):
        try:
            membership = GroupMembership.objects.get(user=user, group=group)
            membership.delete()
            return True
        except GroupMembership.DoesNotExist:
            return False

    def get_group_members(self, group_id):
        group = Group.objects.get(id=group_id)
        return group.members.all()

    def get_user_groups(self, user_id):
        user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
        return user.user_groups.all()
