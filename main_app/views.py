from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from .models import Task, Category
from .form import TaskForm, CategoryForm, UserRegisterForm, UserAuthenticationForm


class UserRegister(FormView):
    template_name = 'main_app/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super(UserRegister, self).get_context_data()
        context['title'] = 'Реєстрація'
        return context

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Успішна реєстрація!')
        return super(UserRegister, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка реєстрації!')
        return super(UserRegister, self).form_invalid(form)


class UserLogin(LoginView):
    template_name = 'main_app/login.html'
    form_class = UserAuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super(UserLogin, self).get_context_data()
        context['title'] = 'Вхід'
        return context

    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список завдань'
        return context


class TaskByCategory(LoginRequiredMixin, ListView):
    template_name = 'main_app/task_by_category.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, category__pk=self.kwargs['pk'], performed=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        return context


class PerformedTask(LoginRequiredMixin, ListView):
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Виконані завдання"
        return context


class SearchList(LoginRequiredMixin, ListView):
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пошук'
        return context


class AddTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddTask, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddTask, self).get_context_data()
        context['title'] = 'Додати завдання'
        return context


@login_required()
def perform_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed = True
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


class UpdateTask(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super(UpdateTask, self).get_context_data()
        context['title'] = 'Редагування завдання'
        return context


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super(DeleteTask, self).get_context_data()
        context['title'] = 'Видалення завдання'
        return context


@login_required()
def recovery_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed = False
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


class AddCategory(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(AddCategory, self).get_context_data()
        context['title'] = 'Додати категорію'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCategory, self).form_valid(form)


class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm

    def get_context_data(self, **kwargs):
        context = super(UpdateCategory, self).get_context_data()
        context['title'] = 'Редагування категорії'
        return context


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('tasks')

    def get_context_data(self, **kwargs):
        context = super(DeleteCategory, self).get_context_data()
        context['title'] = 'Видалити категорію'
        return context
