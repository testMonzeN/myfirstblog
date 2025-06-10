from django.urls import path
from .views import CalculatorView

urlpatterns = [
    path('', CalculatorView.as_view(), name='calc'),
]