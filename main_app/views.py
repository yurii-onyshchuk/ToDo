from django.shortcuts import render, HttpResponse, redirect
from .models import Task, Category
from .form import TaskForm, CategoryForm, UserRegisterForm, UserAuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout


def task_list(request):
    if request.user.is_authenticated:
        title = 'Список завдань'
        task_list = Task.objects.filter(user=request.user, performed=False)
        return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})
    else:
        return redirect('user_login')


def task_by_catagory(request, pk):
    if request.user.is_authenticated:
        title = Category.objects.get(user=request.user, pk=pk)
        task_list = Task.objects.filter(user=request.user, category_id=pk, performed=False)
        return render(request, 'main_app/task_by_category.html', {'task_list': task_list, 'title': title})
    else:
        return redirect('user_login')


def add_task(request):
    if request.user.is_authenticated:
        title = 'Додати завдання'
        if request.method == "POST":
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('index')
        else:
            form = TaskForm()
            form.fields['category'].queryset = Category.objects.filter(user=request.user)
        return render(request, 'main_app/add_task.html', {'form': form, 'title': title})
    else:
        return redirect('user_login')


def delete_task(request, pk):
    if request.user.is_authenticated:
        Task.objects.get(user=request.user, id=pk).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('user_login')


def perform_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(user=request.user, id=pk)
        task.performed = True
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('user_login')


def performed_task(request):
    if request.user.is_authenticated:
        title = "Виконані завдання"
        task_list = Task.objects.filter(user=request.user, performed=True)
        return render(request, 'main_app/task_list.html', {'task_list': task_list, 'title': title})
    else:
        return redirect('user_login')


def recovery_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(user=request.user, id=pk)
        task.performed = False
        task.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('user_login')


def edit_task(request, pk):
    if request.user.is_authenticated:
        title = 'Редагування завдання'
        task = Task.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
                task = form.save(commit=False)
                task.save()
                return redirect('index')
        else:
            form = TaskForm({'title': task.title, 'text': task.text, 'category': task.category})
        return render(request, 'main_app/edit_task.html', {'title': title, 'form': form, 'task': task})
    else:
        return redirect('user_login')


def add_category(request):
    if request.user.is_authenticated:
        title = 'Додати категорію'
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save()
                category.user = request.user
                category.save()
                return redirect('index')
        else:
            form = CategoryForm()
        return render(request, 'main_app/add_category.html', {'title': title, 'form': form, })
    else:
        return redirect('user_login')


def edit_category(request, pk):
    if request.user.is_authenticated:
        title = 'Редагування категорії'
        category = Category.objects.get(user=request.user, pk=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                category = form.save()
                category.save()
                return redirect('task_by_category', pk)
        else:
            form = CategoryForm({'title': category.title})
        return render(request, 'main_app/edit_category.html', {'title': title, 'form': form, })
    else:
        return redirect('user_login')


def delete_category(request, pk):
    if request.user.is_authenticated:
        Category.objects.get(pk=pk).delete()
        return redirect('index')
    else:
        return redirect('user_login')


def search(request):
    if request.user.is_authenticated:
        task_list = Task.objects.filter(user=request.user, title__icontains=request.GET.get('s'))
        return render(request, 'main_app/search.html', {'task_list': task_list})
    else:
        return redirect('user_login')


def user_register(request):
    if not request.user.is_authenticated:
        title = 'Реєстрація'
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Успішна реєстрація!')
                return redirect('index')
            else:
                messages.error(request, 'Помилка реєстрації!')
        else:
            form = UserRegisterForm()
        return render(request, 'main_app/register.html', {'title': title, 'form': form})
    else:
        return redirect('index')


def user_login(request):
    if not request.user.is_authenticated:
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
    else:
        return redirect('index')


def user_logout(request):
    logout(request)
    return redirect('user_login')
