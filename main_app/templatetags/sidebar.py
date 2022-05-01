from django import template
from main_app.models import Category, Task

register = template.Library()


@register.inclusion_tag('main_app/inc/_sidebar.html')
def show_sidebar(request):
    category = Category.objects.filter(user=request.user)
    return {'category': category, 'request': request}


@register.simple_tag()
def get_task_amount(user, category=None):
    if category:
        return Task.objects.filter(user=user, category__pk=category, performed=False).count()
    else:
        return Task.objects.filter(user=user, performed=False).count()
