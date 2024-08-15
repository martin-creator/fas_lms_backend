from django.conf import settings

# GroupSettings: Manages app-specific settings for groups.
# Functions:
# get_group_settings, update_group_settings.


class GroupSettings:
    # get_group_settings: Get the group settings for the given group.
    # group: The group for which to get the settings.
    # Returns: The group settings for the given group.
    def get_group_settings(group):
        return group.group_settings

    # update_group_settings: Update the group settings for the given group.
    # group: The group for which to update the settings.
    # settings: The new settings to apply.
    def update_group_settings(group, settings):
        group.group_settings = settings
        group.save()
        return group.group_settings