from django.urls import path
from .views import Catapi, CatHistory, DogHistory, DogApi, DogHistoryAjax, CatHistoryAjax

urlpatterns = [
    path('cat/', Catapi.as_view(), name='cat'),
    path('cat_hist/',  CatHistory.as_view(), name='cat_hist'),
    path('cat_hist/ajax/', CatHistoryAjax.as_view(), name='cat_history_ajax'),

    path('dog/',  DogApi.as_view(), name='dog'),
    path('dog_hist/',  DogHistory.as_view(), name='dog_hist'),
    path('dog_hist/ajax/', DogHistoryAjax.as_view(), name='dog_history_ajax'),
]