from django.db.models import Count, Q
from companies.models import Company, CompanyUpdate
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from django.utils import timezone


class CompanyQuery:
    @staticmethod
    def get_companies():
        """
        Get all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data

    @staticmethod
    def get_company(company_id):
        """
        Get a specific company.
        """
        company = Company.objects.get(id=company_id)
        serializer = CompanySerializer(company)
        return serializer.data

    @staticmethod
    def get_company_updates(company_id):
        """
        Get all updates for a specific company.
        """
        updates = CompanyUpdate.objects.filter(company_id=company_id)
        serializer = CompanyUpdateSerializer(updates, many=True)
        return serializer.data

    @staticmethod
    def get_companies_by_owner(owner_id):
        """
        Get all companies owned by a specific owner.
        """
        companies = Company.objects.filter(owner_id=owner_id)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data

    @staticmethod
    def get_companies_by_employee(employee_id):
        """
        Get all companies where a specific employee works.
        """
        companies = Company.objects.filter(employees=employee_id)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_location(location):
        """
        Get all companies in a specific location.
        """
        companies = Company.objects.filter(location=location)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_industry(industry):
        """
        Get all companies in a specific industry.
        """
        companies = Company.objects.filter(industry=industry)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_size(size):
        """
        Get all companies of a specific size.
        """
        companies = Company.objects.filter(size=size)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_founded(founded):
        """
        Get all companies founded in a specific year.
        """
        companies = Company.objects.filter(founded=founded)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_funding(funding):
        """
        Get all companies that have received a specific amount of funding.
        """
        companies = Company.objects.filter(funding=funding)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_by_status(status):
        """
        Get all companies with a specific status.
        """
        companies = Company.objects.filter(status=status)
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def delete_company(company_id):
        """
        Delete a company.
        """
        company = Company.objects.get(id=company_id)
        company.delete()

        return True
    
    @staticmethod
    def delete_company_update(update_id):
        """
        Delete a company update.
        """
        update = CompanyUpdate.objects.get(id=update_id)
        update.delete()

        return True
    
    @staticmethod
    def delete_all_companies():
        """
        Delete all companies.
        """
        companies = Company.objects.all()
        companies.delete()

        return True
    
    

