from django import template

register = template.Library()

@register.filter
def capitalize_first(value):
    return value[0].upper() + value[1:] if value else value
