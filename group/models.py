from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=255)
    
    user_list = models.ManyToManyField(User, related_name='online', blank=True)
    
    def get_user_count(self):
        return self.user_list.count()
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'pk': self.pk})
    
    
    
class Message(models.Model):
    img = models.ImageField(upload_to='messages/', blank=True, null=True)
    text = models.CharField(max_length=255)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    date_create = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.text
    
    def get_group(self):
        return self.group.name
    
    
    def get_author(self):
        return self.author.username
    
    def get_absolute_url(self):
        return reverse('message_detail', kwargs={'pk': self.pk})
    