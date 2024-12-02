from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput)
    email = forms.CharField(label='Email', widget=forms.TextInput)

    first_name = forms.CharField(label='Фамилия', widget=forms.TextInput)
    last_name = forms.CharField(label='Отчество', widget=forms.TextInput)

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

class SingInForm(forms.ModelForm):
    username = forms.CharField(label='Login', widget=forms.TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password')