from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Task(models.Model):
    """Model to represent a task of user"""

    user = models.ForeignKey(verbose_name='Користувач', to=User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='Назва', max_length=100)
    description = models.TextField(verbose_name='Опис', blank=True)
    planned_date = models.DateTimeField(verbose_name='Запланований час виконання', blank=True, null=True)
    created_date = models.DateTimeField(verbose_name='Час створення', auto_now_add=True)
    performed_date = models.DateTimeField(verbose_name='Час виконання', blank=True, null=True)

    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'
        ordering = ('-created_date',)

    def __str__(self):
        return self.title


class Category(models.Model):
    """Model to represent a category of task."""

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, db_index=True, verbose_name='Назва категорії')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the absolute URL for the task category."""
        return reverse('task-by-category', kwargs={'pk': self.pk})
