from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from certifications.models import Certification, LinkedInBadge
from certifications.serializers import CertificationSerializer, LinkedInBadgeSerializer
from certifications.settings.certifications_settings import CertificationsSettings
from certifications.querying.certifications_query import CertificationQuery
from certifications.helpers.certifications_helpers import CertificationHelpers
from certifications.utils import UserUtils, DateTimeUtils
from certifications.reports.certifications_report import CertificationsReport


class CompanyService:

    @staticmethod
    def get_companies():
        """
        Get all companies.
        """
        companies = CompanyQuery.get_companies()
        return companies
    

    @staticmethod
    def get_company(company_id):
        """
        Get a specific company.
        """
        company = CompanyQuery.get_company(company_id)
        return company
    
    @staticmethod
    def create_company(company_data):
        """
        Create a new company.
        """
        company, categories, members, followers = CompanyHelpers.process_company_data(company_data)
        company.save()

        if categories:
            company.categories.set(categories)
        
        if members:
            company.members.set(members)

        if followers:
            company.followers.set(followers)

        serializer = CompanySerializer(company)

        return serializer.data
    

    @staticmethod
    def update_company(company_id, company_data):
        """
        Update a company.
        """
        company, categories, members, followers =  CompanyHelpers.process_company_data_update(company_id, company_data)
        company.save()

        if categories:
            company.categories.set(categories)
        
        if members:
            company.members.set(members)

        if followers:
            company.followers.set(followers)

        serializer = CompanySerializer(company)

        return serializer.data
    

    @staticmethod
    def delete_company(company_id):
        """
        Delete a company.
        """
        company = CompanyQuery.get_company(company_id)
        company.delete()

        return True
    

    @staticmethod
    def delete_all_companies():
        """
        Delete all companies.
        """
        companies = CompanyQuery.get_companies()
        companies.delete()

        return True
    

    @staticmethod
    def get_company_updates(company_id):
        """
        Get all updates for a specific company.
        """
        updates = CompanyQuery.get_company_updates(company_id)
        
        return updates
    

    @staticmethod
    def get_company_update_by_id(update_id):
        """
        Get a specific update for a company.
        """
        update = CompanyQuery.get_company_update(update_id)
        return update
    


    @staticmethod
    def create_company_update(company_id, update_data):
        """
        Create a new update for a company.
        """
        company_update = CompanyHelpers.process_company_update_data(company_id, update_data)
        company_update.save()

        serializer = CompanyUpdateSerializer(company_update)

        return serializer.data
    

    @staticmethod
    def update_company_update(company_id, update_id, update_data):
        """
        Update an update for a company.
        """
        company_update = CompanyHelpers.process_company_update_data_update(update_id, update_data)
        company_update.save()

        serializer = CompanyUpdateSerializer(company_update)

        return serializer.data
    

    @staticmethod
    def delete_company_update(update_id):
        """
        Delete an update for a company.
        """
        company_update = CompanyQuery.get_company_update(update_id)
        company_update.delete()

        return True
    



# class EventService:

#     @staticmethod
#     def get_events():
#         """
#         Get all events.
#         """
#         events = EventQuery.get_events()
#         return events
    

#     @staticmethod
#     def get_event(event_id):
#         """
#         Get a specific event.
#         """
#         event = EventQuery.get_event(event_id)
#         return event

#     @staticmethod
#     def create_event(event_data):
#         """
#         Create a new event.
#         """

#         event, event_tags = EventQuery.process_event_data(event_data)
#         event.save()

#         if event_tags:
#             event.tags.set(event_tags)

#         serializer = EventSerializer(event)

#         return serializer.data
    

#     @staticmethod
#     def update_event(event_id, event_data):
#         """
#         Update an event.
#         """

#         # event = EventQuery.get_event(event_id)
#         event, event_tags = EventQuery.process_event_update_data(event_id, event_data)
#         event.save()

#         if event_tags:
#             event.tags.set(event_tags)

#         serializer = EventSerializer(event)

#         return serializer.data
    

#     @staticmethod
#     def delete_event(event_id):
#         """
#         Delete an event.
#         """
#         event = EventQuery.get_event(event_id)
#         event.delete()

#         return True
    
    
#     @staticmethod
#     def delete_all_events():
#         """
#         Delete all events.
#         """
#         events = EventQuery.get_events()
#         events.delete()

#         return True
    

#     @staticmethod
#     def get_event_report(event_id):
#         """
#         Get a report for a specific event.
#         """
#         event = EventQuery.get_event(event_id)
#         report = EventReport.get_event_report(event)

#         return report
    

#     @staticmethod
#     def get_attendee_report(attendee_id):
#         """
#         Get a report for a specific attendee.
#         """
#         attendee = UserUtils.get_current_user(attendee_id)
#         report = EventReport.get_attendee_report(attendee)

#         return report
    
#     @staticmethod
#     def register_for_event(event_id, attendee_id):
#         """
#         Register for an event.
#         """
#         event = EventQuery.get_event(event_id)
#         attendee = UserUtils.get_current_user(attendee_id)

#         registration = EventRegistration(event=event, attendee=attendee)
#         registration.save()

#         return True


#     @staticmethod
#     def unregister_from_event(event_id, attendee_id):
#         """
#         Unregister from an event.
#         """
#         registration = EventQuery.get_event_registration(event_id, attendee_id)
#         registration.delete()

#         return True
    

#     @staticmethod
#     def provide_event_feedback(event_id, attendee_id, feedback_data):
#         """
#         Provide feedback for an event.
#         """
#         event = EventQuery.get_event(event_id)
#         attendee = UserUtils.get_current_user(attendee_id)

#         feedback = EventFeedback(event=event, attendee=attendee, **feedback_data)
#         feedback.save()

#         return True

    
#     @staticmethod
#     def get_events_by_organizer(organizer_id):
#         """
#         Get all events organized by a specific organizer.
#         """
#         events = EventQuery.get_events_by_organizer(organizer_id)
#         return events
    

#     @staticmethod
#     def get_events_by_attendee(attendee_id):
#         """
#         Get all events attended by a specific attendee.
#         """
#         events = EventQuery.get_events_by_attendee(attendee_id)
#         return events
    

#     @staticmethod   
#     def get_event_attendees(event_id):
#         """
#         Get all attendees for an event.
#         """
#         attendees = EventQuery.get_event_attendees(event_id)
#         return attendees


#     @staticmethod
#     def get_event_registrations(event_id):
#         """
#         Get all registrations for a specific event.
#         """
#         registrations = EventQuery.get_event_registrations(event_id)
#         return registrations
    

#     @staticmethod
#     def get_event_feedbacks(event_id):
#         """
#         Get all feedbacks for a specific event.
#         """
#         feedbacks = EventQuery.get_event_feedbacks(event_id)
#         return feedbacks
    

#     @staticmethod
#     def get_events_monthly_report():
#         """
#         Get a monthly report for all events.
#         """
#         report = EventReport.get_events_monthly_report()
#         return report
    

    
    
    

    

    


        