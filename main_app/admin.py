from django.contrib import admin

from .models import Task, Category


class TaskAdmin(admin.ModelAdmin):
    """Admin class for the Task model.

    Defines the display of Task objects in the Django admin panel.
    """

    list_display = ('id', 'title')


class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""

    list_display = ('id', 'title')


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
