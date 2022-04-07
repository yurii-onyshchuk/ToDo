from django import template
from main_app.models import Category

register = template.Library()


@register.inclusion_tag('main_app/inc/_sidebar.html')
def show_sidebar():
    category = Category.objects.all()
    return {'category': category}
