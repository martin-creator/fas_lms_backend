from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.querying.posts_querysets import PostQuerySet, CommentQuerySet
from posts.reports.posts_report import PostReport
from posts.settings.posts_settings import PostsSettings
from posts.utils import UserUtils, DateTimeUtils
from posts.services.posts_services import PostService




class CompanyController:
    
    def __init__(self):
        self.company_query = CompanyQuery()
        self.company_report = CompanyReport()
        self.company_settings = CompanySettings()
        self.user_utils = UserUtils()
        self.date_time_utils = DateTimeUtils()
        self.company_service = CompanyService()


    def get_all_companies(self):
        """
        Get all companies.
        """
        return self.company_service.get_companies()


    def get_company_by_id(self, company_id):
        """
        Get a specific company.
        """
        return self.company_service.get_company(company_id)


    def create_company(self, company_data):
        """
        Create a new company.
        """
        return self.company_service.create_company(company_data)
    

    def update_company(self, company_id, company_data):
        """
        Update a company.
        """
        return self.company_service.update_company(company_id, company_data)
    

    def delete_company(self, company_id):
        """
        Delete a company.
        """
        return self.company_service.delete_company(company_id)
    

    def delete_all_companies(self):
        """
        Delete all companies.
        """
        return self.company_service.delete_all_companies()
    

    def get_company_updates(self, company_id):
        """
        Get all updates for a company.
        """
        return self.company_service.get_company_updates(company_id)
    

    def get_company_update_by_id(self, update_id):
        """
        Get a specific company update.
        """
        return self.company_service.get_company_update_by_id(update_id)
    

    def create_company_update(self, company_id, update_data):
        """
        Create an update for a company.
        """
        return self.company_service.create_company_update(company_id, update_data)
    

    def update_company_update(self, company_id, update_id, update_data):
        """
        Update an update for a company.
        """
        return self.company_service.update_company_update(company_id, update_id, update_data)
    

    def delete_company_update(self, update_id):
        """
        Delete a company update.
        """
        return self.company_service.delete_company_update(update_id)



# class EventController:
    
#     def __init__(self):
#         self.event_query = EventQuery()
#         self.event_report = EventReport()
#         self.event_settings = EventSettings()
#         self.user_utils = UserUtils()
#         self.date_time_utils = DateTimeUtils()
#         self.event_service = EventService()

    
#     def get_all_events(self):
#         """
#         Get all events.
#         """
#         return self.event_service.get_events
    

#     def get_event(self, event_id):
#         """
#         Get a specific event.
#         """
#         return self.event_service.get_event(event_id)
    
#     def create_event(self, event_data):
#         """
#         Create a new event.
#         """
#         return self.event_service.create_event(event_data)
    
#     def update_event(self, event_id, event_data):
#         """
#         Update an event.
#         """
#         return self.event_service.update_event(event_id, event_data)
    
#     def delete_event(self, event_id):
#         """
#         Delete an event.
#         """
#         return self.event_service.delete_event(event_id)
    
#     def delete_all_events(self):
#         """
#         Delete all events.
#         """
#         return self.event_service.delete_all_events()
    
#     def register_for_event(self, event_id, user_id):
#         """
#         Register for an event.
#         """
#         return self.event_service.register_for_event(event_id, user_id)
    
#     def unregister_from_event(self, event_id, user_id):
#         """
#         Unregister from an event.
#         """
#         return self.event_service.unregister_from_event(event_id, user_id)
    
#     def provide_event_feedback(self, event_id, user_id, feedback_data):
#         """
#         Provide feedback for an event.
#         """
#         return self.event_service.provide_event_feedback(event_id, user_id, feedback_data)
    
#     def get_event_attendees(self, event_id):
#         """
#         Get all attendees for an event.
#         """
#         return self.event_service.get_event_attendees(event_id)
    
#     def get_event_registrations(self, event_id):
#         """
#         Get all registrations for an event.
#         """
#         return self.event_service.get_event_registrations(event_id)
    
#     def get_event_feedbacks(self, event_id):
#         """
#         Get all feedbacks for an event.
#         """
#         return self.event_service.get_event_feedbacks(event_id)
    

