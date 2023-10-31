from itertools import chain

from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.datetime_safe import datetime
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from .form import CategoryForm
from .models import Task, Category
from .mixins import AddUserToFormMixin, TaskEditMixin


class TaskList(LoginRequiredMixin, ListView):
    """View for listing all tasks associated with the currently authenticated user."""

    extra_context = {'title': 'Всі завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date=None).order_by('-created_date')


class TodayTaskList(LoginRequiredMixin, ListView):
    """View for listing tasks for that are planned for today."""

    extra_context = {'title': 'Завдання на сьогодні'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__date=datetime.today().date(),
                                   performed_date=None).order_by('planned_date')


class UpcomingTaskList(LoginRequiredMixin, ListView):
    """View for listing upcoming tasks that are not yet completed."""

    extra_context = {'title': 'Майбутні завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__isnull=False, performed_date=None).order_by(
            'planned_date')


class ExpiredTaskList(LoginRequiredMixin, ListView):
    """View for listing expired tasks."""

    extra_context = {'title': 'Протерміновані завдання', 'without_add_task_button': True}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__lt=datetime.today(),
                                   performed_date=None).order_by('planned_date')


class TaskByCategory(LoginRequiredMixin, ListView):
    """View for listing tasks by category."""

    template_name = 'main_app/task_list.html'
    context_object_name = 'task_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(user=self.request.user, pk=self.kwargs['pk'])
        context['title'] = context['category']
        return context

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, category__pk=self.kwargs['pk'], performed_date=None)
        return list(chain(queryset.filter(planned_date__isnull=False).order_by('planned_date'),
                          queryset.filter(planned_date__isnull=True).order_by('-created_date')))


class PerformedTask(LoginRequiredMixin, ListView):
    """View for listing performed tasks."""

    extra_context = {'title': "Виконані завдання", 'without_add_task_button': True}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=False).order_by('-performed_date')


class SearchList(LoginRequiredMixin, ListView):
    """View for searching tasks."""

    template_name = 'main_app/search_task_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Результати пошуку'
        context['q'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        return Task.objects.filter(Q(user=self.request.user, title__icontains=self.request.GET.get('q')) |
                                   Q(user=self.request.user, description__icontains=self.request.GET.get('q')))


class AddTask(LoginRequiredMixin, TaskEditMixin, AddUserToFormMixin, CreateView):
    """View for adding a new task."""

    model = Task
    extra_context = {'title': 'Додати завдання'}


class UpdateTask(LoginRequiredMixin, TaskEditMixin, UpdateView):
    """View for updating an existing task."""

    extra_context = {'title': 'Редагувати завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@login_required()
def perform_task(request, pk):
    """Mark a task as performed by setting the performed_date to the current date and time."""

    task = Task.objects.get(user=request.user, id=pk)
    task.performed_date = datetime.now()
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_task(request, pk):
    """View allows users to delete a specific task from their task list."""

    task = Task.objects.filter(user=request.user, id=pk)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def recovery_task(request, pk):
    """View allows users to recover a previously performed task by setting the performed_date to None."""

    task = Task.objects.get(user=request.user, id=pk)
    task.performed_date = None
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_performed_tasks(request):
    """Delete all performed tasks that have been marked as performed."""

    tasks = Task.objects.filter(user=request.user, performed_date__isnull=False)
    tasks.delete()
    return redirect(request.META.get('HTTP_REFERER'))


class AddCategory(LoginRequiredMixin, AddUserToFormMixin, CreateView):
    """View for adding a new category."""

    extra_context = {'title': 'Додати категорію'}
    model = Category
    form_class = CategoryForm


class UpdateCategory(LoginRequiredMixin, UpdateView):
    """View for updating a new category."""

    extra_context = {'title': 'Редагування категорії'}
    form_class = CategoryForm

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


@login_required
def delete_category(request, pk):
    """View for deleting of category."""

    category = Category.objects.filter(user=request.user, id=pk)
    category.delete()
    return redirect('tasks')
