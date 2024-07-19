UserProfile
 └── user (OneToOneField) -> User
 └── followers (ManyToManyField) -> self
 └── skills (ManyToManyField) -> Skill
 └── experiences (ManyToManyField) -> Experience
 └── educations (ManyToManyField) -> Education
 └── endorsements (ManyToManyField) -> Endorsement
 └── job_applications (ManyToManyField) -> jobs.JobApplication
 └── job_listings (ManyToManyField) -> jobs.JobListing
 └── notifications (ManyToManyField) -> notifications.Notification
 └── followers (ManyToManyField) -> Follower
 └── follow_requests (ManyToManyField) -> FollowRequest
 └── shares (ManyToManyField) -> activity.Share

Experience
 └── user (ForeignKey) -> UserProfile
 └── company (ForeignKey) -> companies.Company
 └── shares (ManyToManyField) -> activity.Share

Education
 └── user (ForeignKey) -> UserProfile
 └── shares (ManyToManyField) -> activity.Share

Skill
 └── users (ManyToManyField) -> UserProfile
 └── shares (ManyToManyField) -> activity.Share
 └── endorsements (ManyToManyField) -> Endorsement
 └── job_applications (ManyToManyField) -> jobs.JobApplication
 └── job_listings (ManyToManyField) -> jobs.JobListing
 └── notifications (ManyToManyField) -> notifications.Notification
 └── verified_from (ManyToManyField) -> UserProfile
 └── verified_to (ManyToManyField) -> UserProfile

Endorsement
 └── skill (ForeignKey) -> Skill
 └── endorsed_by (ForeignKey) -> UserProfile
 └── endorsed_user (ForeignKey) -> UserProfile
 └── shares (ManyToManyField) -> activity.Share

Achievement
 └── user (ForeignKey) -> UserProfile

Portfolio
 └── user (ForeignKey) -> UserProfile

LogEntry
 └── content_type (ForeignKey) -> ContentType

Permission
 └── content_type (ForeignKey) -> ContentType

Group
 └── categories (ManyToManyField) -> Category
 └── shares (ManyToManyField) -> Share

PermissionsMixin
 └── groups (ManyToManyField) -> Group
 └── user_permissions (ManyToManyField) -> Permission

ContentType

EmailAddress

EmailConfirmation
 └── email_address (ForeignKey) -> EmailAddress

SocialApp

SocialAccount

SocialToken
 └── app (ForeignKey) -> SocialApp
 └── account (ForeignKey) -> SocialAccount

SolarSchedule

IntervalSchedule

ClockedSchedule

CrontabSchedule

PeriodicTasks

PeriodicTask
 └── interval (ForeignKey) -> IntervalSchedule
 └── crontab (ForeignKey) -> CrontabSchedule
 └── solar (ForeignKey) -> SolarSchedule
 └── clocked (ForeignKey) -> ClockedSchedule

Token

TagBase

ItemBase

Category

Share
 └── content_type (ForeignKey) -> ContentType
 └── content_object (GenericForeignKey) -> content_type
 └── attachments (GenericRelation) -> Attachment

Reaction
 └── message (ForeignKey) -> messaging.Message
 └── post (ForeignKey) -> posts.Post
 └── comment (ForeignKey) -> posts.Comment
 └── job_post (ForeignKey) -> jobs.JobListing
 └── group (ForeignKey) -> groups.Group

Attachment
 └── content_type (ForeignKey) -> ContentType
 └── content_object (GenericForeignKey) -> content_type

Thread

UserActivity
 └── categories (ManyToManyField) -> Category

UserStatistics

MarketingCampaign
 └── categories (ManyToManyField) -> Category
 └── attachments (GenericRelation) -> Attachment

LearningService
 └── categories (ManyToManyField) -> Category
 └── attachments (GenericRelation) -> Attachment

Analytics
 └── categories (ManyToManyField) -> Category

ChatRoom

Message
 └── chat (ForeignKey) -> ChatRoom
 └── attachments (ManyToManyField) -> activity.Attachment
 └── parent_message (ForeignKey) -> self
 └── reactions (ManyToManyField) -> activity.Reaction
 └── shares (ManyToManyField) -> activity.Share

NotificationType

Notification
 └── content_type (ForeignKey) -> ContentType
 └── content_object (GenericForeignKey) -> content_type
 └── notification_type (ForeignKey) -> NotificationType
 └── shares (ManyToManyField) -> Share

NotificationTemplate
 └── notification_type (ForeignKey) -> NotificationType

NotificationSettings
 └── notification_type (ForeignKey) -> NotificationType

NotificationReadStatus
 └── notification (ForeignKey) -> Notification

Post
 └── group (ForeignKey) -> groups.Group
 └── attachments (GenericRelation) -> Attachment
 └── categories (ManyToManyField) -> activity.Category
 └── reactions (ManyToManyField) -> activity.Reaction
 └── comments (ManyToManyField) -> Comment
 └── shares (ManyToManyField) -> activity.Share

Comment
 └── post (ForeignKey) -> Post
 └── attachments (GenericRelation) -> Attachment
 └── parent_comment (ForeignKey) -> self
 └── reactions (ManyToManyField) -> activity.Reaction

JobListing
 └── company (ForeignKey) -> companies.Company
 └── attachments (GenericRelation) -> activity.Attachment
 └── categories (ManyToManyField) -> activity.Category
 └── skills_required (ManyToManyField) -> profiles.Skill
 └── applications (ManyToManyField) -> JobApplication
 └── notifications (ManyToManyField) -> JobNotification
 └── shares (ManyToManyField) -> activity.Share

JobApplication
 └── job_listing (ForeignKey) -> JobListing
 └── attachments (GenericRelation) -> activity.Attachment
 └── shares (ManyToManyField) -> activity.Share

JobNotification
 └── job_listing (ForeignKey) -> JobListing
 └── shares (ManyToManyField) -> activity.Share

GroupMembership
 └── group (ForeignKey) -> Group

Follower

FollowRequest

FollowNotification

Event
 └── organizer (ForeignKey) -> UserProfile
 └── attachments (GenericRelation) -> Attachment
 └── categories (ManyToManyField) -> Category
 └── attendees (ManyToManyField) -> UserProfile

Course
 └── attachments (GenericRelation) -> Attachment
 └── categories (ManyToManyField) -> activity.Category
 └── shares (ManyToManyField) -> activity.Share
 └── comments (ManyToManyField) -> posts.Comment
 └── reactions (ManyToManyField) -> activity.Reaction

CourseEnrollment
 └── course (ForeignKey) -> Course

CourseCompletion
 └── course (ForeignKey) -> Course
 └── certificate (ForeignKey) -> certifications.Certification

ConnectionRequest
 └── from_user (ForeignKey) -> UserProfile
 └── to_user (ForeignKey) -> UserProfile

Connection
 └── user (ForeignKey) -> UserProfile
 └── connection (ForeignKey) -> UserProfile

Recommendation
 └── recommended_by (ForeignKey) -> UserProfile
 └── recommended_user (ForeignKey) -> UserProfile

Company
 └── attachments (GenericRelation) -> Attachment
 └── categories (ManyToManyField) -> Category

CompanyUpdate
 └── company (ForeignKey) -> Company
 └── attachments (GenericRelation) -> Attachment

Certification
 └── attachments (GenericRelation) -> Attachment
 └── categories (ManyToManyField) -> activity.Category
 └── related_jobs (ManyToManyField) -> jobs.JobListing
 └── related_courses (ManyToManyField) -> courses.Course

