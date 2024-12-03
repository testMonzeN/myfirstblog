from django import forms
from .models import Post
from .models import Answer
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('post', 'text')






