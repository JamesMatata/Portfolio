from django import template

register = template.Library()


@register.filter
def split_tools_and_languages(value):
    return value.split(',')
