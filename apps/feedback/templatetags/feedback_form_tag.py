from django import template

register = template.Library()

@register.inclusion_tag('feedback/dashboard/feedback_form.html')
def display_form(form):
    return {'form': form}