from django import forms
from .models import Task, Category


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "--Без категорії--"

    class Meta:
        model = Task
        fields = ('title', 'text', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }
