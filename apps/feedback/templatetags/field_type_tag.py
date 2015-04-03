from django import template
register = template.Library()

@register.filter('get_type')
def get_type(field):
    return field.__class__.__name__