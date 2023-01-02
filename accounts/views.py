from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import FormView, UpdateView

from .form import UserRegisterForm, UserAuthenticationForm, UserSettingForm, UserPasswordChangeForm


class UserRegister(FormView):
    extra_context = {'title': 'Реєстрація'}
    template_name = 'main_app/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Успішна реєстрація!')
        return super(UserRegister, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Помилка реєстрації!')
        return super(UserRegister, self).form_invalid(form)


class UserLogin(LoginView):
    extra_context = {'title': 'Вхід'}
    template_name = 'main_app/login.html'
    form_class = UserAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class UserSetting(LoginRequiredMixin, UpdateView):
    extra_context = {'title': 'Налаштування акаунту'}
    model = User
    form_class = UserSettingForm
    template_name = 'main_app/user_form.html'
    success_url = reverse_lazy('tasks')

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    extra_context = {'title': 'Зміна паролю'}
    template_name = 'main_app/password_change.html'
    form_class = UserPasswordChangeForm
