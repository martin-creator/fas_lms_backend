from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import UserProfile, User, Experience, Education, Skill, Endorsement, Achievement, Portfolio
from profiles.serializers import UserProfileSerializer, UserSerializer, ExperienceSerializer, EducationSerializer, SkillSerializer, EndorsementSerializer, AchievementSerializer, PortfolioSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


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



class ProfileHelpers:
    @staticmethod
    def process_user_data(data):
        # add only profile and cover photo
        profile_picture = data.get('profile_picture')
        cover_photo = data.get('cover_photo')
        user = User(profile_picture=profile_picture, cover_photo=cover_photo)
        return user
    
    @staticmethod
    def process_user_data_update(user_id, data):
        user = User.objects.get(id=user_id)
        profile_picture = data.get('profile_picture')
        cover_photo = data.get('cover_photo')
        if profile_picture is not None:
            user.profile_picture = profile_picture
        if cover_photo is not None:
            user.cover_photo = cover_photo
        return user
    
    @staticmethod
    def process_user_profile_data(data):
        bio = data.get('bio')
        headline = data.get('headline')
        location = data.get('location')
        is_private = data.get('is_private')

        user_profile = UserProfile(bio=bio, headline=headline, location=location, is_private=is_private)
        return user_profile
    

    @staticmethod
    def process_user_profile_data_update(user_id, data):
        user_profile = UserProfile.objects.get(id=user_id)
        bio = data.get('bio')
        headline = data.get('headline')
        location = data.get('location')
        is_private = data.get('is_private')

        if bio is not None:
            user_profile.bio = bio
        if headline is not None:
            user_profile.headline = headline
        if location is not None:
            user_profile.location = location
        if is_private is not None:
            user_profile.is_private = is_private

        return user_profile
    

    @staticmethod
    def process_experience_data(data):
        title = data.get('title')
        company = data.get('company')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        experience = Experience(title=title, company=company, description=description, start_date=start_date, end_date=end_date, is_current=is_current)
        return experience
    

    @staticmethod
    def process_experience_data_update(experience_id, data):
        experience = Experience.objects.get(id=experience_id)
        title = data.get('title')
        company = data.get('company')
        description = data.get('description')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        if title is not None:
            experience.title = title
        if company is not None:
            experience.company = company
        if description is not None:
            experience.description = description
        if start_date is not None:
            experience.start_date = start_date
        if end_date is not None:
            experience.end_date = end_date
        if is_current is not None:
            experience.is_current = is_current

        return experience
    

    @staticmethod
    def process_education_data(data):
        institution = data.get('institution')
        degree = data.get('degree')
        field_of_study = data.get('field_of_study')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        education = Education(institution=institution, degree=degree, field_of_study=field_of_study, start_date=start_date, end_date=end_date, is_current=is_current)
        return education
    

    @staticmethod
    def process_education_data_update(education_id, data):
        education = Education.objects.get(id=education_id)
        institution = data.get('institution')
        degree = data.get('degree')
        field_of_study = data.get('field_of_study')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_current = data.get('is_current')

        if institution is not None:
            education.institution = institution
        if degree is not None:
            education.degree = degree
        if field_of_study is not None:
            education.field_of_study = field_of_study
        if start_date is not None:
            education.start_date = start_date
        if end_date is not None:
            education.end_date = end_date
        if is_current is not None:
            education.is_current = is_current

        return education
    

    @staticmethod
    def process_skill_data(data):
        name = data.get('name')
        proficiency = data.get('proficiency')

        skill = Skill(name=name, proficiency=proficiency)
        return skill
    

    @staticmethod
    def process_skill_data_update(skill_id, data):
        skill = Skill.objects.get(id=skill_id)
        name = data.get('name')
        proficiency = data.get('proficiency')

        if name is not None:
            skill.name = name
        if proficiency is not None:
            skill.proficiency = proficiency

        return skill
    

    @staticmethod
    def process_endorsement_data(data):
        skill = data.get('skill')
        endorsed_by = data.get('endorsed_by')
        endorsed_user = data.get('endorsed_user')

        endorsement = Endorsement(skill=skill, endorsed_by=endorsed_by, endorsed_user=endorsed_user)
        return endorsement
    

    @staticmethod
    def process_endorsement_data_update(endorsement_id, data):
        endorsement = Endorsement.objects.get(id=endorsement_id)
        skill = data.get('skill')
        endorsed_by = data.get('endorsed_by')
        endorsed_user = data.get('endorsed_user')

        if skill is not None:
            endorsement.skill = skill
        if endorsed_by is not None:
            endorsement.endorsed_by = endorsed_by
        if endorsed_user is not None:
            endorsement.endorsed_user = endorsed_user

        return endorsement
    

    @staticmethod
    def process_achievement_data(data):
        title = data.get('title')
        description = data.get('description')
        date_achieved = data.get('date_achieved')

        achievement = Achievement(title=title, description=description, date_achieved=date_achieved)
        return achievement
    

    @staticmethod
    def process_achievement_data_update(achievement_id, data):
        achievement = Achievement.objects.get(id=achievement_id)
        title = data.get('title')
        description = data.get('description')
        date_achieved = data.get('date_achieved')

        if title is not None:
            achievement.title = title
        if description is not None:
            achievement.description = description
        if date_achieved is not None:
            achievement.date_achieved = date_achieved

        return achievement
    

    @staticmethod
    def process_portfolio_data(data):
        project_name = data.get('project_name')
        description = data.get('description')
        project_url = data.get('project_url')

        portfolio = Portfolio(project_name=project_name, description=description, project_url=project_url)
        return portfolio
    

    @staticmethod
    def process_portfolio_data_update(portfolio_id, data):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        project_name = data.get('project_name')
        description = data.get('description')
        project_url = data.get('project_url')

        if project_name is not None:
            portfolio.project_name = project_name
        if description is not None:
            portfolio.description = description
        if project_url is not None:
            portfolio.project_url = project_url

        return portfolio
    

