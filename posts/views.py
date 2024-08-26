from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from posts.models import Post, Comment
from posts.serializers import PostSerializer, CommentSerializer
from posts.controllers.posts_controller import PostController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

post_controller = PostController()

RESPONSE_VALUE = {
                'author': 'author',
                'group': 'group',
                'content': 'content',
                'attachments': 'attachments',
                'visibility': 'visibility',
                'categories': 'categories',
                'created_at': 'created_at',
                'updated_at': 'updated_at',
                'reactions': 'reactions',
                'comments': 'comments',
                'shares': 'shares',
                'pinned': 'pinned',
                'archived_at': 'archived_at',
                'reported': 'reported',
                'tags': 'tags',
                'slug': 'slug',
                'deleted': 'deleted'
            }

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all posts',
            description='Get all posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_all_posts(request):
    """
    API endpoint that allows all posts to be retrieved.
    """
    if request.method == 'GET':
        posts = post_controller.get_all_posts()
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific post',
            description='Get a specific post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['GET'])
def get_specific_post(request, post_id):
    """
    API endpoint that allows a specific post to be retrieved.
    """
    if request.method == 'GET':
        post = post_controller.get_post_by_id(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# create_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='group', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='visibility', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='reactions', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='comments', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='shares', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='pinned', type=bool, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='archived_at', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='reported', type=bool, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='slug', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='deleted', type=bool, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a post',
            description='Create a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def create_post(request):
    """
    API endpoint that allows a new post to be created.
    """
    if request.method == 'POST':
        post_data = request.data
        post = post_controller.create_post(post_data)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='group', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='visibility', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='reactions', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='comments', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='shares', type=int, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='pinned', type=bool, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='archived_at', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='reported', type=bool, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='tags', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='slug', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='deleted', type=bool, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a post',
            description='Update a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['PUT'])
def update_post(request, post_id):
    """
    API endpoint that allows a specific post to be updated.
    """
    if request.method == 'PUT':
        post_data = request.data
        post = post_controller.update_post(post_id, post_data)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get posts by author',
            description='Get posts by author',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_posts_by_author(request):
    """
    API endpoint that allows all posts by a specific author to be retrieved.
    """
    if request.method == 'GET':
        author = request.GET.get('author')
        posts = post_controller.get_posts_by_author(author)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='group', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get posts by group',
            description='Get posts by group',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_posts_by_group(request):
    """
    API endpoint that allows all posts by a specific group to be retrieved.
    """
    if request.method == 'GET':
        group = request.GET.get('group')
        posts = post_controller.get_posts_by_group(group)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='tag_name', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get posts by tag',
            description='Get posts by tag',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_posts_by_tag(request):
    """
    API endpoint that allows all posts by a specific tag to be retrieved.
    """
    if request.method == 'GET':
        tag_name = request.GET.get('tag_name')
        posts = post_controller.get_posts_by_tag(tag_name)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a post',
            description='Delete a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['DELETE'])
def delete_post(request, post_id):
    """
    API endpoint that allows a specific post to be deleted.
    """
    if request.method == 'DELETE':
        post = post_controller.delete_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Pin a post',
            description='Pin a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def pin_post(request, post_id):
    """
    API endpoint that allows a specific post to be pinned.
    """
    if request.method == 'POST':
        post = post_controller.pin_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Unpin a post',
            description='Unpin a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def unpin_post(request, post_id):
    """
    API endpoint that allows a specific post to be unpinned.
    """
    if request.method == 'POST':
        post = post_controller.unpin_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Report a post',
            description='Report a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def report_post(request, post_id):
    """
    API endpoint that allows a specific post to be reported.
    """
    if request.method == 'POST':
        post = post_controller.report_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Resolve report for a post',
            description='Resolve report for a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def resolve_report_post(request, post_id):
    """
    API endpoint that allows a specific post report to be resolved.
    """
    if request.method == 'POST':
        post = post_controller.resolve_report_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='limit', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get recent comments',
            description='Get recent comments',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of comments')}
)
@api_view(['GET'])
def get_recent_comments(request):
    """
    API endpoint that allows recent comments to be retrieved.
    """
    if request.method == 'GET':
        limit = request.GET.get('limit')
        comments = post_controller.get_recent_comments(limit)
        return Response(comments, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get posts by tag report',
            description='Get posts by tag report',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_posts_by_tag_report(request):
    """
    API endpoint that allows a report for all posts by tag to be retrieved.
    """
    if request.method == 'GET':
        report = post_controller.get_posts_by_tag_report()
        return Response(report, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all reported posts',
            description='Get all reported posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_reported_posts(request):
    """
    API endpoint that allows all reported posts to be retrieved.
    """
    if request.method == 'GET':
        posts = post_controller.get_reported_posts()
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    

# archieved posts
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get archived posts',
            description='Get archived posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_archived_posts(request):
    """
    API endpoint that allows all archived posts to be retrieved.
    """
    if request.method == 'GET':
        posts = post_controller.get_archived_posts()
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# active posts
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get active posts',
            description='Get active posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_active_posts(request):
    """
    API endpoint that allows all active posts to be retrieved.
    """
    if request.method == 'GET':
        posts = post_controller.get_active_posts()
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# archive_posts
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Archive posts',
            description='Archive posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['POST'])
def archive_posts(request):
    """
    API endpoint that allows multiple posts to be archived.
    """
    if request.method == 'POST':
        post_ids = request.data.get('post_ids')
        posts = post_controller.archive_posts(post_ids)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# restore_posts
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Restore posts',
            description='Restore posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['POST'])
def restore_posts(request):
    """
    API endpoint that allows multiple posts to be restored.
    """
    if request.method == 'POST':
        post_ids = request.data.get('post_ids')
        posts = post_controller.restore_posts(post_ids)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_related_posts
@extend_schema(
    parameters=[
        OpenApiParameter(name='post', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get related posts',
            description='Get related posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_related_posts(request):
    """
    API endpoint that allows related posts to be retrieved.
    """
    if request.method == 'GET':
        post = request.GET.get('post')
        posts = post_controller.get_related_posts(post)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_popular_tags
@extend_schema(
    parameters=[
        OpenApiParameter(name='limit', type=int, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get popular tags',
            description='Get popular tags',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of tags')}
)
@api_view(['GET'])
def get_popular_tags(request):
    """
    API endpoint that allows popular tags to be retrieved.
    """
    if request.method == 'GET':
        limit = request.GET.get('limit')
        tags = post_controller.get_popular_tags(limit)
        return Response(tags, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_sorted_posts
@extend_schema(
    parameters=[
        OpenApiParameter(name='field_name', type=str, location=OpenApiParameter.QUERY, required=False),
        OpenApiParameter(name='descending', type=bool, location=OpenApiParameter.QUERY, required=False),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get sorted posts',
            description='Get sorted posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_sorted_posts(request):
    """
    API endpoint that allows sorted posts to be retrieved.
    """
    if request.method == 'GET':
        field_name = request.GET.get('field_name')
        descending = request.GET.get('descending')
        posts = post_controller.get_sorted_posts(field_name, descending)
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_public_posts
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get public posts',
            description='Get public posts',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of posts')}
)
@api_view(['GET'])
def get_public_posts(request):
    """
    API endpoint that allows all public posts to be retrieved.
    """
    if request.method == 'GET':
        posts = post_controller.get_public_posts()
        return Response(posts, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# archive_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Archive a post',
            description='Archive a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def archive_post(request, post_id):
    """
    API endpoint that allows a specific post to be archived.
    """
    if request.method == 'POST':
        post = post_controller.archive_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# unarchive_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Unarchive a post',
            description='Unarchive a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def unarchive_post(request, post_id):
    """
    API endpoint that allows a specific post to be unarchived.
    """
    if request.method == 'POST':
        post = post_controller.unarchive_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# toggle_visibility_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Toggle visibility for a post',
            description='Toggle visibility for a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def toggle_visibility_post(request, post_id):
    """
    API endpoint that allows visibility for a specific post to be toggled.
    """
    if request.method == 'POST':
        post = post_controller.toggle_visibility_post(post_id)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# add_tags_to_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='tag_names', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add tags to a post',
            description='Add tags to a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def add_tags_to_post(request, post_id):
    """
    API endpoint that allows tags to be added to a specific post.
    """
    if request.method == 'POST':
        tag_names = request.data.get('tag_names')
        post = post_controller.add_tags_to_post(post_id, tag_names)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# remove_tags_from_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='tag_names', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Remove tags from a post',
            description='Remove tags from a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def remove_tags_from_post(request, post_id):
    """
    API endpoint that allows tags to be removed from a specific post.
    """
    if request.method == 'POST':
        tag_names = request.data.get('tag_names')
        post = post_controller.remove_tags_from_post(post_id, tag_names)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_reactions_count
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get reactions count for a post',
            description='Get reactions count for a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Reactions count')}
)
@api_view(['GET'])
def get_reactions_count(request, post_id):
    """
    API endpoint that allows reactions count for a specific post to be retrieved.
    """
    if request.method == 'GET':
        count = post_controller.get_reactions_count(post_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)



# get_comments_count
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get comments count for a post',
            description='Get comments count for a post',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comments count')}
)
@api_view(['GET'])
def get_comments_count(request, post_id):
    """
    API endpoint that allows comments count for a specific post to be retrieved.
    """
    if request.method == 'GET':
        count = post_controller.get_comments_count(post_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_shares_count
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get shares count for a post',
            description='Get shares count for a post',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Shares count')}
)
@api_view(['GET'])
def get_shares_count(request, post_id):
    """
    API endpoint that allows shares count for a specific post to be retrieved.
    """
    if request.method == 'GET':
        count = post_controller.get_shares_count(post_id)
        return Response(count, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# add_attachments_to_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='attachment_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add attachments to a post',
            description='Add attachments to a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def add_attachments_to_post(request, post_id):
    """
    API endpoint that allows attachments to be added to a specific post.
    """
    if request.method == 'POST':
        attachment_ids = request.data.get('attachment_ids')
        post = post_controller.add_attachments_to_post(post_id, attachment_ids)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# remove_attachments_from_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='attachment_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Remove attachments from a post',
            description='Remove attachments from a post',
            value=RESPONSE_VALUE
        )
    ],
    request=PostSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Post data')}
)
@api_view(['POST'])
def remove_attachments_from_post(request, post_id):
    """
    API endpoint that allows attachments to be removed from a specific post.
    """
    if request.method == 'POST':
        attachment_ids = request.data.get('attachment_ids')
        post = post_controller.remove_attachments_from_post(post_id, attachment_ids)
        return Response(post, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# create_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='content_type', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='object_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='post', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='visibility', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='parent_comment', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new comment',
            description='Create a new comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def create_comment(request):
    """
    API endpoint that allows a new comment to be created.
    """
    if request.method == 'POST':
        comment = post_controller.create_comment(request.data)
        return Response(comment, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_comment_by_id
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific comment',
            description='Get a specific comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['GET'])
def get_comment_by_id(request, comment_id):
    """
    API endpoint that allows a specific comment to be retrieved.
    """
    if request.method == 'GET':
        comment = post_controller.get_comment_by_id(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# update_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='content', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='visibility', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a comment',
            description='Update a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['PUT'])
def update_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to be updated.
    """
    if request.method == 'PUT':
        comment = post_controller.update_comment(comment_id, request.data)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# delete_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a comment',
            description='Delete a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['DELETE'])
def delete_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to be deleted.
    """
    if request.method == 'DELETE':
        comment = post_controller.delete_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# delete_comment_with_replies
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a comment with replies',
            description='Delete a comment with replies',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['DELETE'])
def delete_comment_with_replies(request, comment_id):
    """
    API endpoint that allows a specific comment and its replies to be deleted.
    """
    if request.method == 'DELETE':
        comment = post_controller.delete_comment_with_replies(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# report_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Report a comment',
            description='Report a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def report_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to be reported.
    """
    if request.method == 'POST':
        comment = post_controller.report_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# resolve_report_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Resolve report for a comment',
            description='Resolve report for a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def resolve_report_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to have its report resolved.
    """
    if request.method == 'POST':
        comment = post_controller.resolve_report_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_comments
@extend_schema(
    parameters=[
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all comments',
            description='Get all comments',
            value=RESPONSE_VALUE
        )
    ],

    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comments data')}
)
@api_view(['GET'])
def get_comments(request):
    """
    API endpoint that allows all comments to be retrieved.
    """
    if request.method == 'GET':
        comments = post_controller.get_comments()
        return Response(comments, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# archive_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Archive a comment',
            description='Archive a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def archive_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to be archived.
    """
    if request.method == 'POST':
        comment = post_controller.archive_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# unarchive_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Unarchive a comment',
            description='Unarchive a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def unarchive_comment(request, comment_id):
    """
    API endpoint that allows a specific comment to be unarchived.
    """
    if request.method == 'POST':
        comment = post_controller.unarchive_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# toggle_visibility_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Toggle visibility for a comment',
            description='Toggle visibility for a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def toggle_visibility_comment(request, comment_id):
    """
    API endpoint that allows visibility for a specific comment to be toggled.
    """
    if request.method == 'POST':
        comment = post_controller.toggle_visibility_comment(comment_id)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# add_attachments_to_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='attachment_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Add attachments to a comment',
            description='Add attachments to a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def add_attachments_to_comment(request, comment_id):
    """
    API endpoint that allows attachments to be added to a specific comment.
    """
    if request.method == 'POST':
        attachment_ids = request.data.get('attachment_ids')
        comment = post_controller.add_attachments_to_comment(comment_id, attachment_ids)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# remove_attachments_from_comment
@extend_schema(
    parameters=[
        OpenApiParameter(name='comment_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='attachment_ids', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Remove attachments from a comment',
            description='Remove attachments from a comment',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comment data')}
)
@api_view(['POST'])
def remove_attachments_from_comment(request, comment_id):
    """
    API endpoint that allows attachments to be removed from a specific comment.
    """
    if request.method == 'POST':
        attachment_ids = request.data.get('attachment_ids')
        comment = post_controller.remove_attachments_from_comment(comment_id, attachment_ids)
        return Response(comment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_comments_by_author
@extend_schema(
    parameters=[
        OpenApiParameter(name='author', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get comments by author',
            description='Get comments by author',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comments data')}
)
@api_view(['GET'])
def get_comments_by_author(request, author):
    """
    API endpoint that allows comments by a specific author to be retrieved.
    """
    if request.method == 'GET':
        comments = post_controller.get_comments_by_author(author)
        return Response(comments, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# get_comments_by_post
@extend_schema(
    parameters=[
        OpenApiParameter(name='post_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get comments by post',
            description='Get comments by post',
            value=RESPONSE_VALUE
        )
    ],
    request=CommentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Comments data')}
)
@api_view(['GET'])
def get_comments_by_post(request, post_id):
    """
    API endpoint that allows comments by a specific post to be retrieved.
    """
    if request.method == 'GET':
        comments = post_controller.get_comments_by_post(post_id)
        return Response(comments, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

