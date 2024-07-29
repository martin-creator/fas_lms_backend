from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
# from jobs.models import JobApplication, JobListing
from followers.models import Follower, FollowRequest, FollowNotification
# from notifications.models import Notification
from shortuuidfield import ShortUUIDField
# from messaging.models import Reaction, Share
from profiles.actions.profile_actions import ProfileActions
from profiles.utils.permissions import ProfilePermissionChecker

class User(AbstractUser):
    userId = ShortUUIDField()
    profile_picture = models.ImageField(upload_to="users_images/", null=True, blank=True)
    cover_photo = models.ImageField(upload_to="cover_photos/", null=True, blank=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_index=True)
    bio = models.TextField(blank=True)
    headline = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_private = models.BooleanField(default=False)
    joined_date = models.DateTimeField(default=timezone.now)
    followers = models.ManyToManyField("self", through='Follower', related_name='following', symmetrical=False, db_index=True)
    skills = models.ManyToManyField('Skill', related_name='users_skills', blank=True, db_index=True)
    experiences = models.ManyToManyField('Experience', related_name='users_experiences', blank=True, db_index=True)
    educations = models.ManyToManyField('Education', related_name='users_educations', blank=True, db_index=True)
    endorsements = models.ManyToManyField('Endorsement', related_name='users_endorsements', blank=True, db_index=True)
    job_applications = models.ManyToManyField('jobs.JobApplication', related_name='profile_job_applications', blank=True)
    job_listings = models.ManyToManyField('jobs.JobListing', related_name='profile_job_listings', blank=True)
    notifications = models.ManyToManyField('notifications.Notification', related_name='profile_notifications', blank=True)
    followers = models.ManyToManyField(Follower, related_name='users_followers', blank=True)
    follow_requests = models.ManyToManyField(FollowRequest, related_name='users_follow_requests', blank=True)
    shares = models.ManyToManyField('activity.Share', related_name='users_shares', blank=True)
    
    
    def __str__(self):
        return self.user.username

    def perform_action(self, user, action, *args, **kwargs):
        """
        Perform an action on the UserProfile instance with permission checks.

        Args:
            user (User): The user performing the action.
            action (str): The action to perform (e.g., 'follow', 'unfollow', 'endorse_skill').
            *args: Additional arguments for the action.
            **kwargs: Additional keyword arguments for the action.

        Raises:
            PermissionDenied: If the user does not have permission for the action.
            ValueError: If the action is unknown.
        """
        ProfilePermissionChecker.check_permission_for_action(user, action)

        action_methods = {
            'follow': ProfileActions.follow_profile,
            'unfollow': ProfileActions.unfollow_profile,
            'is_following': ProfileActions.is_following,
            'has_follow_request': ProfileActions.has_follow_request,
            'accept_follow_request': ProfileActions.accept_follow_request,
            'reject_follow_request': ProfileActions.reject_follow_request,
            'endorse_skill': ProfileActions.endorse_skill,
            'has_endorsed': ProfileActions.has_endorsed,
            'add_experience': ProfileActions.add_experience,
            'remove_experience': ProfileActions.remove_experience,
            'add_education': ProfileActions.add_education,
            'remove_education': ProfileActions.remove_education,
        }

        action_method = action_methods.get(action)
        if action_method:
            return action_method(user, self, *args, **kwargs)
        else:
            raise ValueError(f"Unknown action: {action}")

    # Existing methods can be updated to use perform_action
    def follow(self, profile):
        return self.perform_action(self.user, 'follow', profile)

    def unfollow(self, profile):
        return self.perform_action(self.user, 'unfollow', profile)

    def is_following(self, profile):
        return self.perform_action(self.user, 'is_following', profile)

    def has_follow_request(self, profile):
        return self.perform_action(self.user, 'has_follow_request', profile)

    def accept_follow_request(self, profile):
        return self.perform_action(self.user, 'accept_follow_request', profile)

    def reject_follow_request(self, profile):
        return self.perform_action(self.user, 'reject_follow_request', profile)

    def endorse_skill(self, skill, endorsed_by):
        return self.perform_action(self.user, 'endorse_skill', skill, endorsed_by)

    def has_endorsed(self, skill):
        return self.perform_action(self.user, 'has_endorsed', skill)

    def add_experience(self, title, company, description, start_date, end_date=None, is_current=False):
        return self.perform_action(self.user, 'add_experience', title, company, description, start_date, end_date, is_current)

    def remove_experience(self, experience_id):
        return self.perform_action(self.user, 'remove_experience', experience_id)

    def add_education(self, institution, degree, field_of_study, start_date, end_date=None, is_current=False):
        return self.perform_action(self.user, 'add_education', institution, degree, field_of_study, start_date, end_date, is_current)

    def remove_education(self, education_id):
        return self.perform_action(self.user, 'remove_education', education_id)
        
class Experience(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user_experiences', on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=255)
    company = models.ForeignKey('companies.Company', related_name='employees', on_delete=models.SET_NULL, null=True, db_index=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    shares = models.ManyToManyField('activity.Share', related_name='experience_shares', blank=True)

    def __str__(self):
        return f'{self.title} at {self.company.name if self.company else "N/A"}'

class Education(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user_educations', on_delete=models.CASCADE, db_index=True)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    shares = models.ManyToManyField('activity.Share', related_name='education_shares', blank=True)

    def __str__(self):
        return f'{self.degree} in {self.field_of_study} from {self.institution}'

class Skill(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(UserProfile, related_name='user_skills', db_index=True)
    proficiency = models.CharField(max_length=50)
    shares = models.ManyToManyField('activity.Share', related_name='skill_shares', blank=True)
    endorsements = models.ManyToManyField('Endorsement', related_name='endorsement_skills', blank=True, db_index=True)
    job_applications = models.ManyToManyField('jobs.JobApplication', related_name='skill_job_applications', blank=True)
    job_listings = models.ManyToManyField('jobs.JobListing', related_name='skill_job_listings', blank=True)
    notifications = models.ManyToManyField('notifications.Notification', related_name='skill_notifications', blank=True)
    verified_from = models.ManyToManyField(UserProfile, related_name='skill_verified_from', blank=True)
    verified_to = models.ManyToManyField(UserProfile, related_name='skill_verified_to', blank=True)

    def __str__(self):
        return self.name

class Endorsement(models.Model):
    skill = models.ForeignKey(Skill, related_name='skills_endorsements', on_delete=models.CASCADE, db_index=True)
    endorsed_by = models.ForeignKey(UserProfile, related_name='given_endorsements', on_delete=models.CASCADE, db_index=True)
    endorsed_user = models.ForeignKey(UserProfile, related_name='received_endorsements', on_delete=models.CASCADE, db_index=True)
    shares = models.ManyToManyField('activity.Share', related_name='endorsement_shares', blank=True)

    def __str__(self):
        return f'{self.endorsed_by.user.username} endorsed {self.endorsed_user.user.username} for {self.skill.name}'
    
class Achievement(models.Model):
    user = models.ForeignKey(UserProfile, related_name='achievements', on_delete=models.CASCADE, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_achieved = models.DateField()

    def __str__(self):
        return self.title
    
class Portfolio(models.Model):
    user = models.ForeignKey(UserProfile, related_name='portfolio', on_delete=models.CASCADE, db_index=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    project_url = models.URLField()

    def __str__(self):
        return self.project_name