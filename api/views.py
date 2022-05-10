from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from main_app.models import Task
from .serializers import TaskSerializer


class TaskAPIViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
