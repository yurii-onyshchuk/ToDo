from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    def clean_username(self):
        username = self.cleaned_data['username']
        if [x for x in username if u'\u0400' <= x <= u'\u04FF' or u'\u0500' <= x <= u'\u052F']:
            raise ValidationError('В імені користувача заборонена кирилиця')
        else:
            return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class UserSettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})

    def clean_username(self):
        username = self.cleaned_data['username']
        if [x for x in username if u'\u0400' <= x <= u'\u04FF' or u'\u0500' <= x <= u'\u052F']:
            raise ValidationError('В імені користувача заборонена кирилиця')
        else:
            return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        help_texts = {'username': ''}


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старий пароль:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Новий пароль:", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Новий пароль (підтвердження):",
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача",
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': 'None'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
