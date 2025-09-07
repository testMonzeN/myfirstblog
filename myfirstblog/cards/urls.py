from django.urls import path
from . import views

urlpatterns = [
    path('', views.cards_list, name='cards'),
    path('#', views.teleport_blog, name='teleport_blog'),

    path('?', views.teleport_stepik, name='teleport_stepik')
]