from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from datetime import timedelta
# from posts.models import Comment
# from certifications.models import Certification
from django.contrib.contenttypes.fields import GenericRelation

class Course(models.Model):
    """
    Represents a course that students can enroll in.
    
    Attributes:
        title (CharField): The title of the course.
        description (TextField): A detailed description of the course.
        attachments (GenericRelation): A relation to attachments related to the course.
        categories (ManyToManyField): The categories to which the course belongs.
        instructor (ForeignKey): The instructor teaching the course.
        students (ManyToManyField): The students enrolled in the course.
        shares (ManyToManyField): Shares related to the course.
        comments (ManyToManyField): Comments made on the course.
        reactions (ManyToManyField): Reactions to the course.
        tags (TaggableManager): Tags associated with the course.
        prerequisites (ManyToManyField): Courses that are prerequisites for this course.
        duration (DurationField): The duration of the course.
        language (CharField): The language in which the course is taught.
        level (CharField): The level of the course (Beginner, Intermediate, Advanced).
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachments = GenericRelation('Attachment')
    categories = models.ManyToManyField('activity.Category', related_name='courses_categories')
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='instructed_courses', on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CourseEnrollment', related_name='enrolled_courses')
    shares = models.ManyToManyField('activity.Share', related_name='course_shares', blank=True)
    comments = models.ManyToManyField('posts.Comment', related_name='course_comments', blank=True)
    reactions = models.ManyToManyField('activity.Reaction', related_name='course_reactions', blank=True)
    tags = TaggableManager()
    # video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, related_name='required_for_courses', blank=True)
    duration = models.DurationField(default=timedelta(weeks=1))
    language = models.CharField(max_length=50, default='English')
    level = models.CharField(max_length=50, choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], null=True, blank=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """
    Represents a lesson within a course.
    
    Attributes:
        course (ForeignKey): The course to which the lesson belongs.
        title (CharField): The title of the lesson.
        description (TextField): A detailed description of the lesson.
        content (TextField): The content of the lesson.
        video_url (URLField): Optional URL for a video lesson.
        attachments (GenericRelation): A relation to attachments related to the lesson.
        tags (TaggableManager): Tags associated with the lesson.
        other_reading_links (ManyToManyField): Other reading links related to the lesson.
        order (PositiveIntegerField): The order of the lesson within the course.
    """
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True, null=True)
    content = models.TextField(default='', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    attachments = GenericRelation('Attachment')
    tags = TaggableManager()
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    

class LessonProgress(models.Model):
    """
    Represents the progress of a user through a lesson.

    Attributes:
        user (ForeignKey): The user who is progressing through the lesson.
        lesson (ForeignKey): The lesson being tracked.
        completed_at (DateTimeField): The date and time when the lesson was completed.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"
    
    


    

