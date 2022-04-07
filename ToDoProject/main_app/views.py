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
    return redirect('index')
