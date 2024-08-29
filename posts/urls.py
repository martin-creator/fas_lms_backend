from django.urls import path
from posts import views


   
urlpatterns = [
    path('', views.get_all_posts, name='get_all_posts'),
    path('<int:post_id>/', views.get_specific_post, name='get_specific_post'),
    path('create/', views.create_post, name='create_post'),
    path('update/<int:post_id>/', views.update_post, name='update_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('report/<int:post_id>/', views.report_post, name='report_post'),
    path('resolve-report/<int:post_id>/', views.resolve_report_post, name='resolve_report_post'),
    path('recent-comments/', views.get_recent_comments, name='get_recent_comments'),
    path('tags-report/', views.get_posts_by_tag_report, name='get_posts_by_tag_report'),
    path('reported/', views.get_reported_posts, name='get_reported_posts'),
    path('archived/', views.get_archived_posts, name='get_archived_posts'),
    path('active/', views.get_active_posts, name='get_active_posts'),
    path('archive/', views.archive_posts, name='archive_posts'),
    path('restore/', views.restore_posts, name='restore_posts'),
    path('related/', views.get_related_posts, name='get_related_posts'),
    path('popular-tags/', views.get_popular_tags, name='get_popular_tags'),
    path('sorted/', views.get_sorted_posts, name='get_sorted_posts'),
    path('public/', views.get_public_posts, name='get_public_posts'),
    path('archive/<int:post_id>/', views.archive_post, name='archive_post'),
    path('unarchive/<int:post_id>/', views.unarchive_post, name='unarchive_post'),
    path('toggle-visibility/<int:post_id>/', views.toggle_visibility_post, name='toggle_visibility_post'),
    path('add-tags/<int:post_id>/', views.add_tags_to_post, name='add_tags_to_post'),
    path('remove-tags/<int:post_id>/', views.remove_tags_from_post, name='remove_tags_from_post'),
    path('reactions-count/<int:post_id>/', views.get_reactions_count, name='get_reactions_count'),
    path('comments-count/<int:post_id>/', views.get_comments_count, name='get_comments_count'),
    path('shares-count/<int:post_id>/', views.get_shares_count, name='get_shares_count'),
    path('add-attachments/<int:post_id>/', views.add_attachments_to_post, name='add_attachments_to_post'),
    path('remove-attachments/<int:post_id>/', views.remove_attachments_from_post, name='remove_attachments_from_post'),
    path('comments/create/', views.create_comment, name='create_comment'),
    path('comments/<int:comment_id>/', views.get_comment_by_id, name='get_comment_by_id'),
    path('comments/update/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('comments/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comments/delete-with-replies/<int:comment_id>/', views.delete_comment_with_replies, name='delete_comment_with_replies'),
    path('comments/report/<int:comment_id>/', views.report_comment, name='report_comment'),
    path('comments/resolve-report/<int:comment_id>/', views.resolve_report_comment, name='resolve_report_comment'),
    path('comments/', views.get_comments, name='get_comments'),
    path('comments/archive/<int:comment_id>/', views.archive_comment, name='archive_comment'),
    path('comments/unarchive/<int:comment_id>/', views.unarchive_comment, name='unarchive_comment'),
    path('comments/toggle-visibility/<int:comment_id>/', views.toggle_visibility_comment, name='toggle_visibility_comment'),
    path('comments/add-attachments/<int:comment_id>/', views.add_attachments_to_comment, name='add_attachments_to_comment'),
    path('comments/remove-attachments/<int:comment_id>/', views.remove_attachments_from_comment, name='remove_attachments_from_comment'),
    path('comments/by-author/<int:author>/', views.get_comments_by_author, name='get_comments_by_author'),
    path('comments/by-post/<int:post_id>/', views.get_comments_by_post, name='get_comments_by_post'),
]

    

# Funtionalities to be added
# path('posts/delete/all/', delete_all_posts, name='delete_all_posts'),
# path('posts/reactions/<int:post_id>/', get_post_reactions, name='get_post_reactions'),
# path('posts/comments/<int:post_id>/', get_post_comments, name='get_post_comments'),
# path('posts/shares/<int:post_id>/', get_post_shares, name='get_post_shares'),
