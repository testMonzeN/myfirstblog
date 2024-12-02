import django.contrib.auth.handlers.modwsgi
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Answer(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    data_create = models.DateTimeField(default=timezone.now)
    date_public = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.date_public = timezone.now()
        self.save()

