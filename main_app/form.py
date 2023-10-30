from django import forms

from .models import Task, Category


class TaskForm(forms.ModelForm):
    """Form for creating or updating a Task object."""

    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'planned_date')
        widgets = {
            'description': forms.Textarea(attrs={'rows': '3'}),
            'planned_date': forms.DateTimeInput(attrs={'type': "datetime-local"}, format="%Y-%m-%dT%H:%M")
        }


class CategoryForm(forms.ModelForm):
    """Form for creating or updating a Category object."""

    class Meta:
        model = Category
        fields = ('title',)
