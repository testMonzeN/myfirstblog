from rest_framework import serializers
from blog.models import Post
from stepik.models import Taskpy, Taskjs
from rest_framework import viewsets
from django.contrib.auth import get_user_model

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