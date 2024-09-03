from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from profiles.models import UserProfile, Follower, FollowRequest, Skill, Experience, Education, Endorsement, Achievement, Portfolio
from profiles.serializers import UserProfileSerializer, SkillSerializer, ExperienceSerializer, EducationSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from profiles.settings.profiles_settings import ProfilesSettings
from profiles.querying.profiles_query import ProfileQuery
from profiles.helpers.profiles_helpers import ProfileHelpers
from profiles.reports.profiles_report import ProfilesReport
from profiles.utils import UserUtils, DateTimeUtils



# class User(AbstractUser):
#     userId = ShortUUIDField()
#     profile_picture = models.ImageField(upload_to="users_images/", null=True, blank=True)
#     cover_photo = models.ImageField(upload_to="cover_photos/", null=True, blank=True)

#     def __str__(self):
#         return self.username

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', db_index=True)
#     bio = models.TextField(blank=True)
#     headline = models.CharField(max_length=255, blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     is_private = models.BooleanField(default=False)
#     joined_date = models.DateTimeField(default=timezone.now)
#     followers = models.ManyToManyField("self", through='Follower', related_name='following', symmetrical=False, db_index=True)
#     skills = models.ManyToManyField('Skill', related_name='users_skills', blank=True, db_index=True)
#     experiences = models.ManyToManyField('Experience', related_name='users_experiences', blank=True, db_index=True)
#     educations = models.ManyToManyField('Education', related_name='users_educations', blank=True, db_index=True)
#     endorsements = models.ManyToManyField('Endorsement', related_name='users_endorsements', blank=True, db_index=True)
#     job_applications = models.ManyToManyField('jobs.JobApplication', related_name='profile_job_applications', blank=True)
#     job_listings = models.ManyToManyField('jobs.JobListing', related_name='profile_job_listings', blank=True)
#     notifications = GenericRelation('notifications.Notification', related_name='profile_notifications')
#     followers = models.ManyToManyField(Follower, related_name='users_followers', blank=True)
#     follow_requests = models.ManyToManyField(FollowRequest, related_name='users_follow_requests', blank=True)
#     shares = GenericRelation('activity.Share', related_name='users_shares')
#     linkedin_id = models.CharField(max_length=255, blank=True, null=True)
#     linkedin_access_token = models.CharField(max_length=255, blank=True, null=True)
    
    
#     def __str__(self):
#         return self.user.username

# class Experience(models.Model):
#     user = models.ForeignKey(UserProfile, related_name='user_experiences', on_delete=models.CASCADE, db_index=True)
#     title = models.CharField(max_length=255)
#     company = models.ForeignKey('companies.Company', related_name='employees', on_delete=models.SET_NULL, null=True, db_index=True)
#     description = models.TextField(blank=True)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     is_current = models.BooleanField(default=False)
#     shares = GenericRelation('activity.Share', related_name='experience_shares')

#     def __str__(self):
#         return f'{self.title} at {self.company.name if self.company else "N/A"}'

# class Education(models.Model):
#     user = models.ForeignKey(UserProfile, related_name='user_educations', on_delete=models.CASCADE, db_index=True)
#     institution = models.CharField(max_length=255)
#     degree = models.CharField(max_length=255)
#     field_of_study = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     is_current = models.BooleanField(default=False)
#     shares = GenericRelation('activity.Share', related_name='education_shares')

#     def __str__(self):
#         return f'{self.degree} in {self.field_of_study} from {self.institution}'

# class Skill(models.Model):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(UserProfile, related_name='user_skills', db_index=True)
#     proficiency = models.CharField(max_length=50)
#     shares = models.ManyToManyField('activity.Share', related_name='skill_shares', blank=True)
#     endorsements = models.ManyToManyField('Endorsement', related_name='endorsement_skills', blank=True, db_index=True)
#     job_applications = models.ManyToManyField('jobs.JobApplication', related_name='skill_job_applications', blank=True)
#     job_listings = models.ManyToManyField('jobs.JobListing', related_name='skill_job_listings', blank=True)
#     notifications = GenericRelation('notifications.Notification', related_name='skill_notifications')
#     verified_from = models.ManyToManyField(UserProfile, related_name='skill_verified_from', blank=True)
#     verified_to = models.ManyToManyField(UserProfile, related_name='skill_verified_to', blank=True)

