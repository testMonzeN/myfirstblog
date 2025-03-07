from discord.app_commands import private_channel_only
from rest_framework import serializers
from blog.models import Post
from stepik.models import Taskpy, Taskjs
from rest_framework import viewsets
from django.contrib.auth import get_user_model
import requests
from django.shortcuts import render
from django.views import View
from .models import Catlink
from django.utils import timezone



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'created_date', 'published_date']

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer




class TaskPySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Taskpy
        fields = ['author', 'title', 'text', 'created_date', 'published_date']

class TaskPyViewSet(viewsets.ModelViewSet):
    author = UserSerializer(read_only=True)

    queryset = Taskpy.objects.all()
    serializer_class = TaskPySerializer




class TaskJsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taskjs
        fields = ['author', 'title', 'text', 'created_date', 'published_date']

class TaskJsViewSet(viewsets.ModelViewSet):
    queryset = Taskjs.objects.all()
    serializer_class = TaskJsSerializer


class Catapi(View):
    def get(self, request):
        key = 'live_pLbZvqWanhciL4RKR9IzPN0YcC1r6MUHzE2m5Rs3PxzlzZPyvo3hzJQ3HF12ne3G'
        url = 'https://api.thecatapi.com/v1/images/search'

        try:
            html = requests.get(url, params={
                'x-api-key': key
            }).json()

            image = html[0]['url']
        except Exception as e:
            image = None
            print('НЕ БУДЕТ КОТЭКА(((((((((((((((((((((((((((((((', e)

        self.load(image)
        return render(request, 'api/cat/cat.html', {
            'image': image
        })

    def load(self, link):
        model = Catlink()

        if not Catlink.objects.filter(link=link).exists():
            model.link = link
            model.published_date = timezone.now()

            model.save()





