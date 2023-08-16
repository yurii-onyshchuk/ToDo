from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import viewsets

from .serializers import TaskSerializer, CategorySerializer
from main_app.models import Task, Category

User = get_user_model()


class TaskAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=True)


class CategoriesAPIViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TaskByCategoryAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, category__pk=self.kwargs['pk'], performed_date__isnull=True)


class PerformedTaskAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=False)
