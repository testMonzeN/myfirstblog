from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.reg, name='register'),
    path('sing_in/', views.sing_in, name='sing_in'),
]
