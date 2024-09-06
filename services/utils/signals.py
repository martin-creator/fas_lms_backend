import logging
import os
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from services.models import FileRecord, Project, Certification, Notification, UserActivityLog
from services.notifications import NotificationHandler
from services.exceptions import SignalHandlingException
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_migrate


logger = logging.getLogger(__name__)

class SignalHandler:
    @staticmethod
    @receiver(post_save, sender=User)
    def handle_user_created(sender, instance, created, **kwargs):
        """
        Handle actions after a User instance is created.
        """
        if created:
            try:
                # Send a welcome email to the new user
                subject = "Welcome to Our LMS"
                message = f"Hello {instance.username}, welcome to our LMS!"
                from_email = "no-reply@lms.com"
                recipient_list = [instance.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                logger.info(f"Welcome email sent to user: {instance.username}")

                # Send a notification to the admin
                NotificationHandler.send_in_app_notification(User.objects.get(is_superuser=True), "New User Signup", f"User {instance.username} has signed up.")
            except Exception as e:
                logger.error(f"Error handling user creation signal for user {instance.username}: {e}")
                raise SignalHandlingException("Failed to handle user creation signal.")

    @staticmethod
    @receiver(pre_delete, sender=FileRecord)
    def handle_file_record_deletion(sender, instance, **kwargs):
        """
        Handle actions before a FileRecord instance is deleted.
        """
        try:
            # Delete the file from the filesystem
            if instance.file_path:
                os.remove(instance.file_path)
                logger.info(f"File deleted: {instance.file_path}")
        except Exception as e:
            logger.error(f"Error handling file deletion signal for file {instance.file_id}: {e}")
            raise SignalHandlingException("Failed to handle file deletion signal.")

    @staticmethod
    @receiver(post_save, sender=Project)
    def handle_project_update(sender, instance, created, **kwargs):
        """
        Handle actions after a Project instance is created or updated.
        """
        try:
            if created:
                # Send a notification to the project owner
                NotificationHandler.send_in_app_notification(instance.owner, "Project Created", f"Your project {instance.name} has been created.")
                logger.info(f"Project creation notification sent to user: {instance.owner.username}")
            else:
                # Send a notification to the project owner about the update
                NotificationHandler.send_in_app_notification(instance.owner, "Project Updated", f"Your project {instance.name} has been updated.")
                logger.info(f"Project update notification sent to user: {instance.owner.username}")
        except Exception as e:
            logger.error(f"Error handling project update signal for project {instance.name}: {e}")
            raise SignalHandlingException("Failed to handle project update signal.")

    @staticmethod
    @receiver(post_save, sender=Certification)
    def handle_certification_issued(sender, instance, created, **kwargs):
        """
        Handle actions after a Certification instance is created.
        """
        if created:
            try:
                # Send a certification email to the user
                subject = "Certification Awarded"
                message = f"Congratulations {instance.user.username}, you have been awarded a certification for {instance.related_courses.first().name}!"
                from_email = "no-reply@lms.com"
                recipient_list = [instance.user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                logger.info(f"Certification email sent to user: {instance.user.username}")

                # Send an in-app notification to the user
                NotificationHandler.send_in_app_notification(instance.user, "Certification Awarded", f"You have been awarded a certification for {instance.related_courses.first().name}.")
            except Exception as e:
                logger.error(f"Error handling certification issued signal for user {instance.user.username}: {e}")
                raise SignalHandlingException("Failed to handle certification issued signal.")

    @staticmethod
    @receiver(post_save, sender=Notification)
    def handle_notification_sent(sender, instance, created, **kwargs):
        """
        Handle actions after a Notification instance is created.
        """
        if created:
            try:
                # Log the notification event
                logger.info(f"Notification sent to user: {instance.user.username}, message: {instance.message}")
            except Exception as e:
                logger.error(f"Error handling notification sent signal for user {instance.user.username}: {e}")
                raise SignalHandlingException("Failed to handle notification sent signal.")

    @staticmethod
    @receiver(post_save, sender=UserActivityLog)
    def handle_user_activity_logged(sender, instance, created, **kwargs):
        """
        Handle actions after a UserActivityLog instance is created.
        """
        if created:
            try:
                # Log the user activity
                logger.info(f"User activity logged: {instance.user.username}, activity: {instance.activity_type}")
            except Exception as e:
                logger.error(f"Error handling user activity logged signal for user {instance.user.username}: {e}")
                raise SignalHandlingException("Failed to handle user activity logged signal.")

    @staticmethod
    def connect_signals():
        """
        Connect all the signals.
        """
        post_save.connect(SignalHandler.handle_user_created, sender=User)
        pre_delete.connect(SignalHandler.handle_file_record_deletion, sender=FileRecord)
        post_save.connect(SignalHandler.handle_project_update, sender=Project)
        post
        
        

class ExtendedSignalHandler:
    @staticmethod
    @receiver(user_logged_in)
    def handle_user_login(sender, request, user, **kwargs):
        """
        Handle actions after a user logs in.
        """
        try:
            # Log the login activity
            logger.info(f"User logged in: {user.username}")

            # Log the user login activity
            UserActivityLog.objects.create(user=user, activity_type='login', description="User logged in")
            
            # Send a notification to the user
            NotificationHandler.send_in_app_notification(user, "Login Alert", "You have logged in successfully.")
        except Exception as e:
            logger.error(f"Error handling user login signal for user {user.username}: {e}")
            raise SignalHandlingException("Failed to handle user login signal.")
    
    @staticmethod
    @receiver(user_logged_out)
    def handle_user_logout(sender, request, user, **kwargs):
        """
        Handle actions after a user logs out.
        """
        try:
            # Log the logout activity
            logger.info(f"User logged out: {user.username}")

            # Log the user logout activity
            UserActivityLog.objects.create(user=user, activity_type='logout', description="User logged out")
            
            # Send a notification to the user
            NotificationHandler.send_in_app_notification(user, "Logout Alert", "You have logged out successfully.")
        except Exception as e:
            logger.error(f"Error handling user logout signal for user {user.username}: {e}")
            raise SignalHandlingException("Failed to handle user logout signal.")
    
    @staticmethod
    @receiver(pre_delete, sender=Project)
    def handle_project_deletion(sender, instance, **kwargs):
        """
        Handle actions before a Project instance is deleted.
        """
        try:
            # Notify project owner about the deletion
            NotificationHandler.send_in_app_notification(instance.owner, "Project Deletion", f"Your project {instance.name} is being deleted.")
            
            # Log the project deletion
            logger.info(f"Project deleted: {instance.name}, owner: {instance.owner.username}")

            # Log the user activity
            UserActivityLog.objects.create(user=instance.owner, activity_type='project_deletion', description=f"Project {instance.name} deleted")
        except Exception as e:
            logger.error(f"Error handling project deletion signal for project {instance.name}: {e}")
            raise SignalHandlingException("Failed to handle project deletion signal.")
    
    @staticmethod
    @receiver(post_migrate)
    def handle_post_migrate(sender, **kwargs):
        """
        Handle actions after all migrations have been applied.
        """
        try:
            # Example of post-migrate tasks, e.g., initializing default settings
            logger.info("Migrations completed. Running post-migration tasks.")
            
            # Example task: Ensure default projects or users are created
            if not Project.objects.exists():
                Project.objects.create(name="Default Project", description="This is a default project created post-migration.")
                logger.info("Default project created post-migration.")
        except Exception as e:
            logger.error(f"Error handling post-migrate signal: {e}")
            raise SignalHandlingException("Failed to handle post-migrate signal.")
    
    @staticmethod
    def connect_additional_signals():
        """
        Connect additional signals.
        """
        user_logged_in.connect(ExtendedSignalHandler.handle_user_login)
        user_logged_out.connect(ExtendedSignalHandler.handle_user_logout)
        pre_delete.connect(ExtendedSignalHandler.handle_project_deletion, sender=Project)
        post_migrate.connect(ExtendedSignalHandler.handle_post_migrate)

# Ensure all signals are connected
SignalHandler.connect_signals()
ExtendedSignalHandler.connect_additional_signals()