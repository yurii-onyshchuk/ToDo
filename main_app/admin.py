from django.contrib import admin
from .models import Task, Category


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
