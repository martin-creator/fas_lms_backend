# utils/pagination.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(queryset, page_number, page_size):
    """
    Paginate a queryset.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.

    Returns:
    - Paginated queryset for the requested page.
    - Metadata: Total number of pages, total count of items, and current page number.
    """
    paginator = Paginator(queryset, page_size)

    try:
        paginated_queryset = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer, deliver first page.
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        paginated_queryset = paginator.page(paginator.num_pages)

    return {
        'data': paginated_queryset.object_list,
        'page_number': paginated_queryset.number,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count
    }

def get_paginated_response(queryset, page_number, page_size):
    """
    Get paginated response.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.

    Returns:
    - Paginated queryset for the requested page wrapped in a response object.
    """
    paginated_data = paginate_queryset(queryset, page_number, page_size)
    
    return {
        'results': paginated_data['data'],
        'page': paginated_data['page_number'],
        'total_pages': paginated_data['total_pages'],
        'count': paginated_data['total_items']
    }

def execute_paged_query(query, page_number, page_size):
    """
    Execute a paged query to fetch results in chunks.

    Args:
    - query: QuerySet or list of data to paginate.
    - page_number: Current page number (1-based index).
    - page_size: Number of items per page.

    Returns:
    - Paginated results based on the page number and size.
    """
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    results = query[start_index:end_index]  # Example implementation
    return results
