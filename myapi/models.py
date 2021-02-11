from django.db import models
from django.conf import settings
from uuid import uuid4
from datetime import datetime
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



def get_image_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    return '/'.join(['images', ymd_path, filename])

def get_file_path(instance, filename):
    ymd_path = datetime.now().strftime('%Y/%m/%d')
    return '/'.join(['files', ymd_path, filename])

class Essay(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Album(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, null=False, blank=False)
    description = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
        super(Album, self).delete(*args, **kwargs)

class Files(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_file = models.FileField(upload_to=get_file_path, null=False, blank=False)
    description = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def delete(self, *args, **kwargs):
        if self.upload_file:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.upload_file.path))
        super(Files, self).delete(*args, **kwargs)