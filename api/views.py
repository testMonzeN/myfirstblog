from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from django_ratelimit.core import is_ratelimited
from rest_framework import serializers
from blog.models import Post
from stepik.models import Taskpy, Taskjs
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.views import View
from .models import Catlink, Doglink
from django.utils import timezone
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
    ratelimited = False

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.ratelimited = is_ratelimited(request=request, group='CatLimit', fn=None,
                                              key='user', rate='5/d', method='get',
                                              increment=True)
            return super().dispatch(request, *args, **kwargs)
        else: return redirect('sing_in')


    def get(self, request):
        if self.ratelimited:
            return render(request, 'api/cat/cat.html', {
                'ratelimited': True,
            })

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

        except Exception as e:
            print(f'Общая ошибка: {str(e)}')
            image = None

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



class CatHistory(View):
    def get(self, request):
        object_list = Catlink.objects.all()
        paginator = Paginator(object_list, 9)

        page_number = request.GET.get('page')
        all_image = paginator.get_page(page_number)

        return render(request, 'api/cat/history.html', {
            'images': all_image,

            'page_next': all_image.next_page_number() if all_image.has_next() else None,
            'page_previous': all_image.previous_page_number() if all_image.has_previous() else None,
            'page_current': all_image.number,
            'page_end': all_image.paginator.num_pages,
            'page_has_next': all_image.has_next,
            'page_has_previous': all_image.has_previous,
        })

class CatHistoryAjax(View):
    def get(self, request):
        object_list = Catlink.objects.all()
        paginator = Paginator(object_list, 9)

        page_number = request.GET.get('page')
        all_image = paginator.get_page(page_number)

        html = render_to_string('api/cat/images.html', {
            'images': all_image
        }, request=request)

        pag = render_to_string('api/cat/pag.html', {
            'page_next': all_image.next_page_number() if all_image.has_next() else None,
            'page_previous': all_image.previous_page_number() if all_image.has_previous() else None,
            'page_current': all_image.number,
            'page_end': all_image.paginator.num_pages,
            'page_has_next': all_image.has_next,
            'page_has_previous': all_image.has_previous
        }, request=request)

        return JsonResponse({
            'html': html,
            'paginator': pag,
        })


class DogApi(View):
    ratelimited = False
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.ratelimited = is_ratelimited(request=request, group='DogLimit', fn=None,
                                              key='user', rate='5/d', method='get',
                                              increment=True)
            return super().dispatch(request, *args, **kwargs)
        else: return redirect('sing_in')


    def get(self, request):
        if self.ratelimited:
            return render(request, 'api/dog/dog.html', {
                'ratelimited': True,
            })

        key = 'live_pLbZvqWanhciL4RKR9IzPN0YcC1r6MUHzE2m5Rs3PxzlzZPyvo3hzJQ3HF12ne3G'
        url = 'https://dog.ceo/api/breeds/image/random'

        try:
            response = requests.get(
                url,
                params={'x-api-key': key},
                timeout=(3.05, 5)
            )

            response.raise_for_status()
            html = response.json()
            image = html['message']

        except (requests.Timeout, requests.RequestException):
            return render(request, 'api/dog/dog.html', {
                'ratelimited': False,
                'error': 'Сервер с песиками не ответил вовремя 🐓'
            })

        except Exception as e:
            print(f'Общая ошибка: {str(e)}')
            image = None

        self.load(image)
        return render(request, 'api/dog/dog.html', {
            'image': image
        })

    def load(self, link):
        model = Doglink()
        if not Catlink.objects.filter(link=link).exists():
            model.link = link
            model.published_date = timezone.now()
            model.save()

class DogHistory(View):

    def get(self, request):
        object_list = Doglink.objects.all()
        paginator = Paginator(object_list, 9)

        page_number = request.GET.get('page')
        all_image = paginator.get_page(page_number)

        return render(request, 'api/dog/history.html', {
            'images': all_image,

            'page_next': all_image.next_page_number() if all_image.has_next() else None,
            'page_previous': all_image.previous_page_number() if all_image.has_previous() else None,
            'page_current': all_image.number,
            'page_end': all_image.paginator.num_pages,
            'page_has_next': all_image.has_next,
            'page_has_previous': all_image.has_previous,
        })


class DogHistoryAjax(View):
    def get(self, request):
        object_list = Doglink.objects.all()
        paginator = Paginator(object_list, 9)

        page_number = request.GET.get('page')
        all_image = paginator.get_page(page_number)

        html = render_to_string('api/dog/images.html', {
            'images': all_image
        }, request=request)

        pag = render_to_string('api/dog/pag.html', {
            'page_next': all_image.next_page_number() if all_image.has_next() else None,
            'page_previous': all_image.previous_page_number() if all_image.has_previous() else None,
            'page_current': all_image.number,
            'page_end': all_image.paginator.num_pages,
            'page_has_next': all_image.has_next,
            'page_has_previous': all_image.has_previous
        }, request=request)

        return JsonResponse({
            'html': html,
            'paginator': pag,
        })


