from django.conf import settings
from companies.models import Company, CompanyUpdate


class CompanyProfilesController:
    def __init__(self):
        pass

    def create_company_profile(self, name, website="", location="", industry="", description="", founded_date=None, employee_count=0, revenue=None):
        company = Company(
            name=name,
            website=website,
            location=location,
            industry=industry,
            description=description,
            founded_date=founded_date,
            employee_count=employee_count,
            revenue=revenue,
        )
        company.save()
        return company

    def update_company_profile(self, company_id, **kwargs):
        company = Company.objects.get(id=company_id)
        for key, value in kwargs.items():
            setattr(company, key, value)
        company.save()
        return company

    def get_company_profile(self, company_id):
        return Company.objects.get(id=company_id)

    def get_company_updates(self, company_id):
        return CompanyUpdate.objects.filter(company_id=company_id).order_by('-created_at')

    def get_company_followers(self, company_id):
        company = Company.objects.get(id=company_id)
        return company.followers.all()

    def get_company_members(self, company_id):
        company = Company.objects.get(id=company_id)
        return company.members.all()
