from posts.models import Post, Comment
from activity.models import Reaction, Share, Attachment
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from taggit.models import Tag

class PostManagementController:
    def __init__(self):
        pass

    def create_post(self, author, content, group=None, visibility='public', categories=None, tags=None):
        post = Post.objects.create(
            author=author,
            content=content,
            group=group,
            visibility=visibility,
        )
        if categories:
            post.categories.set(categories)
        if tags:
            post.tags.add(*tags)
        return post

    def update_post(self, post_id, content=None, visibility=None, categories=None, tags=None):
        post = Post.objects.get(id=post_id)
        if content is not None:
            post.content = content
        if visibility is not None:
            post.visibility = visibility
        if categories:
            post.categories.set(categories)
        if tags:
            post.tags.set(*tags)
        post.save()
        return post

    def delete_post(self, post_id):
        post = Post.objects.get(id=post_id)
        post.delete()
        return True

    def create_comment(self, post, author, content, visibility='public', parent_comment=None):
        comment = Comment.objects.create(
            post=post,
            author=author,
            content=content,
            visibility=visibility,
            parent_comment=parent_comment,
        )
        return comment

    def update_comment(self, comment_id, content=None, visibility=None):
        comment = Comment.objects.get(id=comment_id)
        if content is not None:
            comment.content = content
        if visibility is not None:
            comment.visibility = visibility
        comment.save()
        return comment

    def delete_comment(self, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return True

    def like_post(self, post, user):
        post.likes.add(user)
        return True

    def unlike_post(self, post, user):
        post.likes.remove(user)
        return True

    def react_to_post(self, post_id, reaction_type, user):
        post = Post.objects.get(id=post_id)
        reaction, created = Reaction.objects.get_or_create(
            post=post,
            user=user,
            type=reaction_type,
        )
        return reaction

    def share_post(self, post_id, user, message=''):
        post = Post.objects.get(id=post_id)
        share = Share.objects.create(
            content_object=post,
            user=user,
            message=message,
        )
        return share

    def get_post_reactions(self, post_id):
        post = Post.objects.get(id=post_id)
        return post.reactions.all()

    def get_post_comments(self, post_id):
        post = Post.objects.get(id=post_id)
        return post.comments.all()

    def get_post_shares(self, post_id):
        post = Post.objects.get(id=post_id)
        return post.shares.all()

    def get_post_attachments(self, post_id):
        post = Post.objects.get(id=post_id)
        return post.attachments.all()

    def get_post_tags(self, post_id):
        post = Post.objects.get(id=post_id)
        return post.tags.all()
