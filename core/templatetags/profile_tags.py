from django import template
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def profile_detail(key, value, suffix=""):
    if value is None or value == "":
        value = "Not specified"
    elif isinstance(value, list):
        value = ", ".join(value) if value else "Not specified"
    elif isinstance(value, bool):
        value = "Yes" if value else "No"

    return format_html(
        '<div><dt>{}</dt><dd>{}{}</dd></div>',
        key,
        value,
        suffix
    )
