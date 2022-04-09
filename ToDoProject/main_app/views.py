from django.shortcuts import render, HttpResponse, redirect
from .models import Task, Category
from .form import TaskForm


def task_list(request):
    title = 'Всі задання'
    task_list = Task.objects.all()
    return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})


def task_by_catagory(request, pk):
    title = Category.objects.get(pk=pk)
    task_list = Task.objects.filter(category_id=pk)
    return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})


def add_task(request):
    title = 'Додати завдання'
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'main_app/add_task.html', {'form': form, 'title': title})


def delete_task(request, pk):
    Task.objects.filter(id=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


def edit_task(request, pk):
    title = 'Редагування завдання'
    task = Task.objects.get(pk=pk)
    if request.method == 'GET':
        form = TaskForm({'title': task.title, 'text': task.text, 'category': task.category})
        return render(request, 'main_app/edit_task.html', {'title': title, 'form': form, 'task': task})
    elif request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('index')
