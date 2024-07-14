# activity/utils/constants.py

class ActivityConstants:
    ACTIVITY_TYPES = [
        'post_created',
        'post_updated',
        'post_deleted',
        'comment_created',
        'comment_updated',
        'comment_deleted',
        'reaction_created',
        'reaction_updated',
        'reaction_deleted',
        'share_created',
        'attachment_added',
        'thread_created',
        'user_statistics_updated',
        'marketing_campaign_created',
        'marketing_campaign_updated',
        'learning_service_created',
        'learning_service_updated',
        'analytics_created',
        'analytics_updated',
    ]
    
    ATTACHMENT_TYPES = [
        ('photo', 'Photo'),
        ('document', 'Document'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('other', 'Other'),
    ]
