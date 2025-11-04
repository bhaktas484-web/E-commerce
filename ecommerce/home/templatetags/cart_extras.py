
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Allows dictionary access in templates"""
    return dictionary.get(key)
