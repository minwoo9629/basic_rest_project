from rest_framework.pagination import PageNumberPagination

class EssayPageNumberPagination(PageNumberPagination):
    page_size = 10