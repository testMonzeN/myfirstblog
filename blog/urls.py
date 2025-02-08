from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('ajax/', views.post_list_ajax, name='ajax_post_list'),
    path('post/<int:pk>/', views.post_error, name='post_error'),
    path('post/new/', views.post_new, name='post_new'),
    path('answer/new/', views.answer_new, name='answer_new'),
    path('#', views.logout_view, name='logout'),
]