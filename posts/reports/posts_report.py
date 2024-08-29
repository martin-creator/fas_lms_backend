from django.db.models import Count, Q, Sum, Avg, F, ExpressionWrapper, fields
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.querying.posts_querysets import PostQuerySet, CommentQuerySet


class PostReport:
    @staticmethod
    def get_post_report(post):
        """
        Get a report for a specific post.
        """
        post_data = PostSerializer(post).data
        post_comments = Comment.objects.filter(post=post)
        post_data['comments'] = CommentSerializer(post_comments, many=True).data

        # return json data

        json_data = {
            'post': post_data,
            'comments': post_data['comments']
        }

        return json_data

    @staticmethod
    def get_author_report(author):
        """
        Get a report for a specific author.
        """
        author_data = {}
        author_data['posts'] = PostQuerySet.get_posts_by_author(author).count()
        author_data['comments'] = CommentQuerySet.get_comments_by_author(author).count()

        return author_data

    @staticmethod
    def get_comments_report():
        """
        Get a report for all comments.
        """
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_report():
        """
        Get a report for all posts.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_by_author_report():
        """
        Get a report for all posts by author.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_by_group_report():
        """
        Get a report for all posts by group.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_by_tag_report():
        """
        Get a report for all posts by tag.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_by_reaction_report():
        """
        Get a report for all posts by reaction.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    
    @staticmethod
    def get_posts_by_comment_report():
        """
        Get a report for all posts by comment.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data
    




