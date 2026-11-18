from rest_framework.pagination import PageNumberPagination


class Paginacao(PageNumberPagination):
    """?page=2&page_size=50 (máximo 100 por página)."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
