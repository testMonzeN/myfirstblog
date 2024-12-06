from django.contrib.auth.decorators import login_required

from .models import Post, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .forms import PostForm, AnswerForm
from django.contrib import messages

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {
        'posts': posts,
        }
    )

def post_error(request, pk):

        post = get_object_or_404(Post, pk=pk)
        answers = Answer.objects.filter(post=post)
        return render(request, 'blog/post_error.html',
                      {'post': post,
                       'answers': answers
                       }
                      )

def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_error', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_create.html', {'form': form})
    else:
        return redirect('sing_in')

def answer_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.author = request.user
                answer.date_public = timezone.now()
                answer.save()
        else:
            form = AnswerForm()
        return render(request, 'blog/answer_create.html', {'form': form})
    else:
        return redirect('sing_in')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('sing_in')



