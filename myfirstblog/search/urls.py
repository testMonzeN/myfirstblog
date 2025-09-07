from django.urls import path
from . import views

urlpatterns = [
    path('ajax/', views.search_ajax, name='search_ajax'),
    path('', views.search, name='search'),
    path('sadjosdfojkfdjosdfjiosdfsdfji/', views.global_search, name='global_search'),
]