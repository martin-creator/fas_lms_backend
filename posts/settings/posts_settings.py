from django.conf import settings


class PostsSettings:
    """
    PostsSettings: Manages app-specific settings for posts.
    """

    @staticmethod
    def get_posts_settings():
        """
        Get all posts settings.
        """
        return settings.POSTS_SETTINGS

    @staticmethod
    def update_posts_settings(posts_settings):
        """
        Update posts settings.
        """
        settings.POSTS_SETTINGS = posts_settings
