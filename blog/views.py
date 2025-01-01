from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from .models import Post, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .forms import PostForm, AnswerForm
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string



def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return JsonResponse({
        'html': render_to_string(request = request, template_name='blog/post_list.html',
                                 context={
                                     'posts': page_obj,
                                     'page_obj': page_obj,
                                     'page_number': page_number
                                 }
                                 )
    })


def post_list1(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'page_obj': page_obj
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



