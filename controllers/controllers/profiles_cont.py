from django.db.models import Count
from profiles.models import UserProfile, Experience, Education, Skill, Endorsement, Achievement, Portfolio
from followers.models import Follower, FollowRequest
from activity.models import Share
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import datetime

class ProfileManagementController:
    def __init__(self):
        pass

    def create_user_profile(self, user, bio='', headline='', location='', is_private=False):
        """
        Creates a new user profile.
        """
        profile = UserProfile.objects.create(
            user=user,
            bio=bio,
            headline=headline,
            location=location,
            is_private=is_private
        )
        return profile

    def update_user_profile(self, user_profile_id, bio=None, headline=None, location=None, is_private=None):
        """
        Updates an existing user profile.
        """
        profile = UserProfile.objects.get(id=user_profile_id)
        if bio is not None:
            profile.bio = bio
        if headline is not None:
            profile.headline = headline
        if location is not None:
            profile.location = location
        if is_private is not None:
            profile.is_private = is_private
        profile.save()
        return profile

    def get_user_profile(self, user):
        """
        Retrieves a user's profile.
        """
        return UserProfile.objects.filter(user=user).first()

    def get_user_profile_by_id(self, profile_id):
        """
        Retrieves a user's profile by profile ID.
        """
        return get_object_or_404(UserProfile, id=profile_id)

    def follow_profile(self, user_profile, follower):
        """
        Allows a user to follow another profile.
        """
        if not user_profile.is_following(follower):
            user_profile.follow(follower)

    def unfollow_profile(self, user_profile, follower):
        """
        Allows a user to unfollow another profile.
        """
        user_profile.unfollow(follower)

    def accept_follow_request(self, user_profile, follower):
        """
        Accepts a follow request from another profile.
        """
        user_profile.accept_follow_request(follower)

    def reject_follow_request(self, user_profile, follower):
        """
        Rejects a follow request from another profile.
        """
        user_profile.reject_follow_request(follower)

    def endorse_skill(self, user_profile, skill, endorsed_by):
        """
        Endorses a skill on a user's profile.
        """
        user_profile.endorse_skill(skill, endorsed_by)

    def add_experience(self, user_profile, title, company, description, start_date, end_date=None, is_current=False):
        """
        Adds an experience to a user's profile.
        """
        return Experience.objects.create(
            user=user_profile,
            title=title,
            company=company,
            description=description,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )

    def add_education(self, user_profile, institution, degree, field_of_study, start_date, end_date=None, is_current=False):
        """
        Adds an education to a user's profile.
        """
        return Education.objects.create(
            user=user_profile,
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            is_current=is_current
        )

    def add_achievement(self, user_profile, title, description, date_achieved):
        """
        Adds an achievement to a user's profile.
        """
        return Achievement.objects.create(
            user=user_profile,
            title=title,
            description=description,
            date_achieved=date_achieved
        )

    def add_portfolio_project(self, user_profile, project_name, description, project_url):
        """
        Adds a portfolio project to a user's profile.
        """
        return Portfolio.objects.create(
            user=user_profile,
            project_name=project_name,
            description=description,
            project_url=project_url
        )

    def get_followers(self, user_profile):
        """
        Retrieves followers of a user's profile.
        """
        return user_profile.followers.all()

    def get_following(self, user_profile):
        """
        Retrieves profiles followed by a user.
        """
        return user_profile.following.all()

    def get_endorsements(self, user_profile):
        """
        Retrieves endorsements received by a user.
        """
        return user_profile.endorsements.all()

    def get_skills(self, user_profile):
        """
        Retrieves skills listed on a user's profile.
        """
        return user_profile.skills.all()

    def get_experiences(self, user_profile):
        """
        Retrieves experiences listed on a user's profile.
        """
        return user_profile.experiences.all()

    def get_educations(self, user_profile):
        """
        Retrieves educations listed on a user's profile.
        """
        return user_profile.educations.all()

    def get_achievements(self, user_profile):
        """
        Retrieves achievements listed on a user's profile.
        """
        return user_profile.achievements.all()

    def get_portfolio_projects(self, user_profile):
        """
        Retrieves portfolio projects listed on a user's profile.
        """
        return user_profile.portfolio.all()

    def is_following(self, user_profile, follower):
        """
        Checks if a profile is followed by another profile.
        """
        return user_profile.is_following(follower)

    def has_follow_request(self, user_profile, follower):
        """
        Checks if a profile has a follow request from another profile.
        """
        return user_profile.has_follow_request(follower)

    def has_endorsed(self, user_profile, skill):
        """
        Checks if a profile has endorsed a skill.
        """
        return user_profile.has_endorsed(skill)
