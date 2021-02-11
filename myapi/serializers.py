from myapi.models import Essay, Album, Files
from rest_framework import serializers

class EssaySerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Essay
        fields = ['pk', 'title', 'content', 'author_name', 'created_at', 'updated_at']

class AlbumSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = Album
        fields = ['pk', 'image', 'description', 'author_name', 'created_at', 'updated_at']

class FilesSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    upload_file = serializers.FileField(use_url=True)
    class Meta:
        model = Files
        fields = ['pk', 'upload_file', 'description', 'author', 'created_at', 'updated_at']