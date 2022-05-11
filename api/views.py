from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from main_app.models import Task, Category
from .serializers import TaskSerializer, CategorySerializer


class TaskAPIViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoriesAPIViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
