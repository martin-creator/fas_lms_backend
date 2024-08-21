from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from companies.models import Company, CompanyUpdate
from companies.serializers import CompanySerializer, CompanyUpdateSerializer
from companies.querying.companies_query import CompanyQuery


class CompanyReport:
    @staticmethod
    def get_company_report(company):
        """
        Get a report for a specific company.
        """
        company_data = CompanySerializer(company).data
        company_updates = CompanyUpdate.objects.filter(company=company)
        company_data['updates'] = CompanyUpdateSerializer(company_updates, many=True).data

        # return json data

        json_data = {
            'company': company_data,
            'updates': company_data['updates']
        }

        return json_data

    @staticmethod
    def get_owner_report(owner):
        """
        Get a report for a specific owner.
        """
        owner_data = {}
        owner_data['companies'] = CompanyQuery.get_companies_by_owner(owner).count()
        owner_data['updates'] = CompanyQuery.get_company_updates_by_owner(owner).count()

        return owner_data

    @staticmethod
    def get_employees_report():
        """
        Get a report for all employees.
        """
        employees = Company.objects.all()
        serializer = CompanySerializer(employees, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_location_report():
        """
        Get a location report for all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_monthly_report():
        """
        Get a monthly report for all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_industry_report():
        """
        Get an industry report for all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_employees_report():
        """
        Get an employees report for all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data
    
    @staticmethod
    def get_companies_owners_report():
        """
        Get an owners report for all companies.
        """
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data