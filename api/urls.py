from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, TaskPyViewSet, TaskJsViewSet, Catapi, CatHistory

router = DefaultRouter()
router.register(r'Posts', PostViewSet)
router.register(r'TaskPy', TaskPyViewSet)
router.register(r'TaskJs', TaskJsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('cat/', Catapi.as_view(), name='cat'),
    path('hist/',  CatHistory.as_view(), name='hist')
]