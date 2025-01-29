from django.urls import path
from . import views

urlpatterns = [
    path('ajax/', views.search_ajax, name='search_ajax'),
]