from django.shortcuts import resolve_url
from django.utils import timezone
from django.db import models
from django.conf import settings


#Python
class Taskpy(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('py_task_detail', pk=self.pk)

    def get_author(self):
        return self.author.username

class Decisionpy(models.Model):
    task = models.ForeignKey(Taskpy, on_delete=models.CASCADE)

    text = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()



class Taskjs(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return resolve_url('js_task_detail', pk=self.pk)

    def get_author(self):
        return self.author.username

class Decisionjs(models.Model):
    task = models.ForeignKey(Taskjs, on_delete=models.CASCADE)

    text = models.TextField()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()