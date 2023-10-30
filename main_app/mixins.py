from django.urls import reverse_lazy

from main_app.form import TaskForm
from main_app.models import Category


class TaskEditMixin:
    """ Mixin for editing tasks.

    This mixin provides functionality for editing tasks, including handling form classes,
    context data and success URL based on the user's request.
    """

    form_class = TaskForm

    def get_context_data(self, **kwargs):
        """Customize the context data for editing tasks.

        This method updates the form fields to include categories, set the initial category,
        and provide an empty label for the category dropdown.
        """

        context = super().get_context_data(**kwargs)
        context['form'].fields['category'].queryset = Category.objects.filter(user=self.request.user)
        context['form'].fields['category'].empty_label = "Всі завдання"
        context['form'].fields['category'].initial = self.request.GET.get('init_cat')
        return context

    def get_success_url(self):
        """Get the success URL to redirect to after a successful task edit.

        The URL is based on the category selected in the form.
        """

        if self.request.POST['category']:
            return reverse_lazy('task-by-category', kwargs={'pk': self.request.POST['category'], })
        else:
            return reverse_lazy('tasks')


class AddUserToFormMixin:
    """Mixin for adding the user to a form.

    This mixin adds the current user to a form instance before saving it.
    """

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AddUserToFormMixin, self).form_valid(form)
