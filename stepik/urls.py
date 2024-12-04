from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),

    path('#', views.py_task_new, name='py_update_tasks'),
    path('python/', views.task_list, name='py_task_list'),
    path('python/<int:pk>/', views.task_detail, name='py_task_detail'),
    path('python/new/', views.decision_new, name='py_decision_new'),

    path('?', views.js_task_new, name='js_update_tasks'),
    path('js/', views.js_task_list, name='js_task_list'),
    path('js/<int:pk>/', views.js_task_detail, name='js_task_detail'),
    path('js/new/', views.js_decision_new, name='js_decision_new'),

]