class Quiz(models.Model):
    """
    Represents a quiz associated with a lesson.

    Attributes:
        lesson (ForeignKey): The lesson to which the quiz belongs.
        title (CharField): The title of the quiz.
        description (TextField): A detailed description of the quiz.
        questions (ManyToManyField): The questions that are part of the quiz.
    """
    lesson = models.ForeignKey(Lesson, related_name='quizzes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(default='', blank=True, null=True)
    questions = models.ManyToManyField('Question', related_name='quizzes')

    def __str__(self):
        return f"Quiz for {self.lesson.title}"

class Question(models.Model):
    """
    Represents a question in a quiz.

    Attributes:
        text (TextField): The text of the question.
        choices (ManyToManyField): The possible choices for the question.
        correct_choice (ForeignKey): The correct choice for the question.
    """
    text = models.TextField(default='', blank=True, null=True)
    choices = models.ManyToManyField('Choice', related_name='questions')
    correct_choice = models.ForeignKey('Choice', related_name='correct_for_questions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    """
    Represents a choice for a quiz question.

    Attributes:
        text (CharField): The text of the choice.
    """
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    

class QuizProgress(models.Model):
    """
    Represents the progress of a user through a quiz.

    Attributes:
        user (ForeignKey): The user who is progressing through the quiz.
        quiz (ForeignKey): The quiz being tracked.
        completed_at (DateTimeField): The date and time when the quiz was completed.
        score (IntegerField): The score achieved by the user in the quiz.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='progress', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"


class CourseEnrollment(models.Model):
    """
    Represents the enrollment of a student in a course.
    
    Attributes:
        course (ForeignKey): The course in which the student is enrolled.
        student (ForeignKey): The student enrolled in the course.
        enrolled_at (DateTimeField): The date and time when the student enrolled.
        progress (FloatField): The student's progress in the course as a percentage.
    """
    course = models.ForeignKey(Course, related_name='enrolled_courses', on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0)  # Track progress as a percentage

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

class CourseCompletion(models.Model):
    """
    Represents the completion of a course by a student.
    
    Attributes:
        course (ForeignKey): The course that was completed.
        student (ForeignKey): The student who completed the course.
        completed_at (DateTimeField): The date and time when the course was completed.
        certificate_url (URLField): Optional URL for the course completion certificate.
        certificate (ForeignKey): The certificate associated with the course completion.
        tags (TaggableManager): Tags associated with the course completion.
    """
    course = models.ForeignKey(Course, related_name='completions', on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='completed_courses', on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    certificate_url = models.URLField(blank=True, null=True)
    certificate = models.ForeignKey('certifications.Certification', related_name='course_completions', on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()

    def __str__(self):
        return f"{self.student.username} completed {self.course.title}"

# class Certification(models.Model):
#     """
#     Represents a certification that can be awarded upon course completion.
    
#     Attributes:
#         name (CharField): The name of the certification.
#         issuing_organization (CharField): The organization issuing the certification.
#         description (TextField): A detailed description of the certification.
#         url (URLField): Optional URL for more information about the certification.
#         tags (TaggableManager): Tags associated with the certification.
#     """
#     name = models.CharField(max_length=255)
#     issuing_organization = models.CharField(max_length=255)
#     description = models.TextField()
#     url = models.URLField(blank=True, null=True)
#     tags = TaggableManager()

#     def __str__(self):
#         return self.name

class Attachment(models.Model):
    """
    Represents an attachment that can be related to courses and lessons.
    
    Attributes:
        file (FileField): The file of the attachment.
        uploaded_at (DateTimeField): The date and time when the attachment was uploaded.
    """
    file = models.FileField(upload_to='attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment {self.id}"




# from django.db import models
# from activity.models import Attachment
# # from posts.models import Comment
# # from certifications.models import Certification
# from taggit.managers import TaggableManager
# from django.contrib.contenttypes.fields import GenericRelation
# from django.conf import settings


# class Course(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     attachments = GenericRelation(Attachment)
#     categories = models.ManyToManyField('activity.Category', related_name='courses_categories')
#     instructor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='instructed_courses', on_delete=models.CASCADE)
#     students = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CourseEnrollment', related_name='enrolled_courses')
#     shares = models.ManyToManyField('activity.Share', related_name='course_shares', blank=True)
#     comments = models.ManyToManyField('posts.Comment', related_name='course_comments', blank=True)
#     reactions = models.ManyToManyField('activity.Reaction', related_name='course_reactions', blank=True)
#     tags = TaggableManager()

#     def __str__(self):
#         return self.title

# class CourseEnrollment(models.Model):
#     course = models.ForeignKey(Course, related_name='enrolled_courses', on_delete=models.CASCADE)
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     enrolled_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.student.user.username} enrolled in {self.course.title}"

# class CourseCompletion(models.Model):
#     course = models.ForeignKey(Course, related_name='completions', on_delete=models.CASCADE)
#     student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='completed_courses', on_delete=models.CASCADE)
#     completed_at = models.DateTimeField(auto_now_add=True)
#     certificate_url = models.URLField()
#     certificate = models.ForeignKey('certifications.Certification', related_name='course_completions', on_delete=models.SET_NULL, null=True, blank=True)
#     tags = TaggableManager()

#     def __str__(self):
#         return f"{self.student.user.username} completed {self.course.title}"