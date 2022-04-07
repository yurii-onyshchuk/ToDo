from django.db import models
from django.urls import reverse


class Task(models.Model):
    title = models.CharField(verbose_name='Назва', max_length=100)
    text = models.TextField(verbose_name='Опис')
    created_data = models.DateTimeField(verbose_name='Срок виконання', null=True)
    category = models.ForeignKey('Category', verbose_name='Категорія', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = 'Завдання'
        verbose_name_plural = 'Завдання'

    def __str__(self):
        return f'{self.title}, {self.title}'


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_by_category', kwargs={'pk': self.pk})
