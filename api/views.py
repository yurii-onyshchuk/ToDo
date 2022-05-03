from rest_framework import generics
from main_app.models import Task
from .serializers import TaskSerializer


class TaskAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
