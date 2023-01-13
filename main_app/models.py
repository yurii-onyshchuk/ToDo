from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Task(models.Model):
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
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, db_index=True, verbose_name='Назва категорії')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-by-category', kwargs={'pk': self.pk})
