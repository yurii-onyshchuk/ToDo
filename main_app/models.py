from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Task(models.Model):
    user = models.ForeignKey(verbose_name='Користувач', to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(verbose_name='Назва', max_length=100)
    text = models.TextField(verbose_name='Опис', blank=True)
    created_data = models.DateTimeField(verbose_name='Дата створення', auto_now_add=True)
    category = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.PROTECT, null=True, blank=True)
    performed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'

    def __str__(self):
        return f'{self.title}, {self.title}'


class Category(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, db_index=True, verbose_name='Назва категорії')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_by_category', kwargs={'pk': self.pk})