# utils/notification_utils.py 

from notifications.services.notification_service import NotificationService
from notifications.models import NotificationType
from django.contrib.auth.models import User
from courses.models import Course, Quiz, Lesson, Question

class NotificationUtils:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_or_create_notification_type(self, type_name):
        """
        Get or create a notification type.
        """
        try:
            notification_type, created = NotificationType.objects.get_or_create(type_name=type_name)
            return notification_type
        except Exception as e:
            raise ValueError(f"Failed to get or create notification type: {str(e)}")

    def send_notification(self, user, notification_type_name, content, url=''):
        """
        Send a notification to a specific user.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            notification_data = {
                'recipient': user.id,
                'notification_type': notification_type.id,
                'content': content,
                'url': url
            }
            self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to send notification to user {user.username}: {str(e)}")

    def notify_all_users(self, notification_type_name, content, url=''):
        """
        Notify all users.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            users = User.objects.all()
            for user in users:
                notification_data = {
                    'recipient': user.id,
                    'notification_type': notification_type.id,
                    'content': content,
                    'url': url
                }
                self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to notify all users: {str(e)}")

    def notify_admins(self, notification_type_name, content, url=''):
        """
        Notify all admin users.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                notification_data = {
                    'recipient': admin.id,
                    'notification_type': notification_type.id,
                    'content': content,
                    'url': url
                }
                self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to notify admins: {str(e)}")

    def notify_followers(self, user_profile, notification_type_name, content, url=''):
        """
        Notify followers of a user profile about an action.
        """
        try:
            notification_type = self.get_or_create_notification_type(notification_type_name)
            followers = user_profile.followers.all()
            for follower in followers:
                notification_data = {
                    'recipient': follower.id,
                    'notification_type': notification_type.id,
                    'content': content,
                    'url': url
                }
                self.notification_service.send_notification(notification_data)
        except Exception as e:
            raise ValueError(f"Failed to notify followers: {str(e)}")

    def handle_course_enrollment(self, user_id, course_id):
        """
        Handle notification for a user enrolling in a course.
        """
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        self.send_notification(
            user=user,
            notification_type_name='Course Enrollment',
            content=f'You have been enrolled in the course: {course.title}.',
            url=f'/courses/{course_id}/'
        )

    def handle_course_completion(self, user_id, course_id):
        """
        Handle notification for a user completing a course.
        """
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        self.send_notification(
            user=user,
            notification_type_name='Course Completion',
            content=f'Congratulations! You have completed the course: {course.title}.',
            url=f'/courses/{course_id}/completion/'
        )

    def handle_new_quiz(self, lesson_id, quiz_data):
        """
        Handle notification when a new quiz is added to a lesson.
        """
        lesson = Lesson.objects.get(id=lesson_id)
        quiz = Quiz.objects.create(**quiz_data, lesson=lesson)
        self.notify_all_users(
            notification_type_name='New Quiz Added',
            content=f'A new quiz has been added to the lesson: {lesson.title}.',
            url=f'/lessons/{lesson_id}/quizzes/{quiz.id}/'
        )

    def handle_question_update(self, quiz_id, question_data):
        """
        Handle notification when a question is added or updated in a quiz.
        """
        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.create(**question_data, quiz=quiz)
        self.notify_admins(
            notification_type_name='Question Added/Updated',
            content=f'A question has been added or updated in quiz: {quiz.title}.',
            url=f'/quizzes/{quiz_id}/questions/{question.id}/'
        )

    def handle_quiz_submission(self, user_id, quiz_id, answers):
        """
        Handle notification when a user submits a quiz.
        """
        user = User.objects.get(id=user_id)
        quiz = Quiz.objects.get(id=quiz_id)
        score = self.calculate_score(quiz, answers)
        # Save quiz progress logic here
        
        self.send_notification(
            user=user,
            notification_type_name='Quiz Submitted',
            content=f'Your results for the quiz "{quiz.title}" are now available.',
            url=f'/quizzes/{quiz_id}/results/'
        )

    def calculate_score(self, quiz, answers):
        """
        Calculate the score for a quiz based on the answers.
        """
        # Implement scoring logic
        return random.randint(0, 100)  # Placeholder for actual scoring logic
