from django import forms
from .models import Post
from .models import Answer

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('post', 'text')