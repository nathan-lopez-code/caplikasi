from django import template

register = template.Library()

@register.simple_tag
def string_splint(value):
    """Ce tag multiplie la valeur par 2."""

    return f"{value[:200]}..."
