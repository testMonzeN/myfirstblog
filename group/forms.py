from django.forms import ModelForm
from .models import *
from django.conf import settings

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['img']
