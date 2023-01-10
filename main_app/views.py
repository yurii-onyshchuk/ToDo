from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task, Category
from .form import TaskForm, CategoryForm


class TaskList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Всі завдання', 'task_performed': False}
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed=False)


class TaskByCategory(LoginRequiredMixin, ListView):
    extra_context = {'task_performed': False}
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, category__pk=self.kwargs['pk'], performed=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        context['title'] = context['category']
        return context


class PerformedTask(LoginRequiredMixin, ListView):
    extra_context = {'title': "Виконані завдання", 'tasks_performed': True}
    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed=True)


class SearchList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Пошук'}
    template_name = 'main_app/search_task_list.html'
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, title__icontains=self.request.GET.get('s'))


class AddTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddTask, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(AddTask, self).get_context_data()
        context['title'] = 'Додати завдання'
        context['form'].fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return context

    def get_success_url(self):
        if self.request.POST['category']:
            return reverse_lazy('task-by-category', kwargs={'pk': self.request.POST['category'], })
        else:
            return reverse_lazy('tasks')


@login_required()
def perform_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed = True
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


class UpdateTask(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Редагування завдання'}
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


class DeleteTask(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'Видалення завдання'}
    model = Task
    success_url = reverse_lazy('tasks')


@login_required()
def recovery_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed = False
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


class AddCategory(LoginRequiredMixin, CreateView):
    extra_context = {'title': 'Додати категорію'}
    model = Category
    form_class = CategoryForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddCategory, self).form_valid(form)


class UpdateCategory(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Редагування категорії'}
    model = Category
    form_class = CategoryForm


class DeleteCategory(LoginRequiredMixin, DeleteView):
    extra_context = {'title': 'Видалити категорію'}
    model = Category
    success_url = reverse_lazy('tasks')
