from itertools import chain
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.datetime_safe import datetime
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from .models import Task, Category
from .form import CategoryForm
from .utils import TaskEditMixin


class TaskList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Всі завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date=None).order_by('-created_date')


class TodayTaskList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Завдання на сьогодні'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__date=datetime.today().date(),
                                   performed_date=None).order_by('planned_date')


class UpcomingTaskList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Майбутні завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__isnull=False, performed_date=None).order_by(
            'planned_date')


class ExpiredTaskList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Протерміновані завдання', 'without_add_task_button': True}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, planned_date__lt=datetime.today(),
                                   performed_date=None).order_by('planned_date')


class TaskByCategory(LoginRequiredMixin, ListView):
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
    extra_context = {'title': "Виконані завдання", 'without_add_task_button': True}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=False).order_by('-performed_date')


class SearchList(LoginRequiredMixin, ListView):
    extra_context = {'title': 'Пошук'}
    template_name = 'main_app/search_task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, title__icontains=self.request.GET.get('s'))


class AddTask(LoginRequiredMixin, TaskEditMixin, CreateView):
    model = Task
    extra_context = {'title': 'Додати завдання'}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, TaskEditMixin, UpdateView):
    extra_context = {'title': 'Редагувати завдання'}

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@login_required()
def perform_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed_date = datetime.now()
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_task(request, pk):
    task = Task.objects.filter(user=request.user, id=pk)
    task.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def recovery_task(request, pk):
    task = Task.objects.get(user=request.user, id=pk)
    task.performed_date = None
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_performed_tasks(request):
    tasks = Task.objects.filter(user=request.user, performed_date__isnull=False)
    tasks.delete()
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
    form_class = CategoryForm

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


@login_required
def delete_category(request, pk):
    category = Category.objects.filter(user=request.user, id=pk)
    category.delete()
    return redirect('tasks')
