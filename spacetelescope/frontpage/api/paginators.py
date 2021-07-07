from rest_framework import pagination


class ESASkyPaginator(pagination.PageNumberPagination):

    page_size = 100
    max_page_size = 100