#     def __str__(self):
#         return self.name

# class Endorsement(models.Model):
#     skill = models.ForeignKey(Skill, related_name='skills_endorsements', on_delete=models.CASCADE, db_index=True)
#     endorsed_by = models.ForeignKey(UserProfile, related_name='given_endorsements', on_delete=models.CASCADE, db_index=True)
#     endorsed_user = models.ForeignKey(UserProfile, related_name='received_endorsements', on_delete=models.CASCADE, db_index=True)
#     shares = models.ManyToManyField('activity.Share', related_name='endorsement_shares', blank=True)

#     def __str__(self):
#         return f'{self.endorsed_by.user.username} endorsed {self.endorsed_user.user.username} for {self.skill.name}'
    
# class Achievement(models.Model):
#     user = models.ForeignKey(UserProfile, related_name='achievements', on_delete=models.CASCADE, db_index=True)
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     date_achieved = models.DateField()

#     def __str__(self):
#         return self.title
    
# class Portfolio(models.Model):
#     user = models.ForeignKey(UserProfile, related_name='portfolio', on_delete=models.CASCADE, db_index=True)
#     project_name = models.CharField(max_length=255)
#     description = models.TextField()
#     project_url = models.URLField()

#     def __str__(self):
#         return self.project_name


# CREATE PROFILE SERVICE CLASS WITH THE BASIC CRUD OPERATIONS
# THE PROFILE SERVICE CLASS SHOULD INCLUDE ALL THE CLASS METHODS ON THE USER PROFILE MODEL
# FEEL TO ADD ANY OTHER CLASS METHODS THAT YOU THINK WILL BE USEFUL TO THE PROFILE SERVICE


