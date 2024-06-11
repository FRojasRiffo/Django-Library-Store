# myapp/templatetags/multiply.py

from django import template

# Register the custom filter
register = template.Library()

@register.filter
def multiply(value, arg):
    """
    Multiplies the value by the arg.
    """
    return value * arg
