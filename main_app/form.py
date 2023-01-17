from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'planned_date')
        widgets = {
            'description': forms.Textarea(attrs={'rows': '3'}),
            'planned_date': forms.DateTimeInput(attrs={'type': "datetime-local"}, format="%Y-%m-%dT%H:%M")
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
