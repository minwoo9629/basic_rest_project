from django.shortcuts import render
from rest_framework import viewsets
from myapi.models import Essay, Album, Files
from myapi.serializers import EssaySerializer, AlbumSerializer, FilesSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from myapi.pagination import EssayPageNumberPagination

class EssayViewSet(viewsets.ModelViewSet):
    queryset = Essay.objects.all()
    serializer_class = EssaySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = EssayPageNumberPagination

    filter_backends = [SearchFilter]
    search_fields = ('title', 'content')

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                pass
            else:
                qs = qs.filter(author=self.request.user)
        else:
            qs = qs.none()

        return qs

    def perform_create(self, serializers):
        serializers.save(author=self.request.user)

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]
    search_fields = ('description',)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                pass
            else:
                qs = qs.filter(author=self.request.user)
        else:
            qs = qs.none()

        return qs

    def perform_create(self, serializers):
        serializers.save(author=self.request.user)

class FilesViewSet(viewsets.ModelViewSet):
    queryset = Files.objects.all()
    serializer_class = FilesSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter]
    search_fields = ('description',)

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                pass
            else:
                qs = qs.filter(author=self.request.user)
        else:
            qs = qs.none()

        return qs

    # 파일 업로드를 위한
    # parser_class 지정
    parser_classes = (MultiPartParser, FormParser)
    # create() 오버라이딩 create() -> post()
    def post(self, request, *args, **kwargs):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializers):
        serializers.save(author=self.request.user)
        