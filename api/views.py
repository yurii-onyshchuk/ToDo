from rest_framework import generics
from main_app.models import Task
from .serializers import TaskSerializer


# GET and POST
class TaskAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# GET, PUT, PATCH and DELETE
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
