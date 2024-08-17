from django.conf import settings

# CourseSettings: Manages app-specific settings for courses.
# Functions:
# get_course_settings, update_course_settings.

class CourseSettings:
    """
    CourseSettings: Manages app-specific settings for courses.
    """

    @staticmethod
    def get_course_settings():
        """
        Get all course settings.
        """
        return settings.COURSE_SETTINGS

    @staticmethod
    def update_course_settings(course_settings):
        """
        Update course settings.
        """
        settings.COURSE_SETTINGS = course_settings