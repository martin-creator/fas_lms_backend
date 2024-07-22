# utils/pagination.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet

class PaginationError(Exception):
    """Custom exception for pagination errors."""
    pass

def paginate_queryset(queryset, page_number, page_size):
    """
    Paginate a queryset.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.

    Returns:
    - dict: Contains paginated data, current page number, total pages, and total items.

    Raises:
    - PaginationError: If pagination fails.
    """
    if not isinstance(queryset, QuerySet):
        raise PaginationError("Provided input is not a Django QuerySet.")

    paginator = Paginator(queryset, page_size)

    try:
        paginated_queryset = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    return {
        'data': paginated_queryset.object_list,
        'page_number': paginated_queryset.number,
        'total_pages': paginator.num_pages,
        'total_items': paginator.count
    }

def get_paginated_response(queryset, page_number, page_size, serializer=None):
    """
    Get paginated response.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.
    - serializer: Optional serializer function for the results.

    Returns:
    - dict: Contains paginated results, current page number, total pages, and total items.
    """
    paginated_data = paginate_queryset(queryset, page_number, page_size)
    
    results = paginated_data['data']
    if serializer:
        results = [serializer(item) for item in results]

    return {
        'results': results,
        'page': paginated_data['page_number'],
        'total_pages': paginated_data['total_pages'],
        'count': paginated_data['total_items']
    }

def execute_paged_query(query, page_number, page_size):
    """
    Execute a paged query to fetch results in chunks.

    Args:
    - query: List of data to paginate.
    - page_number: Current page number (1-based index).
    - page_size: Number of items per page.

    Returns:
    - list: Paginated results based on the page number and size.

    Raises:
    - PaginationError: If query is not a list or pagination fails.
    """
    if not isinstance(query, list):
        raise PaginationError("Provided input is not a list.")

    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size

    if start_index < 0:
        start_index = 0

    return query[start_index:end_index]

def paginate_queryset_with_filter(queryset, page_number, page_size, filter_func=None):
    """
    Paginate a queryset with an optional filter function.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.
    - filter_func: Optional filter function to apply to the queryset.

    Returns:
    - dict: Contains paginated data, current page number, total pages, and total items.

    Raises:
    - PaginationError: If pagination fails.
    """
    if filter_func:
        queryset = queryset.filter(filter_func)

    return paginate_queryset(queryset, page_number, page_size)

def paginate_and_sort_queryset(queryset, page_number, page_size, sort_field=None, sort_order='asc'):
    """
    Paginate and sort a queryset.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.
    - sort_field: Field to sort by (default is None, meaning no sorting).
    - sort_order: Order of sorting ('asc' or 'desc').

    Returns:
    - dict: Contains paginated and sorted data, current page number, total pages, and total items.

    Raises:
    - PaginationError: If pagination or sorting fails.
    """
    if sort_field:
        if sort_order == 'asc':
            queryset = queryset.order_by(sort_field)
        elif sort_order == 'desc':
            queryset = queryset.order_by(f'-{sort_field}')
        else:
            raise PaginationError("Invalid sort order. Use 'asc' or 'desc'.")

    return paginate_queryset(queryset, page_number, page_size)

def paginate_large_queryset(queryset, page_number, page_size):
    """
    Paginate a large queryset efficiently using a cursor-based pagination approach.

    Args:
    - queryset: Queryset to be paginated.
    - page_number: Page number to retrieve (1-based index).
    - page_size: Number of items per page.

    Returns:
    - dict: Contains paginated data, current page number, total pages, and total items.
    """
    # Assuming large dataset handling using cursor-based approach
    if not isinstance(queryset, QuerySet):
        raise PaginationError("Provided input is not a Django QuerySet.")

    cursor = page_number * page_size
    paginated_queryset = queryset[cursor:cursor + page_size]

    return {
        'data': paginated_queryset,
        'page_number': page_number,
        'total_pages': None,  # Not computed in cursor-based pagination
        'total_items': queryset.count()
    }