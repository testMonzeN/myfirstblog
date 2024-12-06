from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages

# Create your views here.
def cards_list(request):
    return render(request, 'cards/cards.html', {
        'user': request.user.is_superuser
    })

def teleport_blog(request):
    return redirect('post_list')

def teleport_stepik(request):
    return redirect('main')
