from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from activity.models import Category, Attachment, MarketingCampaign, LearningService, Analytics, UserActivity, UserStatistics, Thread, Reaction, Share
from activity.serializers import CategorySerializer, AttachmentSerializer, MarketingCampaignSerializer, LearningServiceSerializer, AnalyticsSerializer, UserActivitySerializer, UserStatisticsSerializer, ThreadSerializer, ReactionSerializer, ShareSerializer
from activity.controllers.activity_controller import ActivityController
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes

# Create your views here.

activity_controller = ActivityController()



# Category views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all categories',
            description='Get all categories',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of categories')}
)
@api_view(['GET'])
def get_categories(request):
    """
    API endpoint that allows all categories to be retrieved.
    """
    if request.method == 'GET':
        categories = activity_controller.get_all_categories()
        return Response(categories, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='category_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific category',
            description='Get a specific category',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Category data')}
)
@api_view(['GET'])
def get_specific_category(request, category_id):
    """
    API endpoint that allows a specific category to be retrieved.
    """
    if request.method == 'GET':
        category = activity_controller.get_category(category_id)
        return Response(category, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new category',
            description='Create a new category',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Category data')}
)
@api_view(['POST'])
def create_category(request):
    """
    API endpoint that allows a new category to be created.
    """
    if request.method == 'POST':
        category = activity_controller.create_category(request.data)
        return Response(category, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='category_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a category',
            description='Update a category',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Category data')}
)
@api_view(['PUT'])
def update_category(request, category_id):
    """
    API endpoint that allows a category to be updated.
    """
    if request.method == 'PUT':
        category = activity_controller.update_category(category_id, request.data)
        return Response(category, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='category_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a category',
            description='Delete a category',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Category deleted')}
)
@api_view(['DELETE'])
def delete_category(request, category_id):
    """
    API endpoint that allows a category to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_category(category_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all categories',
            description='Delete all categories',
            value={
                'name': 'name',
                'description': 'description'
            }
        )
    ],
    request=CategorySerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All categories deleted')}
)
@api_view(['DELETE'])
def delete_all_categories(request):
    """
    API endpoint that allows all categories to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_categories()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Attachment views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all attachments',
            description='Get all attachments',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of attachments')}
)
@api_view(['GET'])
def get_attachments(request):
    """
    API endpoint that allows all attachments to be retrieved.
    """
    if request.method == 'GET':
        attachments = activity_controller.get_all_attachments()
        return Response(attachments, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='attachment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific attachment',
            description='Get a specific attachment',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Attachment data')}
)
@api_view(['GET'])
def get_specific_attachment(request, attachment_id):
    """
    API endpoint that allows a specific attachment to be retrieved.
    """
    if request.method == 'GET':
        attachment = activity_controller.get_attachment(attachment_id)
        return Response(attachment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='attachment_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='file', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='uploaded_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='object_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new attachment',
            description='Create a new attachment',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Attachment data')}
)
@api_view(['POST'])
def create_attachment(request):
    """
    API endpoint that allows a new attachment to be created.
    """
    if request.method == 'POST':
        attachment = activity_controller.create_attachment(request.data)
        return Response(attachment, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='attachment_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='attachment_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='file', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='uploaded_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='object_id', type=int, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an attachment',
            description='Update an attachment',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Attachment data')}
)
@api_view(['PUT'])
def update_attachment(request, attachment_id):
    """
    API endpoint that allows an attachment to be updated.
    """
    if request.method == 'PUT':
        attachment = activity_controller.update_attachment(attachment_id, request.data)
        return Response(attachment, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='attachment_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an attachment',
            description='Delete an attachment',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Attachment deleted')}
)
@api_view(['DELETE'])
def delete_attachment(request, attachment_id):
    """
    API endpoint that allows an attachment to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_attachment(attachment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all attachments',
            description='Delete all attachments',
            value={
                'attachment_type': 'attachment_type',
                'file': 'file',
                'uploaded_at': 'uploaded_at',
                'content_type': 'content_type',
                'object_id': 'object_id'
            }
        )
    ],
    request=AttachmentSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All attachments deleted')}
)
@api_view(['DELETE'])
def delete_all_attachments(request):
    """
    API endpoint that allows all attachments to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_attachments()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# Marketing Campaign views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all marketing campaigns',
            description='Get all marketing campaigns',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of marketing campaigns')}
)
@api_view(['GET'])
def get_marketing_campaigns(request):
    """
    API endpoint that allows all marketing campaigns to be retrieved.
    """
    if request.method == 'GET':
        marketing_campaigns = activity_controller.get_all_marketing_campaigns()
        return Response(marketing_campaigns, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific marketing campaign',
            description='Get a specific marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['GET'])
def get_specific_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a specific marketing campaign to be retrieved.
    """
    if request.method == 'GET':
        marketing_campaign = activity_controller.get_marketing_campaign(marketing_campaign_id)
        return Response(marketing_campaign, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='campaign_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='target_audience', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new marketing campaign',
            description='Create a new marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['POST'])
def create_marketing_campaign(request):
    """
    API endpoint that allows a new marketing campaign to be created.
    """
    if request.method == 'POST':
        marketing_campaign = activity_controller.create_marketing_campaign(request.data)
        return Response(marketing_campaign, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='campaign_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='target_audience', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a marketing campaign',
            description='Update a marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['PUT'])
def update_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a marketing campaign to be updated.
    """
    if request.method == 'PUT':
        marketing_campaign = activity_controller.update_marketing_campaign(marketing_campaign_id, request.data)
        return Response(marketing_campaign, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a marketing campaign',
            description='Delete a marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign deleted')}
)
@api_view(['DELETE'])
def delete_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a marketing campaign to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_marketing_campaign(marketing_campaign_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all marketing campaigns',
            description='Delete all marketing campaigns',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All marketing campaigns deleted')}
)
@api_view(['DELETE'])
def delete_all_marketing_campaigns(request):
    """
    API endpoint that allows all marketing campaigns to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_marketing_campaigns()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# Learning Service views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all learning services',
            description='Get all learning services',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of learning services')}
)
@api_view(['GET'])
def get_learning_services(request):
    """
    API endpoint that allows all learning services to be retrieved.
    """
    if request.method == 'GET':
        learning_services = activity_controller.get_all_learning_services()
        return Response(learning_services, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='learning_service_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific learning service',
            description='Get a specific learning service',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Learning service data')}
)
@api_view(['GET'])
def get_specific_learning_service(request, learning_service_id):
    """
    API endpoint that allows a specific learning service to be retrieved.
    """
    if request.method == 'GET':
        learning_service = activity_controller.get_learning_service(learning_service_id)
        return Response(learning_service, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='service_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new learning service',
            description='Create a new learning service',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Learning service data')}
)
@api_view(['POST'])
def create_learning_service(request):
    """
    API endpoint that allows a new learning service to be created.
    """
    if request.method == 'POST':
        learning_service = activity_controller.create_learning_service(request.data)
        return Response(learning_service, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='learning_service_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='service_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='description', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a learning service',
            description='Update a learning service',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Learning service data')}
)
@api_view(['PUT'])
def update_learning_service(request, learning_service_id):
    """
    API endpoint that allows a learning service to be updated.
    """
    if request.method == 'PUT':
        learning_service = activity_controller.update_learning_service(learning_service_id, request.data)
        return Response(learning_service, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@extend_schema(
    parameters=[
        OpenApiParameter(name='learning_service_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a learning service',
            description='Delete a learning service',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Learning service deleted')}
)
@api_view(['DELETE'])
def delete_learning_service(request, learning_service_id):
    """
    API endpoint that allows a learning service to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_learning_service(learning_service_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all learning services',
            description='Delete all learning services',
            value={
                'service_name': 'service_name',
                'description': 'description',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=LearningServiceSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All learning services deleted')}
)
@api_view(['DELETE'])
def delete_all_learning_services(request):
    """
    API endpoint that allows all learning services to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_learning_services()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
      

# Analytics views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all analytics',
            description='Get all analytics',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of analytics')}
)
@api_view(['GET'])
def get_analytics(request):
    """
    API endpoint that allows all analytics to be retrieved.
    """
    if request.method == 'GET':
        analytics = activity_controller.get_all_analytics()
        return Response(analytics, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='analytic_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific analytic',
            description='Get a specific analytic',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Analytic data')}
)
@api_view(['GET'])
def get_specific_analytic(request, analytic_id):
    """
    API endpoint that allows a specific analytic to be retrieved.
    """
    if request.method == 'GET':
        analytic = activity_controller.get_analytic(analytic_id)
        return Response(analytic, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='activity_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='engagement_rate', type=float, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='trending_topics', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new analytic',
            description='Create a new analytic',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Analytic data')}
)
@api_view(['POST'])
def create_analytic(request):
    """
    API endpoint that allows a new analytic to be created.
    """
    if request.method == 'POST':
        analytic = activity_controller.create_analytic(request.data)
        return Response(analytic, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='analytic_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='activity_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='engagement_rate', type=float, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='trending_topics', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update an analytic',
            description='Update an analytic',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Analytic data')}
)
@api_view(['PUT'])
def update_analytic(request, analytic_id):
    """
    API endpoint that allows an analytic to be updated.
    """
    if request.method == 'PUT':
        analytic = activity_controller.update_analytic(analytic_id, request.data)
        return Response(analytic, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='analytic_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete an analytic',
            description='Delete an analytic',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Analytic deleted')}
)
@api_view(['DELETE'])
def delete_analytic(request, analytic_id):
    """
    API endpoint that allows an analytic to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_analytic(analytic_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all analytics',
            description='Delete all analytics',
            value={
                'activity_type': 'activity_type',
                'engagement_rate': 'engagement_rate',
                'trending_topics': 'trending_topics',
                'categories': 'categories'
            }
        )
    ],
    request=AnalyticsSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All analytics deleted')}
)
@api_view(['DELETE'])
def delete_all_analytics(request):
    """
    API endpoint that allows all analytics to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_analytics()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# User Activity views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all user activities',
            description='Get all user activities',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of user activities')}
)
@api_view(['GET'])
def get_user_activities(request):
    """
    API endpoint that allows all user activities to be retrieved.
    """
    if request.method == 'GET':
        user_activities = activity_controller.get_all_user_activities()
        return Response(user_activities, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_activity_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific user activity',
            description='Get a specific user activity',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User activity data')}
)
@api_view(['GET'])
def get_specific_user_activity(request, user_activity_id):
    """
    API endpoint that allows a specific user activity to be retrieved.
    """
    if request.method == 'GET':
        user_activity = activity_controller.get_user_activity(user_activity_id)
        return Response(user_activity, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='activity_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='details', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new user activity',
            description='Create a new user activity',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User activity data')}
)
@api_view(['POST'])
def create_user_activity(request):
    """
    API endpoint that allows a new user activity to be created.
    """
    if request.method == 'POST':
        user_activity = activity_controller.create_user_activity(request.data)
        return Response(user_activity, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_activity_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='activity_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='details', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a user activity',
            description='Update a user activity',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User activity data')}
)
@api_view(['PUT'])
def update_user_activity(request, user_activity_id):
    """
    API endpoint that allows a user activity to be updated.
    """
    if request.method == 'PUT':
        user_activity = activity_controller.update_user_activity(user_activity_id, request.data)
        return Response(user_activity, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_activity_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a user activity',
            description='Delete a user activity',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User activity deleted')}
)
@api_view(['DELETE'])
def delete_user_activity(request, user_activity_id):
    """
    API endpoint that allows a user activity to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_user_activity(user_activity_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all user activities',
            description='Delete all user activities',
            value={
                'user': 'user',
                'activity_type': 'activity_type',
                'timestamp': 'timestamp',
                'details': 'details',
                'categories': 'categories'
            }
        )
    ],
    request=UserActivitySerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All user activities deleted')}
)
@api_view(['DELETE'])
def delete_all_user_activities(request):
    """
    API endpoint that allows all user activities to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_user_activities()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# User Statistics views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all user statistics',
            description='Get all user statistics',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of user statistics')}
)
@api_view(['GET'])
def get_user_statistics(request):
    """
    API endpoint that allows all user statistics to be retrieved.
    """
    if request.method == 'GET':
        user_statistics = activity_controller.get_all_user_statistics()
        return Response(user_statistics, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_statistic_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific user statistic',
            description='Get a specific user statistic',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User statistic data')}
)
@api_view(['GET'])
def get_specific_user_statistic(request, user_statistic_id):
    """
    API endpoint that allows a specific user statistic to be retrieved.
    """
    if request.method == 'GET':
        user_statistic = activity_controller.get_user_statistic(user_statistic_id)
        return Response(user_statistic, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='connections_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='posts_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='engagement_rate', type=float, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new user statistic',
            description='Create a new user statistic',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User statistic data')}
)
@api_view(['POST'])
def create_user_statistic(request):
    """
    API endpoint that allows a new user statistic to be created.
    """
    if request.method == 'POST':
        user_statistic = activity_controller.create_user_statistic(request.data)
        return Response(user_statistic, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_statistic_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='connections_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='posts_count', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='engagement_rate', type=float, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a user statistic',
            description='Update a user statistic',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User statistic data')}
)
@api_view(['PUT'])
def update_user_statistic(request, user_statistic_id):
    """
    API endpoint that allows a user statistic to be updated.
    """
    if request.method == 'PUT':
        user_statistic = activity_controller.update_user_statistic(user_statistic_id, request.data)
        return Response(user_statistic, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user_statistic_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a user statistic',
            description='Delete a user statistic',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='User statistic deleted')}
)
@api_view(['DELETE'])
def delete_user_statistic(request, user_statistic_id):
    """
    API endpoint that allows a user statistic to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_user_statistic(user_statistic_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all user statistics',
            description='Delete all user statistics',
            value={
                'user': 'user',
                'connections_count': 'connections_count',
                'posts_count': 'posts_count',
                'engagement_rate': 'engagement_rate'
            }
        )
    ],
    request=UserStatisticsSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All user statistics deleted')}
)
@api_view(['DELETE'])
def delete_all_user_statistics(request):
    """
    API endpoint that allows all user statistics to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_user_statistics()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# Marketing Campaign views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all marketing campaigns',
            description='Get all marketing campaigns',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of marketing campaigns')}
)
@api_view(['GET'])
def get_marketing_campaigns(request):
    """
    API endpoint that allows all marketing campaigns to be retrieved.
    """
    if request.method == 'GET':
        marketing_campaigns = activity_controller.get_all_marketing_campaigns()
        return Response(marketing_campaigns, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific marketing campaign',
            description='Get a specific marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['GET'])
def get_specific_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a specific marketing campaign to be retrieved.
    """
    if request.method == 'GET':
        marketing_campaign = activity_controller.get_marketing_campaign(marketing_campaign_id)
        return Response(marketing_campaign, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='campaign_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='target_audience', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new marketing campaign',
            description='Create a new marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['POST'])
def create_marketing_campaign(request):
    """
    API endpoint that allows a new marketing campaign to be created.
    """
    if request.method == 'POST':
        marketing_campaign = activity_controller.create_marketing_campaign(request.data)
        return Response(marketing_campaign, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='campaign_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='start_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='end_date', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='target_audience', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a marketing campaign',
            description='Update a marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign data')}
)
@api_view(['PUT'])
def update_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a marketing campaign to be updated.
    """
    if request.method == 'PUT':
        marketing_campaign = activity_controller.update_marketing_campaign(marketing_campaign_id, request.data)
        return Response(marketing_campaign, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='marketing_campaign_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a marketing campaign',
            description='Delete a marketing campaign',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Marketing campaign deleted')}
)
@api_view(['DELETE'])
def delete_marketing_campaign(request, marketing_campaign_id):
    """
    API endpoint that allows a marketing campaign to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_marketing_campaign(marketing_campaign_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all marketing campaigns',
            description='Delete all marketing campaigns',
            value={
                'campaign_name': 'campaign_name',
                'start_date': 'start_date',
                'end_date': 'end_date',
                'target_audience': 'target_audience',
                'categories': 'categories',
                'attachments': 'attachments'
            }
        )
    ],
    request=MarketingCampaignSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All marketing campaigns deleted')}
)
@api_view(['DELETE'])
def delete_all_marketing_campaigns(request):
    """
    API endpoint that allows all marketing campaigns to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_marketing_campaigns()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Thread views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all threads',
            description='Get all threads',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of threads')}
)
@api_view(['GET'])
def get_threads(request):
    """
    API endpoint that allows all threads to be retrieved.
    """
    if request.method == 'GET':
        threads = activity_controller.get_all_threads()
        return Response(threads, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='thread_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific thread',
            description='Get a specific thread',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Thread data')}
)
@api_view(['GET'])
def get_specific_thread(request, thread_id):
    """
    API endpoint that allows a specific thread to be retrieved.
    """
    if request.method == 'GET':
        thread = activity_controller.get_thread(thread_id)
        return Response(thread, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='thread_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='thread_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='messages', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),

    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new thread',
            description='Create a new thread',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Thread data')}
)
@api_view(['POST'])
def create_thread(request):
    """
    API endpoint that allows a new thread to be created.
    """
    if request.method == 'POST':
        thread = activity_controller.create_thread(request.data)
        return Response(thread, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='thread_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='thread_name', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='thread_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='members', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='messages', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='attachments', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a thread',
            description='Update a thread',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Thread data')}
)
@api_view(['PUT'])
def update_thread(request, thread_id):
    """
    API endpoint that allows a thread to be updated.
    """
    if request.method == 'PUT':
        thread = activity_controller.update_thread(thread_id, request.data)
        return Response(thread, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='thread_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a thread',
            description='Delete a thread',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Thread deleted')}
)
@api_view(['DELETE'])
def delete_thread(request, thread_id):
    """
    API endpoint that allows a thread to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_thread(thread_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all threads',
            description='Delete all threads',
            value={
                'thread_name': 'thread_name',
                'thread_type': 'thread_type',
                'members': 'members',
                'messages': 'messages',
                'attachments': 'attachments',
                'categories': 'categories'
            }
        )
    ],
    request=ThreadSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All threads deleted')}
)
@api_view(['DELETE'])
def delete_all_threads(request):
    """
    API endpoint that allows all threads to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_threads()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# Reaction views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all reactions',
            description='Get all reactions',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of reactions')}
)
@api_view(['GET'])
def get_reactions(request):
    """
    API endpoint that allows all reactions to be retrieved.
    """
    if request.method == 'GET':
        reactions = activity_controller.get_all_reactions()
        return Response(reactions, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='reaction_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific reaction',
            description='Get a specific reaction',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Reaction data')}
)
@api_view(['GET'])
def get_specific_reaction(request, reaction_id):
    """
    API endpoint that allows a specific reaction to be retrieved.
    """
    if request.method == 'GET':
        reaction = activity_controller.get_reaction(reaction_id)
        return Response(reaction, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='reaction_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new reaction',
            description='Create a new reaction',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Reaction data')}
)
@api_view(['POST'])
def create_reaction(request):
    """
    API endpoint that allows a new reaction to be created.
    """
    if request.method == 'POST':
        reaction = activity_controller.create_reaction(request.data)
        return Response(reaction, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='reaction_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='reaction_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='message', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='timestamp', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='categories', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a reaction',
            description='Update a reaction',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Reaction data')}
)
@api_view(['PUT'])
def update_reaction(request, reaction_id):
    """
    API endpoint that allows a reaction to be updated.
    """
    if request.method == 'PUT':
        reaction = activity_controller.update_reaction(reaction_id, request.data)
        return Response(reaction, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='reaction_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a reaction',
            description='Delete a reaction',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Reaction deleted')}
)
@api_view(['DELETE'])
def delete_reaction(request, reaction_id):
    """
    API endpoint that allows a reaction to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_reaction(reaction_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all reactions',
            description='Delete all reactions',
            value={
                'reaction_type': 'reaction_type',
                'user': 'user',
                'message': 'message',
                'timestamp': 'timestamp',
                'categories': 'categories'
            }
        )
    ],
    request=ReactionSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All reactions deleted')}
)
@api_view(['DELETE'])
def delete_all_reactions(request):
    """
    API endpoint that allows all reactions to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_reactions()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    

# Share Views
@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get all shares',
            description='Get all shares',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='List of shares')}
)
@api_view(['GET'])
def get_shares(request):
    """
    API endpoint that allows all shares to be retrieved.
    """
    if request.method == 'GET':
        shares = activity_controller.get_all_shares()
        return Response(shares, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='share_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Get a specific share',
            description='Get a specific share',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Share data')}
)
@api_view(['GET'])
def get_specific_share(request, share_id):
    """
    API endpoint that allows a specific share to be retrieved.
    """
    if request.method == 'GET':
        share = activity_controller.get_share(share_id)
        return Response(share, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shared_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='object_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_object', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shared_to', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Create a new share',
            description='Create a new share',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={201: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Share data')}
)
@api_view(['POST'])
def create_share(request):
    """
    API endpoint that allows a new share to be created.
    """
    if request.method == 'POST':
        share = activity_controller.create_share(request.data)
        return Response(share, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='share_id', type=int, location=OpenApiParameter.PATH, required=True),
        OpenApiParameter(name='user', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shared_at', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_type', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='object_id', type=int, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='content_object', type=str, location=OpenApiParameter.QUERY, required=True),
        OpenApiParameter(name='shared_to', type=str, location=OpenApiParameter.QUERY, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Update a share',
            description='Update a share',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={200: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Share data')}
)
@api_view(['PUT'])
def update_share(request, share_id):
    """
    API endpoint that allows a share to be updated.
    """
    if request.method == 'PUT':
        share = activity_controller.update_share(share_id, request.data)
        return Response(share, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[
        OpenApiParameter(name='share_id', type=int, location=OpenApiParameter.PATH, required=True),
    ],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete a share',
            description='Delete a share',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='Share deleted')}
)
@api_view(['DELETE'])
def delete_share(request, share_id):
    """
    API endpoint that allows a share to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_share(share_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

@extend_schema(
    parameters=[],
    examples=[
        OpenApiExample(
            'Example 1',
            summary='Delete all shares',
            description='Delete all shares',
            value={
                'user': 'user',
                'shared_at': 'shared_at',
                'content_type': 'content_type',
                'object_id': 'object_id',
                'content_object': 'content_object',
                'shared_to': 'shared_to'
            }
        )
    ],
    request=ShareSerializer,
    responses={204: OpenApiResponse(response=OpenApiTypes.OBJECT, description='All shares deleted')}
)
@api_view(['DELETE'])
def delete_all_shares(request):
    """
    API endpoint that allows all shares to be deleted.
    """
    if request.method == 'DELETE':
        activity_controller.delete_all_shares()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    


# Generare url patterns for all the views above following this format.
# the functions SHOULD be imported from the views.function
# urlpatterns = [
#     path('', views.get_companies, name='get_companies'),
#     path('companies/<int:company_id>/', views.get_specific_company, name='get_specific_company'),
#     path('companies/create/', views.create_company, name='create_company'),
#     path('companies/update/<int:company_id>/', views.update_company, name='update_company'),
#     path('companies/delete/<int:company_id>/', views.delete_company, name='delete_company'),
#     path('companies/delete/all/', views.delete_all_companies, name='delete_all_companies'),
#     path('companies/updates/<int:company_id>/', views.get_company_updates, name='get_company_updates'),
#     path('<int:update_id>/', views.get_specific_company_update, name='get_specific_company_update'),
#     path('companies/updates/create/<int:company_id>/', views.create_company_update, name='create_company_update'),
#     path('companies/updates/update/<int:company_id>/<int:update_id>/', views.update_company_update, name='update_company_update'),
#     path('companies/updates/delete/<int:update_id>/', views.delete_company_update, name='delete_company_update'),
#     # path('events/', views.get_events),
#     # path('events/<int:event_id>/', views.get_event),
#     # path('events/create/', views.create_event),
# ]
    


