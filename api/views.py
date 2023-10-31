from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import viewsets

from .serializers import TaskSerializer, CategorySerializer
from main_app.models import Task, Category
from .services.swagger import swagger_safe

User = get_user_model()


class TaskAPIViewSet(viewsets.ModelViewSet):
    """API view for the Task model."""

    serializer_class = TaskSerializer

    @swagger_safe(Task)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=True)


class CategoriesAPIViewSet(viewsets.ModelViewSet):
    """API view for the Category model."""

    serializer_class = CategorySerializer

    @swagger_safe(Category)
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TaskByCategoryAPIView(generics.ListAPIView):
    """API view for retrieving tasks by category."""

    serializer_class = TaskSerializer

    @swagger_safe(Task)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, category__pk=self.kwargs['pk'], performed_date__isnull=True)


class PerformedTaskAPIView(generics.ListAPIView):
    """API view for retrieving performed tasks."""

    serializer_class = TaskSerializer

    @swagger_safe(Task)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, performed_date__isnull=False)
