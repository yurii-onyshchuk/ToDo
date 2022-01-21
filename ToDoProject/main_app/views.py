from django.shortcuts import render, HttpResponse, redirect
from .models import Task
from .form import TaskForm


def index(request):
    task_list = Task.objects.all()
    return render(request, 'main_app/task_list.html', {'task_list': task_list})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'main_app/add_task.html', {'form': form})
