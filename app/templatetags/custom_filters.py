from django import template

register = template.Library()

@register.filter
def sum_attribute(iterable, attribute_path):
    """
    Sum values of a specific attribute in a list of dictionaries
    Usage: {{ queryset|sum_attribute:"field.subfield" }}
    """
    total = 0
    for item in iterable:
        # Traverse the attribute path (e.g., "property_metrics.total_properties")
        value = item
        for attr in attribute_path.split('.'):
            try:
                value = value.get(attr, 0)
            except (AttributeError, TypeError):
                value = 0
                break
        
        try:
            total += float(value)
        except (ValueError, TypeError):
            continue
    return total

@register.filter
def div(value, arg):
    """Divide the value by the arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, ZeroDivisionError):
        return 0