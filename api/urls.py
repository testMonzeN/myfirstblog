from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TaskPyViewSet, TaskJsViewSet, Catapi, CatHistory, DogHistory, DogApi, DogHistoryAjax, CatHistoryAjax

router = DefaultRouter()
router.register(r'Posts', PostViewSet)
router.register(r'TaskPy', TaskPyViewSet)
router.register(r'TaskJs', TaskJsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('cat/', Catapi.as_view(), name='cat'),
    path('cat_hist/',  CatHistory.as_view(), name='cat_hist'),
    path('cat_hist/ajax/', CatHistoryAjax.as_view(), name='cat_history_ajax'),

    path('dog/',  DogApi.as_view(), name='dog'),
    path('dog_hist/',  DogHistory.as_view(), name='dog_hist'),
    path('dog_hist/ajax/', DogHistoryAjax.as_view(), name='dog_history_ajax'),
]