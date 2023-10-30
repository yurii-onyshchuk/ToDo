from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError

User = get_user_model()


class SignUpForm(UserCreationForm):
    """Form for user registration.

    Customizes the UserCreationForm to remove help text and
    add the ability to create a user with email, phone number, and password.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'autofocus': False})
        self.fields['email'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, commit=True):
        data = self.cleaned_data.copy()
        email = data.pop('email')
        password = data.pop('password1')
        data.pop('password2')
        user = User.objects.create_user(email, password, **data)
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)


class CustomSetPasswordForm(SetPasswordForm):
    """Custom form for setting a new password.

    Removes help text for setting a new password.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''


class CustomPasswordChangeForm(PasswordChangeForm):
    """Custom form for changing a password.

    Removes help text for setting a new password and
    excludes the old password field if the user has no usable password.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = ''
        if not self.user.has_usable_password():
            del self.fields['old_password']


class UserForm(forms.ModelForm):
    """Form for editing user profile information."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False})
        self.fields['username'].help_text = ''

    def clean_username(self):
        """Validate the username to ensure it doesn't contain Cyrillic characters.

        This method checks if the username contains Cyrillic characters (from Ukrainian or Russian alphabets)
        and raises a ValidationError if any are found.

        Returns:
            str: The cleaned username if it does not contain Cyrillic characters.
        Raises:
            ValidationError: If Cyrillic characters are found in the username.

        """
        username = self.cleaned_data['username']
        if [x for x in username if u'\u0400' <= x <= u'\u04FF' or u'\u0500' <= x <= u'\u052F']:
            raise ValidationError('В імені користувача заборонена кирилиця')
        else:
            return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)
