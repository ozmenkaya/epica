from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    """Get dictionary value by key"""
    if isinstance(d, dict):
        return d.get(key, {})
    return {}
