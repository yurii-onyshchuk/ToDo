# Generated by Django 4.0.1 on 2022-04-18 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_category_user_task_performed_task_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_data',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата створення'),
        ),
    ]
