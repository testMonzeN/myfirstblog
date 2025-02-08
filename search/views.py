from queue import PriorityQueue

from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse
from blog.models import Post
from stepik.models import Taskpy, Taskjs
from itertools import chain
from django.urls import reverse

from blog.views import post_error
from stepik.views import task_detail, js_task_detail


def perform_search(query):
    object_post_list = Post.objects.filter(title__iregex=query)
    object_taskpy_list = Taskpy.objects.filter(title__iregex=query)
    object_taskjs_list = Taskjs.objects.filter(title__iregex=query)

    return list(chain(object_post_list, object_taskpy_list, object_taskjs_list))

def search_ajax(request):
    query = request.GET.get('q', '')
    all_object = perform_search(query)

    paginator = Paginator(all_object, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    html = render_to_string('search/post_list.html', {
        'posts': page_obj
    }, request=request)

    pag = render_to_string('search/pagination_search.html', {
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


def search(request):
    query = request.GET.get('q', '')
    all_object = perform_search(query)


    paginator = Paginator(all_object, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search/search_page_list.html', {
        'posts': page_obj,
        'page_obj': page_obj,

        'page_next': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'page_current': page_obj.number,
        'page_end': page_obj.paginator.num_pages,
        'page_has_next': page_obj.has_next,
        'page_has_previous': page_obj.has_previous,
        'query': query,
    })

def global_search(request):
    query = request.GET.get('q', '')
    return redirect(f'{reverse("search")}?q={query}')


def search_details(request, pk):
    query = request.GET.get('q', '')

    post = Post.objects.filter(title__iregex=query, pk=pk).first()
    taskpy = Taskpy.objects.filter(title__iregex=query, pk=pk).first()
    taskjs = Taskjs.objects.filter(title__iregex=query, pk=pk).first()

    if post:
        post_error(request, pk)
    elif taskpy:
        task_detail(request, pk)
    elif taskjs:
        js_task_detail(request, pk)


