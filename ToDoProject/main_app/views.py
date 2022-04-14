from django.shortcuts import render, HttpResponse, redirect
from .models import Task, Category
from .form import TaskForm, CategoryForm, UserRegisterForm, UserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout


def task_list(request):
    title = 'Список завдань'
    task_list = Task.objects.filter(performed=False)
    return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})


def task_by_catagory(request, pk):
    title = Category.objects.get(pk=pk)
    task_list = Task.objects.filter(category_id=pk, performed=False)
    return render(request, 'main_app/task_by_category.html', {'task_list': task_list, 'title': title})


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
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('index')
    else:
        form = TaskForm({'title': task.title, 'text': task.text, 'category': task.category})
    return render(request, 'main_app/edit_task.html', {'title': title, 'form': form, 'task': task})


def add_category(request):
    title = 'Додати категорію'
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            category.save()
            return redirect('index')
    else:
        form = CategoryForm()
    return render(request, 'main_app/add_category.html', {'title': title, 'form': form, })


def edit_category(request, pk):
    title = 'Редагування категорії'
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            category.save()
            return redirect('task_by_category', pk)
    else:
        form = CategoryForm({'title': category.title})
    return render(request, 'main_app/edit_category.html', {'title': title, 'form': form, })


def delete_category(request, pk):
    Category.objects.get(pk=pk).delete()
    return redirect('index')


def user_register(request):
    title = 'Реєстрація'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успішна реєстрація!')
            return redirect('user_login')
        else:
            messages.error(request, 'Помилка реєстрації!')
    else:
        form = UserRegisterForm()
    return render(request, 'main_app/register.html', {'title': title, 'form': form})


def user_login(request):
    title = 'Вхід'
    if request.method == 'POST':
        form = UserAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = UserAuthenticationForm()
    return render(request, 'main_app/login.html', {'title': title, 'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def search(request):
    task_list = Task.objects.filter(title__icontains=request.GET.get('s'))
    return render(request, 'main_app/search.html', {'task_list': task_list})
