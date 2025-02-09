from django.template.loader import render_to_string

from .models import Taskjs, Decisionjs, Taskpy, Decisionpy
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .form import DecisionForm, DecisionFormJs
import requests, re
from django.http import JsonResponse
from forchan.urls import *
from django.contrib.auth.models import User

def main(request):
    return render(request, 'stepik/index.html', {
        'user': request.user.is_superuser
    })


def ajax_task_list_py(request):
    object_list = Taskpy.objects.all()
    paginator = Paginator(object_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    html = render_to_string('stepik/py/py_task_list.html', {
        'tasks': page_obj
    }, request=request)

    pag = render_to_string('stepik/py/paginator.html', {
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

def task_list(request):
    tasks = Taskpy.objects.all()
    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stepik/py/py_stepik_list.html', {
        'tasks': page_obj,
        'page_obj': page_obj,

        'page_next': page_obj.next_page_number() if page_obj.has_next() else None,
        'page_previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'page_current': page_obj.number,
        'page_end': page_obj.paginator.num_pages,
        'page_has_next': page_obj.has_next,
        'page_has_previous': page_obj.has_previous,

        'user': request.user.is_superuser,
    })


def task_detail(request, pk):
    task = get_object_or_404(Taskpy, pk=pk)
    decisions = Decisionpy.objects.filter(task=task)
    return render(request, 'stepik/py/task_detail.html',
                  {
                      'task': task,
                      'decisions': decisions
                   }
                )
def decision_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DecisionForm(request.POST)
            if form.is_valid():
                decision = form.save(commit=False)
                decision.author = request.user
                decision.published_date = timezone.now()
                decision.save()
                return redirect('py_task_detail', pk=decision.task.pk)
        else:
            form = DecisionForm()
        return render(request, 'stepik/py/decision_edit.html', {'form': form})

    else:
        return redirect('sing_in')

def py_task_new(request):
    url = f'https://api.github.com/repos/testMonzeN/Practic/contents/'
    response = requests.get(url)
    content = response.json()
    for item in content:
        if item['type'] == 'file' and '.py' in item['name']:
            if not Taskpy.objects.filter(title=item['name']).exists():
                a = requests.get(item['download_url']).text.replace('\n', ' ')
                matches = re.findall(r"'''(.*?)'''", a)
                for match in matches:
                    task = Taskpy()

                    task.title = item['name']
                    task.text = match
                    task.author = request.user
                    task.published_date = timezone.now()

                    task.save()

    return redirect('py_task_list')

##################################################
#                                                #
#                 JavaScript                     #
#                                                #
##################################################

def ajax_task_list_js(request):
    object_list = Taskjs.objects.all()
    paginator = Paginator(object_list, 5)

    page_number = request.GET.get('page')
    tasks_in_page = paginator.get_page(page_number)

    html = render_to_string('stepik/js/js_task_list.html', {
        'tasks': tasks_in_page
    }, request=request)

    pag = render_to_string('stepik/js/paginator.html', {
        'page_next': tasks_in_page.next_page_number() if tasks_in_page.has_next() else None,
        'page_previous': tasks_in_page.previous_page_number() if tasks_in_page.has_previous() else None,
        'page_current': tasks_in_page.number,
        'page_end': tasks_in_page.paginator.num_pages,
        'page_has_next': tasks_in_page.has_next,
        'page_has_previous': tasks_in_page.has_previous
    }, request=request)

    return JsonResponse({
        'html': html,
        'paginator': pag,
    })


def js_task_list(request):
    tasks = Taskjs.objects.all()
    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')
    tasks_in_page = paginator.get_page(page_number)

    return render(request, 'stepik/js/js_stepik_list.html', {
        'tasks': tasks_in_page,
        'page_obj': tasks_in_page,

        'page_next': tasks_in_page.next_page_number() if tasks_in_page.has_next() else None,
        'page_previous': tasks_in_page.previous_page_number() if tasks_in_page.has_previous() else None,
        'page_current': tasks_in_page.number,
        'page_end': tasks_in_page.paginator.num_pages,
        'page_has_next': tasks_in_page.has_next,
        'page_has_previous': tasks_in_page.has_previous,

        'user': request.user.is_superuser
    })


def js_task_detail(request, pk):
    task = get_object_or_404(Taskjs, pk=pk)
    decisions = Decisionjs.objects.filter(task=task)
    return render(request, 'stepik/js/js_task_detail.html',
                  {
                      'task': task,
                      'decisions': decisions
                   }
                )

def js_decision_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = DecisionFormJs(request.POST)
            if form.is_valid():
                decision = form.save(commit=False)
                decision.author = request.user
                decision.published_date = timezone.now()
                decision.save()
                return redirect('js_task_detail', pk=decision.task.pk)
        else:
            form = DecisionFormJs()
        return render(request, 'stepik/js/js_decision_edit.html', {'form': form})
    else:
        return redirect('sing_in')

def js_task_new(request):
    url = f'https://api.github.com/repos/testMonzeN/Practic/contents/'
    response = requests.get(url)
    content = response.json()
    whiteList = ['13_1.py', '13_2.py', '15_1.py', "16_2.py", '16_3.py', '1_11.py', '21_1.py', '23_2.py', '25.py', "31_1.py", '31_2.py']
    for item in content:
        if item['type'] == 'file' and '.py' in item['name'] and item['name'] in whiteList:
            if not Taskjs.objects.filter(title=item['name'].replace('.py', '.js')).exists():
                a = requests.get(item['download_url']).text.replace('\n', ' ')
                matches = re.findall(r"'''(.*?)'''", a)
                for match in matches:
                    task = Taskjs()

                    task.title = item['name'].replace('.py', '.js')

                    task.text = match
                    task.author = request.user
                    task.published_date = timezone.now()

                    task.save()

    return redirect('js_task_list')