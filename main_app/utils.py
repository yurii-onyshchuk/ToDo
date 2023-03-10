from django.urls import reverse_lazy

from main_app.form import TaskForm
from main_app.models import Category


class TaskEditMixin:
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'].fields['category'].queryset = Category.objects.filter(user=self.request.user)
        context['form'].fields['category'].empty_label = "Всі завдання"
        context['form'].fields['category'].initial = self.request.GET.get('init_cat')
        return context

    def get_success_url(self):
        if self.request.POST['category']:
            return reverse_lazy('task-by-category', kwargs={'pk': self.request.POST['category'], })
        else:
            return reverse_lazy('tasks')


class AddUserToFormMixin:
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddUserToFormMixin, self).form_valid(form)
