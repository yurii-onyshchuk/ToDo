from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserSingUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def clean_username(self):
        username = self.cleaned_data['username']
        if [x for x in username if u'\u0400' <= x <= u'\u04FF' or u'\u0500' <= x <= u'\u052F']:
            raise ValidationError('В імені користувача заборонена кирилиця')
        else:
            return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)


class UserSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].help_text = ''

    def clean_username(self):
        username = self.cleaned_data['username']
        if [x for x in username if u'\u0400' <= x <= u'\u04FF' or u'\u0500' <= x <= u'\u052F']:
            raise ValidationError('В імені користувача заборонена кирилиця')
        else:
            return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)
