from django.shortcuts import render, HttpResponse
from .models import Task


def index(request):
    task_list = Task.objects.all()
    return render(request, 'main_app/index.html', {'task_list': task_list})
