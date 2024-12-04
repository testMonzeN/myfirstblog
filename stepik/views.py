from .models import Taskjs, Decisionjs, Taskpy, Decisionpy
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .form import DecisionForm
import requests, re
from django.contrib.auth.models import User

def main(request):
    return render(request, 'stepik/index.html', {
        'user': request.user.is_superuser
    })



def task_list(request):
    if request.user.is_authenticated:
        tasks = Taskpy.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'stepik/task_list.html', {
            'tasks': tasks,
            'user': request.user.is_superuser
        }
    )
    else:
        return redirect('sing_in')
def task_detail(request, pk):
    task = get_object_or_404(Taskpy, pk=pk)
    decisions = Decisionpy.objects.filter(task=task)
    return render(request, 'stepik/task_detail.html',
                  {'task': task,
                            'decisions': decisions
                   }
                )
def decision_new(request):
    if request.method == "POST":
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.author = request.user
            decision.published_date = timezone.now()
            decision.save()
            return redirect('task_list')
    else:
        form = DecisionForm()
    return render(request, 'stepik/decision_edit.html', {'form': form})

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
def js_task_list(request):
    if request.user.is_authenticated:
        tasks = Taskjs.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'stepik/js_task_list.html', {
            'tasks': tasks,
            'user': request.user.is_superuser
        }
    )
    else:
        return redirect('sing_in')
def js_task_detail(request, pk):
    task = get_object_or_404(Taskjs, pk=pk)
    decisions = Decisionjs.objects.filter(task=task)
    return render(request, 'stepik/js_task_detail.html',
                  {'task': task,
                            'decisions': decisions
                   }
                )
def js_decision_new(request):
    if request.method == "POST":
        form = DecisionForm(request.POST)
        if form.is_valid():
            decision = form.save(commit=False)
            decision.author = request.user
            decision.published_date = timezone.now()
            decision.save()
            return redirect('task_list')
    else:
        form = DecisionForm()
    return render(request, 'stepik/js_decision_edit.html', {'form': form})

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