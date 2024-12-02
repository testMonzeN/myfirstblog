from .models import Task, Decision
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .form import DecisionForm
import requests, re

def task_list(request):
    if request.user.is_authenticated:
        task_new(request)
        tasks = Task.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        return render(request, 'stepik/task_list.html', {
            'tasks': tasks
        }
    )
    else:
        return redirect('sing_in')
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    decisions = Decision.objects.filter(task=task)
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
    else:
        form = DecisionForm()
    return render(request, 'stepik/decision_edit.html', {'form': form})

def task_new(request):
    count = 0
    url = f'https://api.github.com/repos/testMonzeN/Practic/contents/'
    response = requests.get(url)
    content = response.json()
    for item in content:
        if item['type'] == 'file' and '.py' in item['name']:
            a = requests.get(item['download_url']).text.replace('\n', ' ')
            matches = re.findall(r"'''(.*?)'''", a)
            for match in matches:
                task = Task()
                task.title = item['name']
                task.text = match
                task.author = request.user
                task.published_date = timezone.now()


                if not Task.objects.filter(title=item['name']).exists():
                    task.save()
                    count += 1

    print('added:', count)






