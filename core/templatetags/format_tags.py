from django import template
import math

register = template.Library()

@register.filter(name='format_price')
def format_price(value):
    try:
        int_value = math.trunc(value)
        return f"{int_value:,}"
    except (ValueError, TypeError):
        return value

@register.filter(name='format_specs')
def format_specs(description_string):
    specs = []
    if not description_string:
        return specs
    
    lines = description_string.strip().splitlines()
    
    for line in lines:
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            if key and value:
                specs.append({'key': key, 'value': value})
    return specs