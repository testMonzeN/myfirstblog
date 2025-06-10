from django import forms
from django.contrib.auth.models import User

class CalculatorForm(forms.Form):
    target = forms.CharField(help_text='Введите размер мишени')
    dist = forms.CharField(help_text='Введите дистанцию до мишени')


    def clean(self):
        cleaned_data = super().clean()

        target = cleaned_data.get('target')
        dist = cleaned_data.get('dist')

        return cleaned_data
        
