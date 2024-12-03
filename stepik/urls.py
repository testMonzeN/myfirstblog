from django.urls import path
from . import views

urlpatterns = [
    path('#', views.task_new, name='update_tasks'),
    path('', views.task_list, name='task_list'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('new/', views.decision_new, name='decision_new')

]