from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from . import forms
from .mixins import RedirectAuthenticatedUserMixin

User = get_user_model()


class SignUpView(RedirectAuthenticatedUserMixin, CreateView):
    """View for handling the user registration."""

    extra_context = {'title': 'Реєстрація'}
    template_name = 'accounts/signup.html'
    form_class = forms.SignUpForm
    redirect_authenticated_user_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Успішна реєстрація!')
        return redirect('tasks')

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка реєстрації!')
        return super(SignUpView, self).form_invalid(form)


class CustomLoginView(LoginView):
    """View for handling the user login process."""

    extra_context = {'title': 'Вхід'}
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')


class PersonalCabinetView(LoginRequiredMixin, TemplateView):
    """View for the user's personal cabinet.

    This view displays the user's personal cabinet with information about
    orders and personal data.
    """

    extra_context = {'title': 'Особистий кабінет',
                     'subtitle': 'Керуйте своїми особистими даними та безпекою акаунту'}
    template_name = 'accounts/personal_cabinet/personal_cabinet.html'


class PersonalInfoUpdateView(LoginRequiredMixin, UpdateView):
    """View for updating the user's personal information."""

    extra_context = {'title': 'Особисті дані',
                     'subtitle': 'Керуйте своїми особистими та контактними даними'}
    template_name = 'accounts/personal_cabinet/personal_info.html'
    form_class = forms.UserForm

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(self.request, 'Особисті дані успішно змінено!')
        return reverse_lazy('personal_cabinet')


class PersonalSafetyView(LoginRequiredMixin, TemplateView):
    """View for account safety settings."""

    extra_context = {'title': 'Безпека облікового запису',
                     'subtitle': 'Змінити пароль або видалити обліковий запис'}
    template_name = 'accounts/personal_cabinet/personal_safety.html'


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a user's account."""

    extra_context = {'title': 'Видалення облікового запису'}

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)

    def get_success_url(self):
        messages.success(self.request, 'Акаунт успішно видалено!')
        return reverse_lazy(settings.LOGIN_URL)
