from django.shortcuts import render, HttpResponse, redirect
from .models import Task, Category
from .form import TaskForm, CategoryForm


def task_list(request):
    title = 'Всі задання'
    task_list = Task.objects.filter(performed=False)
    return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})


def task_by_catagory(request, pk):
    title = Category.objects.get(pk=pk)
    task_list = Task.objects.filter(category_id=pk, performed=False)
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
    Task.objects.get(id=pk).delete()
    return redirect(request.META.get('HTTP_REFERER'))


def perform_task(request, pk):
    task = Task.objects.get(id=pk)
    task.performed = True
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


def performed_task(request):
    title = "Виконані завдання"
    task_list = Task.objects.filter(performed=True)
    return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})


def recovery_task(request, pk):
    task = Task.objects.get(id=pk)
    task.performed = False
    task.save()
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


def add_category(request):
    title = 'Додати категорію'
    if request.method == 'GET':
        form = CategoryForm()
        return render(request, 'main_app/add_category.html', {'title': title, 'form': form, })
    elif request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category.save()
            return redirect('index')
