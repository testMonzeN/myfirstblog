from django.urls import path
from . import views

urlpatterns = [
    path('', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_chat, name='group_chat'),
    path('create/', views.create_group, name='create_group'),
    path('upload-image/', views.upload_image, name='upload_image'),
]
