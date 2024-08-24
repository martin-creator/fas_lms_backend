from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import Count
from jobs.models import JobListing, JobApplication, JobNotification, Interview
from jobs.serializers import JobListingSerializer, JobApplicationSerializer, JobNotificationSerializer, InterviewSerializer
from jobs.querying.jobs_query import JobQuery
from jobs.settings.jobs_settings import JobsSettings
from jobs.helpers.jobs_helpers import JobHelpers
from jobs.utils import UserUtils, DateTimeUtils
from jobs.reports.jobs_report import JobReport

# genarate the most relevant CRUD epoints for all modules to make this jobs service

class JobService:
    
        @staticmethod
        def get_jobs():
            """
            Get all jobs.
            """
            jobs = JobQuery.get_jobs()
            return jobs
        
    
        @staticmethod
        def get_job(job_id):
            """
            Get a specific job.
            """
            job = JobQuery.get_job(job_id)
            return job
        
    
        @staticmethod
        def create_job(job_data):
            """
            Create a new job.
            """
            job = JobHelpers.process_job_data(job_data)
            job.save()
    
            serializer = JobListingSerializer(job)
    
            return serializer.data
        
    
        @staticmethod
        def update_job(job_id, job_data):
            """
            Update a job.
            """
            job = JobQuery.get_job(job_id)
            job = JobHelpers.process_job_update_data(job, job_data)
            job.save()
    
            serializer = JobListingSerializer(job)
    
            return serializer.data
        
    
        @staticmethod
        def delete_job(job_id):
            """
            Delete a job.
            """
            job = JobQuery.get_job(job_id)
            job.delete()
    
            return True
        
    
        @staticmethod
        def delete_all_jobs():
            """
            Delete all jobs.
            """
            jobs = JobQuery.get_jobs()
            jobs.delete()
    
            return True
        
    
        @staticmethod
        def get_job_applications(job_id):
            """
            Get all applications for a specific job.
            """
            applications = JobQuery.get_job_applications(job_id)
            return applications
        

        @staticmethod
        def get_job_application(application_id):
            """
            Get a specific job application.
            """
            application = JobQuery.get_job_application(application_id)
            return application
        

        @staticmethod
        def get_job_application_by_applicant(applicant_id):
            """
            Get all job applications for a specific applicant.
            """
            applications = JobQuery.get_job_application_by_applicant(applicant_id)
            return applications
        

        @staticmethod
        def get_jobs_by_company(company_id):
            """
            Get all jobs for a specific company.
            """
            jobs = JobQuery.get_jobs_by_company(company_id)
            return jobs
        

        @staticmethod
        def create_job_application(application_data):
            """
            Create a new job application.
            """
            application = JobHelpers.process_job_application_data(application_data)
            application.save()
    
            serializer = JobApplicationSerializer(application)
    
            return serializer.data
        

        @staticmethod
        def update_job_application(application_id, application_data):
            """
            Update a job application.
            """
            application = JobQuery.get_job_application(application_id)
            application = JobHelpers.process_job_application_update_data(application, application_data)
            application.save()
    
            serializer = JobApplicationSerializer(application)
    
            return serializer.data
        


        @staticmethod
        def delete_job_application(application_id):
            """
            Delete a job application.
            """
            application = JobQuery.get_job_application(application_id)
            application.delete()
    
            return True
        
    
    
        @staticmethod
        def get_job_notifications(job_id):
            """
            Get all notifications for a specific job.
            """
            notifications = JobQuery.get_job_notifications(job_id)
            return notifications
        

        @staticmethod
        def get_job_notification(notification_id):
            """
            Get a specific job notification.
            """
            notification = JobQuery.get_job_notification(notification_id)
            return notification
        

        @staticmethod
        def get_job_notification_by_user(user_id):
            """
            Get all notifications for a specific user.
            """
            notifications = JobQuery.get_job_notification_by_user(user_id)
            return notifications
        

        @staticmethod
        def create_job_notification(notification_data):
            """
            Create a new job notification.
            """
            notification = JobHelpers.process_job_notification_data(notification_data)
            notification.save()
    
            serializer = JobNotificationSerializer(notification)
    
            return serializer.data
        

        @staticmethod
        def update_job_notification(notification_id, notification_data):
            """
            Update a job notification.
            """
            notification = JobQuery.get_job_notification(notification_id)
            notification = JobHelpers.process_job_notification_update_data(notification, notification_data)
            notification.save()
    
            serializer = JobNotificationSerializer(notification)
    
            return serializer.data
        

        @staticmethod
        def delete_job_notification(notification_id):
            """
            Delete a job notification.
            """
            notification = JobQuery.get_job_notification(notification_id)
            notification.delete()
    
            return True
        

        @staticmethod
        def delete_all_job_notifications():
            """
            Delete all job notifications.
            """
            notifications = JobQuery.get_job_notifications()
            notifications.delete()
    
            return True
        

        @staticmethod
        def get_interviews():
            """
            Get all interviews.
            """
            interviews = JobQuery.get_interviews()
            return interviews
        

        @staticmethod
        def get_interview(interview_id):
            """
            Get a specific interview.
            """
            interview = JobQuery.get_interview(interview_id)
            return interview
        

        @staticmethod
        def get_interviews_by_job(job_id):
            """
            Get all interviews for a specific job.
            """
            interviews = JobQuery.get_interviews_by_job(job_id)
            return interviews
        

        @staticmethod
        def get_interviews_by_job_application(application_id):
            """
            Get all interviews for a specific job application.
            """
            interviews = JobQuery.get_interviews_by_job_application(application_id)
            return interviews
        
        

        @staticmethod
        def create_interview(interview_data):
            """
            Create a new interview.
            """
            interview = JobHelpers.process_interview_data(interview_data)
            interview.save()
    
            serializer = InterviewSerializer(interview)
    
            return serializer.data
        

        @staticmethod
        def update_interview(interview_id, interview_data):
            """
            Update an interview.
            """
            interview = JobQuery.get_interview(interview_id)
            interview = JobHelpers.process_interview_data_update(interview, interview_data)
            interview.save()
    
            serializer = InterviewSerializer(interview)
    
            return serializer.data
        


        @staticmethod
        def delete_interview(interview_id):
            """
            Delete an interview.
            """
            interview = JobQuery.get_interview(interview_id)
            interview.delete()
    
            return True
        

        @staticmethod
        def delete_all_interviews():
            """
            Delete all interviews.
            """
            interviews = JobQuery.get_interviews()
            interviews.delete()
    
            return True     
        
    
    
        @staticmethod
        def generate_job_application_report(job_id):
            """
            Generate a report for a specific job application.
            """
            report = JobReport.generate_job_application_report(job_id)
            return report
        
    
        @staticmethod
        def generate_job_summary():
            """
            Generate a summary report for all jobs.
            """
            report = JobReport.generate_job_summary()
            return report
        
    
        @staticmethod
        def get_interviews_by_job(job_id):
            """
            Get all interviews for a specific job.
            """
            interviews = JobQuery.get_interviews_by_job(job_id)
            return interviews
        

        @staticmethod
        def get_interviews_by_job_application(application_id):
            """
            Get all interviews for a specific job application.
            """
            interviews = JobQuery.get_interviews_by_job_application(application_id)
            return interviews
        





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
    

    
    
    

    

    


        