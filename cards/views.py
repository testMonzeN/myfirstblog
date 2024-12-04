from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib import messages

# Create your views here.
def cards_list(request):
    if request.user.is_authenticated:
        return render(request, 'cards/cards.html', {
            'user': request.user.is_superuser
        })
    else:
        return redirect('sing_in')

def teleport_blog(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        return redirect('sing_in')

def teleport_stepik(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return redirect('sing_in')
