from django.db.models.functions import Trunc
from rest_framework import serializers
from blog.models import Post
from stepik.models import Taskpy, Taskjs
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .models import Catlink
from django.utils import timezone
from django_ratelimit.decorators import ratelimit
from django.urls import reverse
from django.utils.decorators import method_decorator
import requests

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
    @method_decorator(ratelimit(key='user', rate='5/d', block=True))
    def dispatch(self, request, *args, **kwargs):
        if not getattr(request, 'ratelimited', True):
            return render(request, 'api/cat/cat.html', {'ratelimited': True})
        return super().dispatch(request, *args, **kwargs)


    def get(self, request):
        key = 'live_pLbZvqWanhciL4RKR9IzPN0YcC1r6MUHzE2m5Rs3PxzlzZPyvo3hzJQ3HF12ne3G'
        url = 'https://api.thecatapi.com/v1/images/search'

        try:
            response = requests.get(
                url,
                params={'x-api-key': key},
                timeout=(3.05, 5)
            )

            response.raise_for_status()
            html = response.json()
            image = html[0]['url']

        except (requests.Timeout, requests.RequestException):
            return render(request, 'api/cat/cat.html', {
                'ratelimited': False,
                'error': 'Сервер с котэками не ответил вовремя 😿'
            })

        except:
            print(f'Общая ошибка: {str(e)}')
            image = None

        self.load(image)
        return render(request, 'api/cat/cat.html', {
            'ratelimited': False,
            'image': image
        })

    def load(self, link):
        model = Catlink()
        if not Catlink.objects.filter(link=link).exists():
            model.link = link
            model.published_date = timezone.now()
            model.save()


class CatHistory(View):
    def get(self, request):
        all_image = Catlink.objects.all()

        return render(request, 'api/cat/history.html', {
            'image': all_image
        })





