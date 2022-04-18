from django import template
from main_app.models import Category

register = template.Library()


@register.inclusion_tag('main_app/inc/_sidebar.html')
def show_sidebar(request):
    category = Category.objects.filter(user=request.user)
    return {'category': category, 'request': request}
