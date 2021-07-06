from rest_framework import pagination


class ESASkyPaginator(pagination.PageNumberPagination):

    page_size = 10
    max_page_size = 100
