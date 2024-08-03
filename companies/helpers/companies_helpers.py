from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from companies.models import Company, CompanyUpdate
# from profiles.models import UserProfile
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta

User = get_user_model()


# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     website = models.URLField(blank=True)
#     location = models.CharField(max_length=255, blank=True)
#     industry = models.CharField(max_length=255, blank=True)
#     description = models.TextField(blank=True)
#     attachments = GenericRelation(Attachment)
#     categories = models.ManyToManyField(Category, related_name='companies_categories')
#     logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
#     founded_date = models.DateField(null=True, blank=True)
#     employee_count = models.IntegerField(default=0)
#     revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
#     members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='member_companies')
#     followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_companies')
#     services = models.TextField(blank=True)  # New field for listing services provided by the company

#     def __str__(self):
#         return self.name
    
    
# class CompanyUpdate(models.Model):
#     company = models.ForeignKey(Company, related_name='company_updates', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     attachments = GenericRelation(Attachment)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.company.name} Update: {self.title}"



class CompanyHelpers:

    @staticmethod
    def process_company_data(data):
        """
        Process company data before saving it to the database.
        """
        name = data.get('name')
        website = data.get('website')
        location = data.get('location')
        industry = data.get('industry')
        description = data.get('description')
        founded_date = data.get('founded_date')
        employee_count = data.get('employee_count')
        revenue = data.get('revenue')
        services = data.get('services')
        logo = data.get('logo')
        categories = data.get('categories')
        members = data.get('members')
        followers = data.get('followers')

        company = Company(
            name=name,
            website=website,
            location=location,
            industry=industry,
            description=description,
            founded_date=founded_date,
            employee_count=employee_count,
            revenue=revenue,
            services=services,
            logo=logo
        )

        return company, categories, members, followers
    

    @staticmethod
    def process_company_data_update(company_id, data):
        """
        Process company data before updating it in the database.
        """
        
        company = Company.objects.get(id=company_id)
        
        name = data.get('name')
        website = data.get('website')
        location = data.get('location')
        industry = data.get('industry')
        description = data.get('description')
        founded_date = data.get('founded_date')
        employee_count = data.get('employee_count')
        revenue = data.get('revenue')
        services = data.get('services')
        logo = data.get('logo')
        categories = data.get('categories')
        members = data.get('members')
        followers = data.get('followers')

        if name is not None:
            company.name = name

        if website is not None:
            company.website = website

        if location is not None:
            company.location = location

        if industry is not None:
            company.industry = industry

        if description is not None:
            company.description = description

        if founded_date is not None:
            company.founded_date = founded_date

        if employee_count is not None:
            company.employee_count = employee_count

        if revenue is not None:
            company.revenue = revenue

        if services is not None:
            company.services = services

        if logo is not None:
            company.logo = logo

        if categories is not None:
            company.categories.set(categories)

        if members is not None:
            company.members.set(members)

        if followers is not None:
            company.followers.set(followers)

        return company, categories, members, followers
    
    


    @staticmethod
    def process_company_update_data(data):
        """
        Process company update data before saving it to the database.
        """
        title = data.get('title')
        content = data.get('content')
        attachments = data.get('attachments')
        company_id = data.get('company_id')

        if not company_id:
            raise ValidationError('Company ID is required.')
        
        company = Company.objects.filter(id=company_id)

        company_update = CompanyUpdate(
            title=title,
            content=content,
            attachments=attachments,
            company=company
        )

        return company_update









