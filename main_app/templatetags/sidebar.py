from django import template
from datetime import datetime
from main_app.models import Category, Task

register = template.Library()


@register.inclusion_tag('main_app/inc/_sidebar.html')
def show_sidebar(request):
    """Inclusion tag for rendering the sidebar.

    This tag renders the sidebar, including the list of categories
    in the user's tasks.
    """
    category = Category.objects.filter(user=request.user)
    return {'category': category, 'request': request}


@register.simple_tag()
def get_task_amount(user, category=None, today=False, upcoming=False, expired=False):
    """Template tag to get the amount of tasks based on specific criteria.

    This tag calculates the number of tasks based on different criteria such as category,
    tasks for today, upcoming tasks or expired tasks.
    """
    if category:
        return Task.objects.filter(user=user, category__pk=category, performed_date=None).count()
    elif today:
        return Task.objects.filter(user=user, planned_date__date=datetime.today().date(), performed_date=None).count()
    elif upcoming:
        return Task.objects.filter(user=user, planned_date__isnull=False, performed_date=None).count()
    elif expired:
        return Task.objects.filter(user=user, planned_date__lt=datetime.today(), performed_date=None).count()
    else:
        return Task.objects.filter(user=user, performed_date=None).count()
