from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def reg(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user2 = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password,
                first_name=user.first_name,
                last_name=user.last_name
            )
            user2.save()
            login(request, user2)
            return redirect('post_list')
    else:
        form = RegisterForm()
    return render(request, 'users/reg.html', {'form': form})


def sing_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('cards')
        else:
            messages.error(request, 'неправильный логин или пароль')

    return render(request, 'users/sing_in.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('sing_in')