class ProfileService:
        
        @staticmethod
        def update_user_cover_and_profile_picture(user_id, data):
            """
            Update a user's cover and profile picture.
            """
            user = ProfileHelpers.process_user_data_update(user_id, data)
            user.save()

            serializer = UserProfileSerializer(user)

            return serializer.data
    
        @staticmethod
        def get_profiles():
            """
            Get all profiles.
            """
            profiles = ProfileQuery.get_profiles()
            return profiles
        
    
        @staticmethod
        def get_profile(profile_id):
            """
            Get a specific profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            return profile
        
    
        @staticmethod
        def create_profile(profile_data):
            """
            Create a new profile.
            """
    
            profile = ProfileHelpers.process_user_profile_data(profile_data)
            profile.save()
    
            serializer = UserProfileSerializer(profile)
    
            return serializer.data
        
    
        @staticmethod
        def update_profile(profile_id, profile_data):
            """
            Update a profile.
            """
    
            profile = ProfileQuery.get_user_profile(profile_id)
            profile = ProfileHelpers.process_user_profile_data_update(profile, profile_data)
            profile.save()
    
            serializer = UserProfileSerializer(profile)
    
            return serializer.data
        
    
        @staticmethod
        def delete_profile(profile_id):
            """
            Delete a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            profile.delete()
    
            return True
        
    
        @staticmethod
        def delete_all_profiles():
            """
            Delete all profiles.
            """
            profiles = ProfileQuery.get_profiles()
            profiles.delete()
    
            return True
    
        
    
        @staticmethod
        def follow_profile(profile_id):
            """
            Follow a profile.
            """
            profile = ProfileQuery.get_profile(profile_id)
            current_user = UserUtils.get_current_user()
    
            profile.follow(current_user)
    
            return True
        
    
        @staticmethod
        def unfollow_profile(profile_id):
            """
            Unfollow a profile.
            """
            profile = ProfileQuery.get_profile(profile_id)
            current_user = UserUtils.get_current_user()

            profile.unfollow(current_user)

            return True
        

        @staticmethod
        def accept_follow_request(profile_id):
            """
            Accept a follow request.
            """
            profile = ProfileQuery.get_profile(profile_id)
            current_user = UserUtils.get_current_user()

            profile.accept_follow_request(current_user)

            return True
        

        @staticmethod
        def reject_follow_request(profile_id):
            """
            Reject a follow request.
            """
            profile = ProfileQuery.get_profile(profile_id)
            current_user = UserUtils.get_current_user()

            profile.reject_follow_request(current_user)

            return True
        

        @staticmethod
        def endorse_skill(profile_id, skill_id):
            """
            Endorse a skill.
            """
            profile = ProfileQuery.get_profile(profile_id)
            skill = ProfileQuery.get_skill(skill_id)
            current_user = UserUtils.get_current_user()

            profile.endorse_skill(skill, current_user)

            return True
        

        @staticmethod
        def add_experience(profile_id, experience_data):
            """
            Add an experience.
            """
            profile = ProfileQuery.get_profile(profile_id)
            experience = ProfileQuery.process_experience_data(experience_data)
            experience.save()

            profile.experiences.add(experience)

            return True
        

        @staticmethod
        def add_education(profile_id, education_data):

            """
            Add an education.
            """
            profile = ProfileQuery.get_profile(profile_id)
            education = ProfileQuery.process_education_data(education_data)
            education.save()

            profile.educations.add(education)

            return True
        

        @staticmethod
        def add_skill(profile_id, skill_data):
            """
            Add a skill.
            """
            profile = ProfileQuery.get_profile(profile_id)
            skill = ProfileQuery.process_skill_data(skill_data)
            skill.save()

            profile.skills.add(skill)

            return True
        

        @staticmethod
        def add_achievement(profile_id, achievement_data):
            """
            Add an achievement.
            """
            profile = ProfileQuery.get_profile(profile_id)
            achievement = ProfileQuery.process_achievement_data(achievement_data)
            achievement.save()

            profile.achievements.add(achievement)

            return True
        

        @staticmethod
        def add_portfolio(profile_id, portfolio_data):
            """
            Add a portfolio.
            """
            profile = ProfileQuery.get_profile(profile_id)
            portfolio = ProfileQuery.process_portfolio_data(portfolio_data)
            portfolio.save()

            profile.portfolios.add(portfolio)

            return True


        @staticmethod
        def get_followers(profile_id):
            """
            Get all followers for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            followers = profile.followers.all()
            serializer = UserProfileSerializer(followers, many=True)
            return serializer.data
        

        #  CRUD for Experience apart from Create
        @staticmethod
        def get_experiences(profile_id):
            """
            Get all experiences for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            experiences = profile.experiences.all()
            serializer = ExperienceSerializer(experiences, many=True)
            return serializer.data
        

        @staticmethod
        def get_experience(profile_id, experience_id):
            """
            Get a specific experience for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            experience = profile.experiences.get(id=experience_id)
            serializer = ExperienceSerializer(experience)
            return serializer.data
        

        @staticmethod
        def update_experience(profile_id, experience_id, experience_data):
            """
            Update an experience for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            experience = profile.experiences.get(id=experience_id)
            experience = ProfileHelpers.process_experience_data_update(experience, experience_data)
            experience.save()

            serializer = ExperienceSerializer(experience)

            return serializer.data
        

        @staticmethod
        def delete_experience(profile_id, experience_id):
            """
            Delete an experience for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            experience = profile.experiences.get(id=experience_id)
            experience.delete()

            return True
        

        @staticmethod
        def delete_all_experiences(profile_id):
            """
            Delete all experiences for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            experiences = profile.experiences.all()
            experiences.delete()

            return True
        


        # CRUD for Education apart from Create
        @staticmethod
        def get_educations(profile_id):
            """
            Get all educations for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            educations = profile.educations.all()
            serializer = EducationSerializer(educations, many=True)
            return serializer.data
        

        @staticmethod
        def get_education(profile_id, education_id):
            """
            Get a specific education for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            education = profile.educations.get(id=education_id)
            serializer = EducationSerializer(education)
            return serializer.data
        

        @staticmethod
        def update_education(profile_id, education_id, education_data):
            """
            Update an education for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            education = profile.educations.get(id=education_id)
            education = ProfileHelpers.process_education_data_update(education, education_data)
            education.save()

            serializer = EducationSerializer(education)

            return serializer.data
        

        @staticmethod
        def delete_education(profile_id, education_id):
            """
            Delete an education for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            education = profile.educations.get(id=education_id)
            education.delete()

            return True
        

        @staticmethod
        def delete_all_educations(profile_id):
            """
            Delete all educations for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            educations = profile.educations.all()
            educations.delete()

            return True
        

        # CRUD for Skill apart from Create
        @staticmethod
        def get_skills(profile_id):
            """
            Get all skills for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            skills = profile.skills.all()
            serializer = SkillSerializer(skills, many=True)
            return serializer.data
        

        @staticmethod
        def get_skill(profile_id, skill_id):
            """
            Get a specific skill for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            skill = profile.skills.get(id=skill_id)
            serializer = SkillSerializer(skill)
            return serializer.data
        

        @staticmethod
        def update_skill(profile_id, skill_id, skill_data):
            """
            Update a skill for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            skill = profile.skills.get(id=skill_id)
            skill = ProfileHelpers.process_skill_data_update(skill, skill_data)
            skill.save()

            serializer = SkillSerializer(skill)

            return serializer.data
        


        @staticmethod
        def delete_skill(profile_id, skill_id):
            """
            Delete a skill for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            skill = profile.skills.get(id=skill_id)
            skill.delete()

            return True
        

        @staticmethod
        def delete_all_skills(profile_id):
            """
            Delete all skills for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            skills = profile.skills.all()
            skills.delete()

            return True
        


        # CRUD for Achievement apart from Create
        @staticmethod
        def get_achievements(profile_id):
            """
            Get all achievements for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            achievements = profile.achievements.all()
            serializer = AchievementSerializer(achievements, many=True)
            return serializer.data
        

        @staticmethod
        def get_achievement(profile_id, achievement_id):
            """
            Get a specific achievement for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            achievement = profile.achievements.get(id=achievement_id)
            serializer = AchievementSerializer(achievement)
            return serializer.data
        

        @staticmethod
        def update_achievement(profile_id, achievement_id, achievement_data):
            """
            Update an achievement for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            achievement = profile.achievements.get(id=achievement_id)
            achievement = ProfileHelpers.process_achievement_data_update(achievement, achievement_data)
            achievement.save()

            serializer = AchievementSerializer(achievement)

            return serializer.data
        

        @staticmethod
        def delete_achievement(profile_id, achievement_id):
            """
            Delete an achievement for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            achievement = profile.achievements.get(id=achievement_id)
            achievement.delete()

            return True
        


        @staticmethod
        def delete_all_achievements(profile_id):
            """
            Delete all achievements for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            achievements = profile.achievements.all()
            achievements.delete()

            return True


        # CRUD for Portfolio apart from Create
        @staticmethod
        def get_portfolios(profile_id):
            """
            Get all portfolios for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            portfolios = profile.portfolios.all()
            serializer = PortfolioSerializer(portfolios, many=True)
            return serializer.data
        

        @staticmethod
        def get_portfolio(profile_id, portfolio_id):
            """
            Get a specific portfolio for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            portfolio = profile.portfolios.get(id=portfolio_id)
            serializer = PortfolioSerializer(portfolio)
            return serializer.data
        

        @staticmethod
        def update_portfolio(profile_id, portfolio_id, portfolio_data):
            """
            Update a portfolio for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            portfolio = profile.portfolios.get(id=portfolio_id)
            portfolio = ProfileHelpers.process_portfolio_data_update(portfolio, portfolio_data)
            portfolio.save()

            serializer = PortfolioSerializer(portfolio)

            return serializer.data
        


        @staticmethod
        def delete_portfolio(profile_id, portfolio_id):
            """
            Delete a portfolio for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            portfolio = profile.portfolios.get(id=portfolio_id)
            portfolio.delete()

            return True
        

        @staticmethod
        def delete_all_portfolios(profile_id):
            """
            Delete all portfolios for a profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            portfolios = profile.portfolios.all()
            portfolios.delete()

            return True
        


        @staticmethod
        def get_profile_report(profile_id):
            """
            Get a report for a specific profile.
            """
            profile = ProfileQuery.get_user_profile(profile_id)
            report = ProfilesReport.get_user_report(profile)

            return report
        




