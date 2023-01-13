from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'category', 'planned_date')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'planned_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': "datetime-local"},
                                                format="%Y-%m-%dT%H:%M")
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
