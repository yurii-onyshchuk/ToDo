from django.db import models


class Task(models.Model):
    title = models.CharField('Назва', max_length=100)
    text = models.TextField('Опис')
    created_data = models.DateTimeField('Срок виконання', null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)

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
