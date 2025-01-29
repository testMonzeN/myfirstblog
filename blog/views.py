from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from requests import request

from .models import Post, Answer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .forms import PostForm, AnswerForm
from django.http import JsonResponse
from django.template.loader import render_to_string




def post_list_ajax(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    html = render_to_string('blog/post_list.html', {
        'posts': page_obj
    }, request=request)

    pag = render_to_string('blog/pagination.html', {
        'page_next': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'page_current': page_obj.number,
        'page_end': page_obj.paginator.num_pages,
        'page_has_next': page_obj.has_next,
        'page_has_previous': page_obj.has_previous
    }, request=request)

    return JsonResponse({
        'html': html,
        'paginator': pag,
    })

def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_page.html', {
        'posts': page_obj,
        'page_obj': page_obj,

        'page_next': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'page_current': page_obj.number,
        'page_end': page_obj.paginator.num_pages,
        'page_has_next': page_obj.has_next,
        'page_has_previous': page_obj.has_previous,
        'pag_status': True
    })


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



