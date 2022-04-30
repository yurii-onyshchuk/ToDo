from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Task, Category


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'text', 'category')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="Ім'я користувача",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'None'}))
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Підтвердження паролю",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'None'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
