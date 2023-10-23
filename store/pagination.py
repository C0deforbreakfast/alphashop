from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_number = 10

