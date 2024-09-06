# utils/pagination.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.query import QuerySet

class PaginationError(Exception):
    """Custom exception for pagination errors."""
    pass

class PaginatorService:
    def __init__(self, queryset=None, page_number=1, page_size=10, sort_field=None, sort_order='asc', filter_func=None):
        """
        Initialize the PaginatorService class.

        Args:
        - queryset (QuerySet, optional): The queryset to paginate.
        - page_number (int, optional): The page number to retrieve (1-based index). Defaults to 1.
        - page_size (int, optional): Number of items per page. Defaults to 10.
        - sort_field (str, optional): Field to sort by. Defaults to None (no sorting).
        - sort_order (str, optional): Order of sorting ('asc' or 'desc'). Defaults to 'asc'.
        - filter_func (callable, optional): Optional filter function to apply to the queryset. Defaults to None.

        Raises:
        - PaginationError: If invalid parameters are provided.
        """
        if queryset and not isinstance(queryset, QuerySet):
            raise PaginationError("Provided input is not a Django QuerySet.")
        if sort_order not in ['asc', 'desc']:
            raise PaginationError("Invalid sort order. Use 'asc' or 'desc'.")

        self.queryset = queryset
        self.page_number = page_number
        self.page_size = page_size
        self.sort_field = sort_field
        self.sort_order = sort_order
        self.filter_func = filter_func

    def paginate_queryset(self):
        """
        Paginate the queryset.

        Returns:
        - dict: Contains paginated data, current page number, total pages, and total items.

        Raises:
        - PaginationError: If pagination fails.
        """
        if self.filter_func:
            self.queryset = self.queryset.filter(self.filter_func)
        
        if self.sort_field:
            self.queryset = self.queryset.order_by(self.sort_field if self.sort_order == 'asc' else f'-{self.sort_field}')

        paginator = Paginator(self.queryset, self.page_size)

        try:
            paginated_queryset = paginator.page(self.page_number)
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

    def get_paginated_response(self, serializer=None):
        """
        Get a paginated response with optional serialization.

        Args:
        - serializer (callable, optional): Optional serializer function for the results. Defaults to None.

        Returns:
        - dict: Contains paginated results, current page number, total pages, and total items.
        """
        paginated_data = self.paginate_queryset()
        results = paginated_data['data']
        if serializer:
            results = [serializer(item) for item in results]

        return {
            'results': results,
            'page': paginated_data['page_number'],
            'total_pages': paginated_data['total_pages'],
            'count': paginated_data['total_items']
        }

    @staticmethod
    def execute_paged_query(query, page_number, page_size):
        """
        Execute a paged query to fetch results in chunks.

        Args:
        - query (list): List of data to paginate.
        - page_number (int): Current page number (1-based index).
        - page_size (int): Number of items per page.

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

    @staticmethod
    def paginate_large_queryset(queryset, page_number, page_size):
        """
        Paginate a large queryset efficiently using a cursor-based pagination approach.

        Args:
        - queryset (QuerySet): Queryset to be paginated.
        - page_number (int): Page number to retrieve (1-based index).
        - page_size (int): Number of items per page.

        Returns:
        - dict: Contains paginated data, current page number, total pages (None for cursor-based), and total items.

        Raises:
        - PaginationError: If pagination fails.
        """
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
